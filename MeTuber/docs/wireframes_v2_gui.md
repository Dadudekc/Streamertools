# V2 GUI Wireframes & Mockups

**Reference:** [Track 1: GUI Layout & Usability](./track1_gui_layout_usability.md) | [PRD](./prd.md)

---

## Design Overview

Based on research of modern webcam/streaming applications, the V2 GUI will feature a **preview-centric layout** with **sidebar controls** and **progressive disclosure** of advanced features.

### Layout Structure
```
┌─────────────────────────────────────────────────────────────┐
│                    Top Toolbar                              │
│ [Device Selector] [Main Actions] [Settings] [Help]         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│                    Preview Area                             │
│                    (60% of screen)                         │
│                                                             │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                    Status Bar                               │
│ [Performance] [Connection] [FPS] [Memory]                  │
└─────────────────────────────────────────────────────────────┘
```

---

## Detailed Wireframes

### 1. Main Window Layout

```
┌─────────────────────────────────────────────────────────────┐
│ 🎥 [Webcam 0 ▼] [▶ Start] [⏹ Stop] [📸 Snapshot] [⚙] [❓] │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│                    PREVIEW AREA                             │
│                                                             │
│                    [Webcam Feed]                            │
│                                                             │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│ Status: Running | FPS: 30 | Memory: 45MB | CPU: 12%        │
└─────────────────────────────────────────────────────────────┘
```

### 2. Sidebar Controls (Collapsible)

```
┌─────────────────────────────────────────────────────────────┐
│ 🎥 [Webcam 0 ▼] [▶ Start] [⏹ Stop] [📸 Snapshot] [⚙] [❓] │
├─────────────────────────────────────────────────────────────┤
│                    PREVIEW AREA                             │
│                                                             │
│                    [Webcam Feed]                            │
│                                                             │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│ Status: Running | FPS: 30 | Memory: 45MB | CPU: 12%        │
└─────────────────────────────────────────────────────────────┘
```

### 3. Style Selection Panel

```
┌─────────────────────────────────────────────────────────────┐
│ 🎨 STYLES                                                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ ┌─ Artistic ──────────────────────────────────────────────┐ │
│ │ [Cartoon ▼] [Sketch ▼] [Watercolor ▼] [Oil Paint ▼]    │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                             │
│ ┌─ Basic ─────────────────────────────────────────────────┐ │
│ │ [Brightness ▼] [Contrast ▼] [Saturation ▼] [Blur ▼]    │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                             │
│ ┌─ Distortions ───────────────────────────────────────────┐ │
│ │ [Glitch ▼] [Wave ▼] [Mirror ▼] [Kaleidoscope ▼]        │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                             │
│ ┌─ Color Filters ─────────────────────────────────────────┐ │
│ │ [Sepia ▼] [Vintage ▼] [Neon ▼] [Monochrome ▼]          │ │
│ └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### 4. Parameter Controls Panel

```
┌─────────────────────────────────────────────────────────────┐
│ ⚙ PARAMETERS                                                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ ┌─ Cartoon Settings ─────────────────────────────────────┐ │
│ │ Intensity: [████████░░] 80%                            │ │
│ │ Edge Strength: [██████░░░░] 60%                        │ │
│ │ Color Depth: [██████████] 100%                         │ │
│ │ Smoothing: [████░░░░░░░░] 40%                          │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                             │
│ ┌─ Advanced Options ─────────────────────────────────────┐ │
│ │ [ ] Enable Edge Detection                              │ │
│ │ [ ] Use GPU Acceleration                               │ │
│ │ [ ] Auto-optimize Performance                          │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                             │
│ [Reset to Default] [Save Preset] [Load Preset]            │
└─────────────────────────────────────────────────────────────┘
```

### 5. Performance & Settings Panel

```
┌─────────────────────────────────────────────────────────────┐
│ ⚙ SETTINGS                                                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ ┌─ Performance ───────────────────────────────────────────┐ │
│ │ Max FPS: [████████░░] 80%                              │ │
│ │ Frame Skip: [██░░░░░░░░] 20%                           │ │
│ │ Quality: [High ▼]                                      │ │
│ │ Resolution: [720p ▼]                                   │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                             │
│ ┌─ Output ───────────────────────────────────────────────┐ │
│ │ Virtual Camera: [OBS Virtual Camera ▼]                │ │
│ │ Snapshot Format: [PNG ▼]                              │ │
│ │ Save Directory: [📁 Browse...]                        │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                             │
│ ┌─ Interface ────────────────────────────────────────────┐ │
│ │ Theme: [Dark ▼]                                        │ │
│ │ Language: [English ▼]                                  │ │
│ │ [ ] Show Performance Overlay                          │ │
│ │ [ ] Enable Tooltips                                   │ │
│ └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## Responsive Breakpoints

### Desktop (1200px+)
- Full sidebar visible
- Large preview area
- All controls accessible

### Tablet (768px - 1199px)
- Collapsible sidebar
- Medium preview area
- Stacked control panels

### Mobile (320px - 767px)
- Full-screen preview
- Bottom sheet controls
- Simplified interface

---

## Accessibility Considerations

### Keyboard Navigation
- Tab order: Device → Style → Parameters → Actions
- Arrow keys for parameter adjustment
- Space/Enter for button activation
- Escape for closing dialogs

### Screen Reader Support
- Descriptive labels for all controls
- Status announcements for changes
- Logical grouping of related elements

### Visual Accessibility
- High contrast mode option
- Adjustable font sizes
- Color-blind friendly palette
- Clear focus indicators

---

## Implementation Notes

### PyQt5 Components Needed
1. **QSplitter** - For resizable preview/sidebar
2. **QTabWidget** - For style categories
3. **QComboBox** - For style variants and device selection
4. **QSlider** - For parameter adjustment
5. **QGroupBox** - For parameter grouping
6. **QToolBar** - For main actions
7. **QStatusBar** - For performance metrics

### CSS Styling
- Dark theme by default
- Consistent spacing (8px grid)
- Modern rounded corners
- Subtle shadows and highlights
- Smooth transitions

### State Management
- Save/restore sidebar collapse state
- Remember last used style and parameters
- Auto-save user preferences
- Session persistence 