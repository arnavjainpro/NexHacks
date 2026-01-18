import { useState, useEffect, useCallback } from 'react'
import { Play, Square, Mic, AlertCircle, Wifi, WifiOff, Volume2 } from 'lucide-react'
import {
  LiveKitRoom,
  RoomAudioRenderer,
  useRoomContext,
  useDataChannel,
  useConnectionState,
  useLocalParticipant,
} from '@livekit/components-react'
import { ConnectionState, RoomEvent } from 'livekit-client'

// Token server URL - defaults to localhost:8000 (FastAPI server)
const TOKEN_SERVER_URL = import.meta.env.VITE_TOKEN_SERVER_URL || 'http://127.0.0.1:8000'

interface ComplianceViolation {
  type: string
  violation: {
    keyword: string
    severity: string
    suggestion: string
  }
  context: string
  is_final: boolean
  timestamp: number
}

interface Nudge {
  id: number
  severity: string
  icon: string
  title: string
  message: string
  suggestion: string
  timestamp: Date
}

const LiveCopilot = () => {
  const [isActive, setIsActive] = useState(false)
  const [product, setProduct] = useState('glucomax')
  const [token, setToken] = useState<string | null>(null)
  const [wsUrl, setWsUrl] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [isConnecting, setIsConnecting] = useState(false)

  const startSession = async () => {
    setIsConnecting(true)
    setError(null)

    const tokenUrl = `${TOKEN_SERVER_URL}/api/token?mode=live`
    console.log('[LiveCopilot] Fetching token from:', tokenUrl)

    try {
      // Step 1: Get token
      const response = await fetch(tokenUrl)
      console.log('[LiveCopilot] Response status:', response.status)

      if (!response.ok) {
        const errorText = await response.text()
        console.error('[LiveCopilot] Error response:', errorText)
        throw new Error(`Failed to get token: ${response.status} ${errorText}`)
      }

      const data = await response.json()
      console.log('[LiveCopilot] Token received for room:', data.room_name)

      // Step 2: Dispatch agent to the same room
      const dispatchUrl = `${TOKEN_SERVER_URL}/api/agent/dispatch?room=${encodeURIComponent(data.room_name)}&mode=live`
      console.log('[LiveCopilot] Dispatching agent to:', dispatchUrl)

      const dispatchResponse = await fetch(dispatchUrl, { method: 'POST' })
      const dispatchData = await dispatchResponse.json()
      console.log('[LiveCopilot] Agent dispatch response:', dispatchData)

      setToken(data.token)
      setWsUrl(data.url)
      setIsActive(true)
    } catch (err) {
      console.error('[LiveCopilot] Error:', err)
      const message = err instanceof Error ? err.message : 'Failed to connect'
      setError(`${message}. Make sure the backend server is running on ${TOKEN_SERVER_URL}`)
    } finally {
      setIsConnecting(false)
    }
  }

  const endSession = () => {
    setIsActive(false)
    setToken(null)
    setWsUrl(null)
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-3xl font-bold text-gray-900">Live Copilot</h2>
        <p className="mt-2 text-gray-600">
          Get real-time compliance guidance during your sales calls
        </p>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-red-700">{error}</p>
        </div>
      )}

      {!isActive ? (
        /* Setup Screen */
        <div className="bg-white rounded-lg shadow p-6 max-w-2xl">
          <h3 className="text-xl font-semibold text-gray-900 mb-6">
            Start Live Session
          </h3>

          {/* Product Selection */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Product Focus
            </label>
            <select
              value={product}
              onChange={(e) => setProduct(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-600 focus:border-transparent"
            >
              <option value="glucomax">GlucoMax - Type 2 Diabetes</option>
              <option value="cardioguard">CardioGuard - Hypertension</option>
            </select>
          </div>

          {/* Privacy Notice */}
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
            <div className="flex items-start space-x-3">
              <AlertCircle size={20} className="text-blue-600 mt-0.5" />
              <div className="text-sm text-blue-900">
                <p className="font-medium mb-1">Privacy-First Architecture</p>
                <p>
                  Audio is processed in real-time and immediately deleted.
                  The AI agent silently monitors for compliance keywords and alerts you instantly.
                </p>
              </div>
            </div>
          </div>

          <button
            onClick={startSession}
            disabled={isConnecting}
            className="w-full bg-green-600 text-white font-semibold py-3 rounded-lg hover:bg-green-700 transition-colors flex items-center justify-center space-x-2 disabled:opacity-50"
          >
            {isConnecting ? (
              <>
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white" />
                <span>Connecting...</span>
              </>
            ) : (
              <>
                <Play size={20} />
                <span>Go Live</span>
              </>
            )}
          </button>
        </div>
      ) : token && wsUrl ? (
        <LiveKitRoom
          token={token}
          serverUrl={wsUrl}
          connect={true}
          audio={true}
          video={false}
          onDisconnected={endSession}
        >
          <ActiveLiveSession onEnd={endSession} product={product} />
          <RoomAudioRenderer />
        </LiveKitRoom>
      ) : null}
    </div>
  )
}

// Active session component that uses LiveKit hooks
const ActiveLiveSession = ({
  onEnd,
  product,
}: {
  onEnd: () => void
  product: string
}) => {
  const [nudges, setNudges] = useState<Nudge[]>([])
  const [transcript, setTranscript] = useState<{ speaker: string; text: string; timestamp: string }[]>([])
  const [sessionDuration, setSessionDuration] = useState(0)
  const [sessionStart] = useState(Date.now())

  const connectionState = useConnectionState()
  const { localParticipant } = useLocalParticipant()
  const room = useRoomContext()

  // Update session duration
  useEffect(() => {
    const interval = setInterval(() => {
      setSessionDuration(Math.floor((Date.now() - sessionStart) / 1000))
    }, 1000)
    return () => clearInterval(interval)
  }, [sessionStart])

  // Listen for data packets (compliance alerts)
  const onDataReceived = useCallback((payload: Uint8Array) => {
    try {
      const decoder = new TextDecoder()
      const data: ComplianceViolation = JSON.parse(decoder.decode(payload))

      if (data.type === 'compliance_violation') {
        const newNudge: Nudge = {
          id: Date.now(),
          severity: data.violation.severity === 'critical' ? 'critical' : 'warning',
          icon: data.violation.severity === 'critical' ? '🛑' : '⚠️',
          title: `${data.violation.keyword.toUpperCase()} detected`,
          message: `Compliance keyword detected in your speech.`,
          suggestion: data.violation.suggestion,
          timestamp: new Date(),
        }
        setNudges((prev) => [newNudge, ...prev].slice(0, 10))

        // Add to transcript
        setTranscript((prev) => [
          ...prev,
          {
            speaker: 'Alert',
            text: `Detected: "${data.violation.keyword}" - ${data.context}`,
            timestamp: formatTime(sessionDuration),
          },
        ].slice(-20))
      }
    } catch (err) {
      console.error('Failed to parse data packet:', err)
    }
  }, [sessionDuration])

  // Subscribe to data channel
  useEffect(() => {
    if (room) {
      room.on(RoomEvent.DataReceived, onDataReceived)
      return () => {
        room.off(RoomEvent.DataReceived, onDataReceived)
      }
    }
  }, [room, onDataReceived])

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
  }

  const isConnected = connectionState === ConnectionState.Connected
  const isMicEnabled = localParticipant?.isMicrophoneEnabled

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      {/* Main HUD */}
      <div className="lg:col-span-2 space-y-6">
        {/* Live Status */}
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="relative">
                <div
                  className={`w-16 h-16 rounded-full flex items-center justify-center ${
                    isConnected ? 'bg-green-600 pulse-critical' : 'bg-gray-400'
                  }`}
                >
                  <Mic size={28} className="text-white" />
                </div>
                {isConnected && (
                  <div className="absolute -top-1 -right-1 w-4 h-4 bg-red-500 rounded-full animate-pulse" />
                )}
              </div>
              <div>
                <div className="flex items-center space-x-2">
                  <h3 className="text-xl font-bold text-gray-900">
                    {isConnected ? 'Live Session Active' : 'Connecting...'}
                  </h3>
                  {isConnected ? (
                    <Wifi size={20} className="text-green-600" />
                  ) : (
                    <WifiOff size={20} className="text-gray-400" />
                  )}
                </div>
                <p className="text-sm text-gray-500">
                  {product === 'glucomax' ? 'GlucoMax' : 'CardioGuard'} · {formatTime(sessionDuration)}
                </p>
                <p className="text-xs text-gray-400">
                  {isMicEnabled ? 'Microphone active - Agent is listening' : 'Microphone muted'}
                </p>
              </div>
            </div>
            <button
              onClick={onEnd}
              className="bg-red-100 text-red-700 px-4 py-2 rounded-lg hover:bg-red-200 transition-colors font-medium flex items-center space-x-2"
            >
              <Square size={18} />
              <span>End Session</span>
            </button>
          </div>
        </div>

        {/* Live Transcript / Activity Log */}
        <div className="bg-white rounded-lg shadow p-6">
          <h4 className="font-semibold text-gray-900 mb-4">Activity Log</h4>
          <div className="space-y-4 max-h-96 overflow-y-auto">
            {transcript.length === 0 ? (
              <div className="text-center py-8 text-gray-500">
                <Volume2 size={32} className="mx-auto mb-2 opacity-50" />
                <p>Speak naturally. The agent is silently monitoring for compliance keywords.</p>
              </div>
            ) : (
              transcript.map((msg, idx) => (
                <TranscriptMessage
                  key={idx}
                  speaker={msg.speaker}
                  text={msg.text}
                  timestamp={msg.timestamp}
                  isAlert={msg.speaker === 'Alert'}
                />
              ))
            )}
          </div>
        </div>

        {/* Session Stats */}
        <div className="bg-white rounded-lg shadow p-6">
          <h4 className="font-semibold text-gray-900 mb-4">Session Stats</h4>
          <div className="grid grid-cols-3 gap-4">
            <StatItem label="Duration" value={formatTime(sessionDuration)} />
            <StatItem label="Alerts" value={nudges.length.toString()} />
            <StatItem
              label="Score"
              value={Math.max(0, 100 - nudges.length * 10).toString()}
              valueColor={nudges.length > 5 ? 'text-red-600' : 'text-green-600'}
            />
          </div>
        </div>
      </div>

      {/* Copilot Sidebar */}
      <div className="lg:col-span-1">
        <div className="bg-white rounded-lg shadow p-6 sticky top-6">
          <h4 className="font-semibold text-gray-900 mb-4">
            Compliance Alerts
          </h4>

          <div className="space-y-4">
            {nudges.map((nudge) => (
              <div
                key={nudge.id}
                className={`
                  p-4 rounded-lg border-l-4 nudge-enter
                  ${
                    nudge.severity === 'critical'
                      ? 'bg-red-50 border-red-500 pulse-critical'
                      : nudge.severity === 'warning'
                      ? 'bg-orange-50 border-orange-500'
                      : 'bg-blue-50 border-blue-500'
                  }
                `}
              >
                <div className="flex items-start space-x-2">
                  <span className="text-2xl">{nudge.icon}</span>
                  <div className="flex-1">
                    <p className="text-sm font-bold text-gray-900 mb-1">
                      {nudge.title}
                    </p>
                    <p className="text-xs text-gray-700 mb-2">{nudge.message}</p>
                    {nudge.suggestion && (
                      <div className="bg-white rounded p-2 border border-gray-200">
                        <p className="text-xs font-medium text-gray-600 mb-1">
                          Say this instead:
                        </p>
                        <p className="text-xs text-gray-900 italic">
                          "{nudge.suggestion}"
                        </p>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            ))}

            {nudges.length === 0 && (
              <div className="text-center py-8">
                <p className="text-gray-500 text-sm">
                  No compliance issues detected. Keep it up!
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

const TranscriptMessage = ({
  speaker,
  text,
  timestamp,
  isAlert = false,
}: {
  speaker: string
  text: string
  timestamp: string
  isAlert?: boolean
}) => (
  <div
    className={`p-3 rounded-lg ${
      isAlert ? 'bg-red-50 border border-red-200' : 'bg-gray-50'
    }`}
  >
    <div className="flex items-baseline justify-between mb-1">
      <span className={`text-sm font-medium ${isAlert ? 'text-red-700' : 'text-gray-900'}`}>
        {speaker}
      </span>
      <span className="text-xs text-gray-500">{timestamp}</span>
    </div>
    <p className={`text-sm ${isAlert ? 'text-red-600' : 'text-gray-700'}`}>{text}</p>
  </div>
)

const StatItem = ({
  label,
  value,
  valueColor = 'text-gray-900',
}: {
  label: string
  value: string
  valueColor?: string
}) => (
  <div>
    <p className="text-xs text-gray-600 mb-1">{label}</p>
    <p className={`text-2xl font-bold ${valueColor}`}>{value}</p>
  </div>
)

export default LiveCopilot
