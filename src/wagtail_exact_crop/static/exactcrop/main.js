class ExactCropWidget {
  constructor(root) {
    this.root = root;
    this.imgUrl = root.dataset.imageUrl;
    this.cropWidth = parseInt(root.dataset.width, 10);
    this.cropHeight = parseInt(root.dataset.height, 10);
    this.locked = true;
    
    // Calculate container scale factor for responsive scaling
    this.containerScale = this.calculateContainerScale();

    // --- Create crop container ---
    this.container = document.createElement("div");
    this.container.classList.add("cropper");
    this.container.style.position = "relative";
    this.container.style.overflow = "hidden";
    this.container.style.width = (this.cropWidth * this.containerScale) + "px";
    this.container.style.height = (this.cropHeight * this.containerScale) + "px";
    this.container.style.background = "black";
    root.appendChild(this.container);

    // --- Image ---
    this.img = new Image();
    this.img.src = this.imgUrl;
    this.img.style.position = "absolute";
    this.img.style.top = "0";
    this.img.style.left = "0";
    this.img.style.transformOrigin = "top left";
    this.img.style.maxWidth = "none";
    this.img.draggable = false;
    this.container.appendChild(this.img);

    // --- Overlay canvas ---
    this.overlay = document.createElement("canvas");
    this.overlay.style.position = "absolute";
    this.overlay.style.top = "0";
    this.overlay.style.left = "0";
    this.overlay.style.width = "100%";
    this.overlay.style.height = "100%";
    this.overlay.style.pointerEvents = "none";
    this.overlayCtx = this.overlay.getContext("2d");
    this.container.appendChild(this.overlay);
    this.overlayEnabled = false;

    // --- Controls ---
    const controlsContainer = document.createElement("div");
    controlsContainer.style = "padding: 1rem 0;";
    this.root.appendChild(controlsContainer);

    this.lockToggleBtn = this.createButton("Edit crop", () => {
      this.setLocked(!this.locked);
    });
    this.lockToggleBtn.className = "button button-secondary";
    this.lockToggleBtn.setAttribute("aria-pressed", "false");
    controlsContainer.appendChild(this.lockToggleBtn);
    
    this.fitBtn = this.createButton("Fit to crop", () => this.fitToCrop());
    this.fitBtn.className = "button button-secondary yes"
    controlsContainer.appendChild(this.fitBtn);
    
    this.overlayToggleBtn = this.createButton("Toggle guides", () => {
      if (this.locked) return;
      this.overlayEnabled = !this.overlayEnabled;
      this.drawOverlay();
    });
    this.overlayToggleBtn.className = "button button-secondary yes"
    controlsContainer.appendChild(this.overlayToggleBtn);
    
    this.resetBtn = this.createButton("Reset", () => this.resetToInitialState());
    this.resetBtn.className = "button button-secondary yes"
    controlsContainer.appendChild(this.resetBtn);

    // Zoom slider
    this.zoomSlider = document.createElement("input");
    this.zoomSlider.type = "range";
    this.zoomSlider.step = "0.001";
    this.zoomSlider.style.display = "block";
    this.zoomSlider.style.width = "100%";
    this.zoomSlider.addEventListener("input", () => {
      if (this.locked) return;
      this.scale = parseFloat(this.zoomSlider.value);
      this.updateTransform();
    });
    root.appendChild(this.zoomSlider);

    this.pos = { x: 0, y: 0 };
    this.scale = 1;
    this.previewEnabled = false;
    this.initialState = null;

    // --- On image load ---
    this.img.onload = () => {
      this.naturalWidth = this.img.naturalWidth;
      this.naturalHeight = this.img.naturalHeight;

      const scaleX = this.cropWidth / this.naturalWidth;
      const scaleY = this.cropHeight / this.naturalHeight;
      this.minScale = Math.max(scaleX, scaleY);
      this.maxScale = 1.0;

      this.zoomSlider.min = this.minScale;
      this.zoomSlider.max = this.maxScale;
      this.zoomSlider.value = this.minScale;

      if (!this.loadFromJSON()) {
        this.fitToCrop();
      }
      // Store initial state after loading
      this.initialState = {
        pos: { x: this.pos.x, y: this.pos.y },
        scale: this.scale
      };
    };

    this.initDrag();
    this.drawOverlay();
    this.setLocked(true);
    
    // Handle window resize for responsive scaling
    window.addEventListener("resize", () => {
      this.handleResize();
    });
  }

  calculateContainerScale() {
    const rootWidth = this.root.clientWidth;
    
    // If container is smaller than crop width, scale down
    // If container is larger, keep at actual size (scale = 1)
    const scale = Math.min(rootWidth / this.cropWidth, 1);
    
    return Math.max(scale, 0.1); // Minimum scale to prevent too small
  }

  handleResize() {
    const newScale = this.calculateContainerScale();
    if (Math.abs(newScale - this.containerScale) > 0.01) {
      this.containerScale = newScale;
      this.container.style.width = (this.cropWidth * this.containerScale) + "px";
      this.container.style.height = (this.cropHeight * this.containerScale) + "px";
      this.updateTransform();
      this.drawOverlay();
    }
  }

  createButton(label, onClick) {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.innerText = label;
    btn.addEventListener("click", onClick);
    return btn;
  }

  setLocked(locked) {
    this.locked = locked;
    this.root.classList.toggle("is-locked", locked);
    this.root.classList.toggle("is-unlocked", !locked);
    this.lockToggleBtn.innerText = locked ? "Edit crop" : "Done";
    this.lockToggleBtn.setAttribute("aria-pressed", String(!locked));
    this.fitBtn.disabled = locked;
    this.overlayToggleBtn.disabled = locked;
    this.resetBtn.disabled = locked;
    this.zoomSlider.disabled = locked;
    if (locked) {
      this.overlayEnabled = false;
      this.drawOverlay();
    }
  }

  fitToCrop() {
    this.scale = this.minScale;
    const displayWidth = this.naturalWidth * this.scale;
    const displayHeight = this.naturalHeight * this.scale;

    // center
    this.pos.x = (this.cropWidth - displayWidth) / 2;
    this.pos.y = (this.cropHeight - displayHeight) / 2;

    this.updateTransform();
  }

  resetToInitialState() {
    if (this.initialState) {
      this.pos.x = this.initialState.pos.x;
      this.pos.y = this.initialState.pos.y;
      this.scale = this.initialState.scale;
      this.updateTransform();
    }
  }

  loadFromJSON() {
    const textarea = document.querySelector("#id_exact_crops");
    let data = {};
    try {
      data = JSON.parse(textarea.value || "{}");
    } catch (e) { return false; }

    const keys = this.root.dataset.presets.split(",");
    const key = keys[0];
    if (!data[key]) return false;

    const rel = data[key];
    this.scale = Math.min(Math.max(rel.scale, this.minScale), this.maxScale);

    const displayWidth = this.naturalWidth * this.scale;
    const displayHeight = this.naturalHeight * this.scale;

    this.pos.x = -rel.x * displayWidth;
    this.pos.y = -rel.y * displayHeight;

    this.updateTransform();
    return true;
  }

  initDrag() {
    let dragging = false;
    let lastX, lastY;

    this.container.addEventListener("mousedown", e => {
      if (this.locked) return;
      dragging = true;
      lastX = e.clientX;
      lastY = e.clientY;
    });

    window.addEventListener("mousemove", e => {
      if (!dragging) return;
      const dx = (e.clientX - lastX) / this.containerScale;
      const dy = (e.clientY - lastY) / this.containerScale;
      this.pos.x += dx;
      this.pos.y += dy;
      lastX = e.clientX;
      lastY = e.clientY;
      this.updateTransform();
    });

    window.addEventListener("mouseup", () => dragging = false);

    this.container.addEventListener("wheel", e => {
      if (this.locked) return;
      e.preventDefault();
      const oldScale = this.scale;
      const zoomFactor = 0.05;
      this.scale *= e.deltaY < 0 ? 1 + zoomFactor : 1 - zoomFactor;
      this.scale = Math.min(Math.max(this.scale, this.minScale), this.maxScale);

      // Zoom toward cursor
      const rect = this.container.getBoundingClientRect();
      const cx = (e.clientX - rect.left) / this.containerScale - this.pos.x;
      const cy = (e.clientY - rect.top) / this.containerScale - this.pos.y;
      this.pos.x -= (cx / oldScale) * (this.scale - oldScale);
      this.pos.y -= (cy / oldScale) * (this.scale - oldScale);

      this.updateTransform();
    });
  }

  clamp() {
    const displayWidth = this.naturalWidth * this.scale;
    const displayHeight = this.naturalHeight * this.scale;

    if (this.pos.x > 0) this.pos.x = 0;
    if (this.pos.y > 0) this.pos.y = 0;
    if (this.pos.x + displayWidth < this.cropWidth) this.pos.x = this.cropWidth - displayWidth;
    if (this.pos.y + displayHeight < this.cropHeight) this.pos.y = this.cropHeight - displayHeight;
  }

  updateTransform() {
    this.clamp();
    // Apply container scale to the transform
    const scaledX = this.pos.x * this.containerScale;
    const scaledY = this.pos.y * this.containerScale;
    const scaledImageScale = this.scale * this.containerScale;
    this.img.style.transform = `translate(${scaledX}px, ${scaledY}px) scale(${scaledImageScale})`;
    this.zoomSlider.value = this.scale;
    this.updateJSON();
    this.drawOverlay();
  }

  updateJSON() {
    const textarea = document.querySelector("#id_exact_crops");
    let data = {};
    try { data = JSON.parse(textarea.value || "{}"); } catch(e) {}

    const displayWidth = this.naturalWidth * this.scale;
    const displayHeight = this.naturalHeight * this.scale;
    const relX = -this.pos.x / displayWidth;
    const relY = -this.pos.y / displayHeight;
    const relW = this.cropWidth / displayWidth;
    const relH = this.cropHeight / displayHeight;

    const keys = this.root.dataset.presets.split(",");
    for (const key of keys) {
      data[key] = {
        x: Number(relX.toFixed(6)),
        y: Number(relY.toFixed(6)),
        scale: Number(this.scale.toFixed(6)),
        w: Number(relW.toFixed(6)),
        h: Number(relH.toFixed(6))
      };
    }

    textarea.value = JSON.stringify(data, null, 2);
  }

  drawOverlay() {
    const ctx = this.overlayCtx;
    const w = this.container.clientWidth;
    const h = this.container.clientHeight;

    this.overlay.width = w;
    this.overlay.height = h;

    ctx.clearRect(0, 0, w, h);
    if (!this.overlayEnabled) return;

    ctx.lineWidth = 1;
    ctx.strokeStyle = "white";

    // Crosshair
    ctx.beginPath();
    ctx.moveTo(w/2 - 20, h/2); ctx.lineTo(w/2 + 20, h/2);
    ctx.moveTo(w/2, h/2 - 20); ctx.lineTo(w/2, h/2 + 20);
    ctx.stroke();

    ctx.setLineDash([3, 3]);

    // Thirds
    ctx.beginPath();
    ctx.moveTo(w/3, 0); ctx.lineTo(w/3, h);
    ctx.moveTo(2*w/3,0); ctx.lineTo(2*w/3,h);
    ctx.moveTo(0,h/3); ctx.lineTo(w,h/3);
    ctx.moveTo(0,2*h/3); ctx.lineTo(w,2*h/3);
    ctx.stroke();

  }
}

// Initialize all widgets
document.querySelectorAll(".exact-crop-widget").forEach(el => new ExactCropWidget(el));
