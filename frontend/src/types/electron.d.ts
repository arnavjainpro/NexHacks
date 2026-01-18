export interface ElectronAPI {
  moveWindow: (position: { x: number; y: number }) => void;
  toggleWindow: () => void;
  minimizeWindow: () => void;
  maximizeWindow: () => void;
  isElectron: boolean;
}

declare global {
  interface Window {
    electron?: ElectronAPI;
  }
}
