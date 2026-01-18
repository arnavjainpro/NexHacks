import FloatingWidget from '../components/FloatingWidget';

export default function Widget() {
  return (
    <div className="w-screen h-screen bg-transparent">
      <FloatingWidget />
      
      {/* Instructions overlay - remove after first use */}
      <div className="absolute top-4 left-1/2 -translate-x-1/2 bg-black/80 text-white px-4 py-2 rounded-lg text-sm max-w-md text-center">
        <p className="mb-1">💡 <strong>Drag the widget anywhere on screen</strong></p>
        <p className="text-xs opacity-80">
          Position it next to your Zoom/Meet window • Click minimize to reduce • Privacy-first design
        </p>
      </div>
    </div>
  );
}
