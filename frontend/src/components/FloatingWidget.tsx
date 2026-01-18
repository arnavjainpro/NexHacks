import { useState, useEffect } from 'react';
import { Minimize2, Maximize2, X, Mic, MicOff, AlertTriangle, AlertCircle, Info, Shield } from 'lucide-react';

interface Nudge {
  id: string;
  type: 'critical' | 'warning' | 'info';
  message: string;
  timestamp: Date;
}

interface TranscriptSegment {
  speaker: string;
  text: string;
  timestamp: Date;
}

export default function FloatingWidget() {
  const [isMinimized, setIsMinimized] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const [nudges, setNudges] = useState<Nudge[]>([]);
  const [transcript, setTranscript] = useState<TranscriptSegment[]>([]);
  const [position, setPosition] = useState({ x: 20, y: 20 });
  const [isDragging, setIsDragging] = useState(false);
  const [dragOffset, setDragOffset] = useState({ x: 0, y: 0 });

  // Mock WebSocket connection
  useEffect(() => {
    if (isRecording) {
      // Simulate receiving nudges
      const interval = setInterval(() => {
        const mockNudge: Nudge = {
          id: Date.now().toString(),
          type: ['critical', 'warning', 'info'][Math.floor(Math.random() * 3)] as any,
          message: 'Stay within approved claims',
          timestamp: new Date(),
        };
        setNudges(prev => [mockNudge, ...prev].slice(0, 5));
      }, 8000);

      return () => clearInterval(interval);
    }
  }, [isRecording]);

  const handleMouseDown = (e: React.MouseEvent) => {
    if ((e.target as HTMLElement).closest('.drag-handle')) {
      // Check if running in Electron
      if (window.electron?.isElectron) {
        // Let Electron handle the drag via IPC
        return;
      }
      
      // Browser-based drag (original behavior)
      setIsDragging(true);
      setDragOffset({
        x: e.clientX - position.x,
        y: e.clientY - position.y,
      });
    }
  };

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      if (isDragging) {
        const newX = e.clientX - dragOffset.x;
        const newY = e.clientY - dragOffset.y;
        setPosition({ x: newX, y: newY });
        
        // If in Electron, also update native window position
        if (window.electron?.isElectron) {
          window.electron.moveWindow({ x: newX, y: newY });
        }
      }
    };

    const handleMouseUp = () => {
      setIsDragging(false);
    };

    if (isDragging) {
      document.addEventListener('mousemove', handleMouseMove);
      document.addEventListener('mouseup', handleMouseUp);
    }

    return () => {
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleMouseUp);
    };
  }, [isDragging, dragOffset]);

  const getSeverityIcon = (type: string) => {
    switch (type) {
      case 'critical':
        return <AlertTriangle className="w-4 h-4 text-red-500" />;
      case 'warning':
        return <AlertCircle className="w-4 h-4 text-yellow-500" />;
      case 'info':
        return <Info className="w-4 h-4 text-blue-500" />;
      default:
        return <Info className="w-4 h-4" />;
    }
  };

  const getSeverityColor = (type: string) => {
    switch (type) {
      case 'critical':
        return 'border-l-4 border-red-500 bg-red-50';
      case 'warning':
        return 'border-l-4 border-yellow-500 bg-yellow-50';
      case 'info':
        return 'border-l-4 border-blue-500 bg-blue-50';
      default:
        return 'border-l-4 border-gray-500 bg-gray-50';
    }
  };

  if (isMinimized) {
    return (
      <div
        style={{
          position: 'fixed',
          left: position.x,
          top: position.y,
          zIndex: 9999,
        }}
        onMouseDown={handleMouseDown}
        className="cursor-move"
      >
        <div className="drag-handle bg-gradient-to-r from-blue-600 to-blue-700 rounded-lg shadow-2xl p-3 flex items-center gap-2 border border-blue-500">
          <Shield className="w-5 h-5 text-white" />
          <span className="text-white font-semibold text-sm">Veritas</span>
          {isRecording && (
            <div className="w-2 h-2 bg-red-500 rounded-full animate-pulse" />
          )}
          <button
            onClick={() => {
              setIsMinimized(false);
              if (window.electron?.isElectron) {
                window.electron.maximizeWindow();
              }
            }}
            className="ml-2 text-white hover:bg-blue-600 rounded p-1"
          >
            <Maximize2 className="w-4 h-4" />
          </button>
        </div>
      </div>
    );
  }

  return (
    <div
      style={{
        position: 'fixed',
        left: position.x,
        top: position.y,
        zIndex: 9999,
        width: '380px',
        maxHeight: '600px',
      }}
      onMouseDown={handleMouseDown}
      className="flex flex-col bg-white rounded-lg shadow-2xl border border-gray-200 overflow-hidden"
    >
      {/* Header */}
      <div className="drag-handle cursor-move bg-gradient-to-r from-blue-600 to-blue-700 text-white p-3 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Shield className="w-5 h-5" />
          <span className="font-semibold">Veritas Copilot</span>
          {isRecording && (
            <div className="flex items-center gap-1 ml-2">
              <div className="w-2 h-2 bg-red-500 rounded-full animate-pulse" />
              <span className="text-xs">Live</span>
            </div>
          )}
        </div>
        <div className="flex items-center gap-1">
          <button
            onClick={() => {
              setIsMinimized(true);
              if (window.electron?.isElectron) {
                window.electron.minimizeWindow();
              }
            }}
            className="hover:bg-blue-600 rounded p-1 transition-colors"
          >
            <Minimize2 className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Controls */}
      <div className="p-3 bg-gray-50 border-b border-gray-200">
        <button
          onClick={() => setIsRecording(!isRecording)}
          className={`w-full py-2 px-4 rounded-lg font-medium flex items-center justify-center gap-2 transition-all ${
            isRecording
              ? 'bg-red-600 hover:bg-red-700 text-white'
              : 'bg-green-600 hover:bg-green-700 text-white'
          }`}
        >
          {isRecording ? (
            <>
              <MicOff className="w-4 h-4" />
              Stop Recording
            </>
          ) : (
            <>
              <Mic className="w-4 h-4" />
              Start Recording
            </>
          )}
        </button>
      </div>

      {/* Active Nudges */}
      {nudges.length > 0 && (
        <div className="p-3 border-b border-gray-200 bg-white">
          <h3 className="text-xs font-semibold text-gray-600 uppercase mb-2">
            Active Alerts
          </h3>
          <div className="space-y-2 max-h-40 overflow-y-auto">
            {nudges.map((nudge) => (
              <div
                key={nudge.id}
                className={`${getSeverityColor(nudge.type)} p-2 rounded text-xs`}
              >
                <div className="flex items-start gap-2">
                  {getSeverityIcon(nudge.type)}
                  <p className="flex-1 text-gray-800">{nudge.message}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Live Transcript */}
      <div className="flex-1 overflow-y-auto p-3 bg-white">
        <h3 className="text-xs font-semibold text-gray-600 uppercase mb-2 sticky top-0 bg-white">
          Live Transcript
        </h3>
        {isRecording ? (
          <div className="space-y-2">
            {transcript.length === 0 ? (
              <div className="text-center py-8">
                <Mic className="w-8 h-8 text-gray-300 mx-auto mb-2 animate-pulse" />
                <p className="text-sm text-gray-500">Listening...</p>
              </div>
            ) : (
              transcript.map((segment, idx) => (
                <div key={idx} className="text-xs">
                  <span className="font-semibold text-gray-700">
                    {segment.speaker}:
                  </span>
                  <span className="text-gray-600 ml-1">{segment.text}</span>
                </div>
              ))
            )}
          </div>
        ) : (
          <div className="text-center py-8">
            <MicOff className="w-8 h-8 text-gray-300 mx-auto mb-2" />
            <p className="text-sm text-gray-500">Start recording to begin</p>
          </div>
        )}
      </div>

      {/* Footer */}
      <div className="p-2 bg-gray-50 border-t border-gray-200 text-center">
        <p className="text-xs text-gray-500">
          Privacy-first • Data not stored
        </p>
      </div>
    </div>
  );
}
