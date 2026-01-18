const { app, BrowserWindow, ipcMain, globalShortcut } = require('electron');
const path = require('path');

let overlayWindow = null;

function createOverlay() {
  overlayWindow = new BrowserWindow({
    width: 380,
    height: 600,
    x: 20,
    y: 20,
    frame: false,
    transparent: true,
    alwaysOnTop: true,
    skipTaskbar: true,
    resizable: false,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js')
    },
    // macOS specific
    hasShadow: true,
    vibrancy: 'under-window',
    visualEffectState: 'active',
    // Windows specific  
    backgroundColor: '#00000000'
  });

  // Load the overlay UI
  // In production, load from built frontend
  // In development, load from dev server
  const isDev = process.argv.includes('--dev');
  
  if (isDev) {
    overlayWindow.loadURL('http://localhost:5173/widget');
    overlayWindow.webContents.openDevTools({ mode: 'detach' });
  } else {
    overlayWindow.loadFile(path.join(__dirname, '../frontend/dist/index.html'), {
      hash: '/widget'
    });
  }

  // Make window draggable
  overlayWindow.setIgnoreMouseEvents(false);
  
  // Prevent window from being closed, just hide it
  overlayWindow.on('close', (e) => {
    e.preventDefault();
    overlayWindow.hide();
  });

  // Listen for position updates from renderer
  ipcMain.on('move-window', (event, { x, y }) => {
    overlayWindow.setPosition(x, y);
  });

  // Listen for show/hide toggle
  ipcMain.on('toggle-window', () => {
    if (overlayWindow.isVisible()) {
      overlayWindow.hide();
    } else {
      overlayWindow.show();
    }
  });

  // Listen for minimize request
  ipcMain.on('minimize-window', () => {
    overlayWindow.setSize(200, 60);
  });

  // Listen for maximize request
  ipcMain.on('maximize-window', () => {
    overlayWindow.setSize(380, 600);
  });

  return overlayWindow;
}

app.whenReady().then(() => {
  createOverlay();

  // Register global shortcut to toggle overlay
  globalShortcut.register('CommandOrControl+Shift+V', () => {
    if (overlayWindow.isVisible()) {
      overlayWindow.hide();
    } else {
      overlayWindow.show();
      overlayWindow.focus();
    }
  });

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createOverlay();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('will-quit', () => {
  // Unregister all shortcuts
  globalShortcut.unregisterAll();
});

// Keep app running in background
app.on('before-quit', (event) => {
  if (!app.isQuitting) {
    event.preventDefault();
    overlayWindow.hide();
  }
});

// Menu bar icon (optional - for future)
// const { Tray, Menu } = require('electron');
// let tray = null;
// tray = new Tray('/path/to/icon.png');
// const contextMenu = Menu.buildFromTemplate([
//   { label: 'Show Overlay', click: () => overlayWindow.show() },
//   { label: 'Hide Overlay', click: () => overlayWindow.hide() },
//   { type: 'separator' },
//   { label: 'Quit', click: () => { app.isQuitting = true; app.quit(); } }
// ]);
// tray.setContextMenu(contextMenu);
