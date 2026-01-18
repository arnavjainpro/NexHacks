# Veritas Electron Desktop Overlay Setup

Transform Veritas into a **system-wide overlay** that floats on top of Zoom, Google Meet, Teams, and any application.

## 🚀 Quick Start

### Step 1: Install Electron Dependencies

```bash
cd electron
npm install
```

### Step 2: Start Frontend Dev Server

In a separate terminal:
```bash
cd frontend
npm run dev
```

### Step 3: Launch Overlay App

```bash
cd electron
npm run dev
```

The overlay window will appear! It floats on top of **all applications**.

## ✨ Features

- **System-wide overlay** - Appears on top of Zoom, Meet, Teams, Slack, anything!
- **Always on top** - Never gets hidden by other windows
- **Draggable** - Position anywhere on your screen
- **Transparent** - Native window with no borders
- **Global shortcut** - Press `Cmd+Shift+V` (Mac) or `Ctrl+Shift+V` (Windows) to show/hide
- **Minimizable** - Collapse to small badge when not needed
- **Doesn't clutter taskbar** - Stays hidden from taskbar/dock

## 🎯 Usage During Zoom Calls

1. **Open Zoom** (or any video conferencing app)
2. **Launch Veritas Overlay**: `npm run dev` in electron folder
3. **Position the overlay** next to your Zoom window
4. **Start recording** when you join a call
5. **Get real-time compliance nudges** during your conversation
6. **Press `Cmd+Shift+V`** to quickly show/hide the overlay

## 🔧 Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Cmd+Shift+V` (Mac) / `Ctrl+Shift+V` (Win) | Show/Hide overlay |
| Click & Drag header | Move window |
| Click minimize button | Collapse to badge |
| Click maximize button | Expand to full size |

## 📦 Building for Distribution

### Build Frontend First
```bash
cd frontend
npm run build
```

### Build Desktop App

**For macOS:**
```bash
cd electron
npm run build
# Creates Veritas Overlay.dmg in electron/dist/
```

**For Windows:**
```bash
cd electron
npm run build
# Creates installer in electron/dist/
```

### Install & Use
- **Mac**: Open the `.dmg`, drag to Applications
- **Windows**: Run the installer `.exe`

The app will run in the background and can be toggled with `Cmd+Shift+V`.

## 🔐 Permissions (macOS)

For the overlay to work on top of Zoom/Meet:
1. Go to **System Preferences** → **Security & Privacy** → **Screen Recording**
2. Enable **Veritas Overlay**
3. Restart the app

## 🏗️ Architecture

```
┌─────────────────────────────────────┐
│   Zoom / Google Meet / Teams        │  ← Your video call
│                                     │
│  ┌───────────────────────────┐     │
│  │  Veritas Overlay (Electron)│     │  ← Floating on top
│  │  • Compliance alerts       │     │
│  │  • Live transcript         │     │
│  │  • Privacy-first           │     │
│  └───────────────────────────┘     │
└─────────────────────────────────────┘
```

**Technology Stack:**
- **Electron**: Native desktop window management
- **React + Vite**: Frontend UI (same as web version)
- **WebSockets**: Real-time backend connection
- **IPC Bridge**: Secure communication between Electron & React

## 🆚 Web vs Desktop

| Feature | Web Widget | Desktop Overlay |
|---------|-----------|----------------|
| Overlay on Zoom | ❌ Only in browser | ✅ System-wide |
| Always on top | ❌ Only within browser | ✅ Above all apps |
| Global shortcut | ❌ | ✅ Cmd+Shift+V |
| Draggable | ✅ | ✅ |
| No taskbar clutter | ❌ | ✅ |
| Installation | None | One-time |

## 🔮 Future Enhancements

- [ ] System tray icon with menu
- [ ] Auto-start on system boot
- [ ] Multiple monitor support
- [ ] Custom global shortcuts
- [ ] Auto-hide when idle
- [ ] Screen edge snapping
- [ ] Theme customization
- [ ] Audio capture from system

## 🐛 Troubleshooting

**Overlay not appearing?**
- Check if frontend dev server is running on port 5173
- Verify no firewall blocking localhost

**Can't drag window?**
- Click and hold the header bar (dark blue area)
- Drag to desired position

**Shortcut not working?**
- Check if another app is using `Cmd+Shift+V`
- Try restarting the Electron app

**Overlay behind Zoom?**
- Restart the Electron app
- On Mac, grant Screen Recording permissions

## 💡 Development Tips

**Hot reload:**
- Frontend changes auto-reload (Vite HMR)
- Electron main.js changes require restart

**Debug mode:**
- DevTools automatically open in dev mode
- Check console for errors

**Testing:**
- Start Zoom/Meet in browser or desktop app
- Launch overlay and position it
- Test drag, minimize, shortcuts
