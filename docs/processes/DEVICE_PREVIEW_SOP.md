# Device Preview SOP

**Purpose:** Create interactive device mockup previews for mobile app prototypes.

## iPhone 15 Pro Specifications

```
Dimensions: 393 × 852px (logical)
Border Radius: 55px (frame), 45px (screen)
Dynamic Island: 126 × 37px, centered, 12px from top
Frame Padding: 12px
```

## Required Elements

### 1. Frame Structure
```html
<div class="iphone-container">
  <div class="iphone-frame">
    <!-- Side Buttons -->
    <div class="side-button power-button"></div>
    <div class="side-button volume-up"></div>
    <div class="side-button volume-down"></div>
    <div class="side-button silent-switch"></div>

    <div class="iphone-screen">
      <div class="dynamic-island"></div>
      <iframe src="page.html" class="screen-content"></iframe>
    </div>
  </div>
</div>
```

### 2. Viewport Scaling (Critical)

Scale device to fit MacBook screens (14"/16"):

```css
.iphone-container {
  --scale: 0.7;
  transform: scale(var(--scale));
  transform-origin: top center;
}

@media (min-height: 900px)  { .iphone-container { --scale: 0.75; } }
@media (min-height: 1000px) { .iphone-container { --scale: 0.85; } }
@media (min-height: 1100px) { .iphone-container { --scale: 0.95; } }
```

### 3. Layout Structure

Use 3-column grid that fills viewport:

```css
.main-layout {
  height: 100vh;
  display: grid;
  grid-template-columns: 200px 1fr 200px;
  gap: 1rem;
  padding: 1rem;
  overflow: hidden;
}

.side-panel {
  overflow-y: auto;
  max-height: calc(100vh - 2rem);
}

.device-column {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  overflow: hidden;
}
```

### 4. Side Button Positions

```css
.side-button {
  position: absolute;
  width: 4px;
  background: #2c2c2e;
  border-radius: 2px;
}

.power-button  { right: -3px; top: 180px; height: 100px; }
.volume-up     { left: -3px; top: 150px; height: 60px; }
.volume-down   { left: -3px; top: 220px; height: 60px; }
.silent-switch { left: -3px; top: 100px; height: 30px; }
```

### 5. Navigation Features

Required:
- Page list with clickable buttons
- Back/Next buttons
- Keyboard arrow key support (← →)
- Page counter (1 / 8)
- Current page info panel

```javascript
document.addEventListener('keydown', (e) => {
  if (e.key === 'ArrowRight') nextPage();
  else if (e.key === 'ArrowLeft') prevPage();
});
```

## Checklist

- [ ] Device scales to fit viewport (no scrolling)
- [ ] 3-column layout (nav | device | info)
- [ ] Dynamic Island present
- [ ] Side buttons styled
- [ ] Arrow key navigation works
- [ ] Back/Next buttons functional
- [ ] Page list highlights current page
- [ ] Info panel shows page details
- [ ] Back to Index link present
- [ ] Git hash in footer

## Example Reference

See: `projects/personal/bible-buddy-a66e1/mockups/device-preview.html`
