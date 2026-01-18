# Veritas Electron Overlay

System-wide floating overlay that works on top of Zoom, Google Meet, Teams, and any other application.

## Quick Start

### Development Mode

1. **Install dependencies:**
   ```bash
   cd electron
   npm install
   ```

2. **Start the frontend dev server** (in another terminal):
   ```bash
   cd ../frontend
   npm run dev
   ```

3. **Start Electron in dev mode:**
   ```bash
   npm run dev
   ```

### Production Build

1. **Build frontend:**
   ```bash
   cd frontend
   npm run build
   ```

2. **Build Electron app:**
   ```bash
   cd electron
   npm run build
   ```

## Features

- ✅ **Always on top** - Floats above Zoom, Meet, Teams, etc.
- ✅ **Draggable** - Position anywhere on screen
- ✅ **Transparent background** - Native window feel
- ✅ **Global shortcut** - `Cmd+Shift+V` (Mac) or `Ctrl+Shift+V` (Windows) to show/hide
- ✅ **Frameless** - No window borders, clean overlay
- ✅ **Minimizable** - Collapse to small badge
- ✅ **Skip taskbar** - Doesn't clutter taskbar/dock

## Global Shortcuts

- `Cmd+Shift+V` (Mac) / `Ctrl+Shift+V` (Windows): Toggle overlay visibility
- Click and drag the header to move window
- Click minimize button to collapse

## Architecture

- **Electron Main Process** (`main.js`): Controls native window
- **Electron Preload** (`preload.js`): Secure IPC bridge
- **React Frontend** (from `/widget` route): UI rendering

## Building for Distribution

### macOS
```bash
npm run build
# Creates .dmg and .zip in dist/
```

### Windows
```bash
npm run build
# Creates installer and portable .exe in dist/
```

## Permissions

### macOS
- **Screen Recording**: Required for overlay on Zoom
  - System Preferences → Security & Privacy → Screen Recording
  - Enable for Veritas Overlay

### Windows
- Runs with normal user permissions
- May need to run as administrator for some features

## Future Enhancements

- [ ] System tray icon for easy access
- [ ] Configurable global shortcut
- [ ] Window snapping to screen edges
- [ ] Multi-monitor support
- [ ] Auto-hide when not in use
- [ ] Custom themes
