# Wagtail Exact Crop Tool

A custom image cropping tool for Wagtail admin that allows precise control over image cropping with a fixed crop area.

## Features

- **Fixed Crop Area**: Users move and scale the image inside a fixed rectangle
- **Smart Initial Positioning**: Images automatically cover the crop area on load
- **Zoom Controls**: Slider and mouse wheel zoom with proper constraints
- **Movement Constraints**: Image cannot leave the crop rectangle
- **Real-time JSON Updates**: Coordinates are automatically saved to the textarea
- **Multiple Widgets**: Support for multiple crop widgets per page
- **Responsive Design**: Works on desktop and mobile devices

## Usage

### HTML Structure

Each crop widget should have this structure:

```html
<div class="exact-crop-widget"
     data-presets="hero_image,thumbnail"
     data-image-url="/media/images/photo.jpg"
     data-width="1600"
     data-height="600">
  <h3 class="exact-crop-title">Hero image</h3>
  <p class="exact-crop-description">Large banner at top of page</p>
  <div class="cropper"></div>
</div>

<textarea id="id_exact_crops" hidden>
{"hero_image": {"x":0.0,"y":0.0,"w":1.0,"h":0.375}}
</textarea>
```

### Data Attributes

- `data-presets`: Comma-separated list of preset keys
- `data-image-url`: URL of the image to crop
- `data-width`: Width of the crop area in pixels
- `data-height`: Height of the crop area in pixels

### JSON Format

The textarea stores crop coordinates as JSON with this structure:

```json
{
  "preset_key": {
    "x": 0.0,  // Left position (0-1, relative to image width)
    "y": 0.0,  // Top position (0-1, relative to image height)
    "w": 1.0,  // Width (0-1, relative to image width)
    "h": 0.375 // Height (0-1, relative to image height)
  }
}
```

## Controls

- **Drag**: Click and drag the image to reposition it
- **Zoom Slider**: Use the slider below the crop area to zoom in/out
- **Mouse Wheel**: Scroll to zoom in/out (when hovering over crop area)

## Constraints

- **No Upscaling**: Images are never scaled beyond 100% of their original size
- **Cover Requirement**: Minimum zoom ensures the image always covers the crop area
- **Boundary Clamping**: Image cannot be moved outside the crop rectangle

## Development

### File Structure

- `static/exactcrop/main.js` - Main JavaScript implementation
- `static/exactcrop/styles.css` - Styling for the crop widgets

### Key Classes

- `ExactCropWidget` - Main class that handles each crop widget
- Methods for image loading, positioning, zooming, and JSON updates

## Integration with Wagtail

The tool integrates with Wagtail's image editing interface and automatically updates the hidden textarea that stores crop coordinates for backend processing.
