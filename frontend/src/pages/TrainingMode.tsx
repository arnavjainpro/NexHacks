import { useState, useEffect, useCallback } from 'react'
import { Play, Square, Volume2, AlertTriangle, Mic, MicOff, Wifi, WifiOff } from 'lucide-react'
import {
  LiveKitRoom,
  RoomAudioRenderer,
  useRoomContext,
  useConnectionState,
  useLocalParticipant,
  useRemoteParticipants,
  useTrackTranscription,
  useTracks,
} from '@livekit/components-react'
import { ConnectionState, Track, RoomEvent, TranscriptionSegment } from 'livekit-client'

// Token server URL - defaults to localhost:8000 (FastAPI server)
const TOKEN_SERVER_URL = import.meta.env.VITE_TOKEN_SERVER_URL || 'http://127.0.0.1:8000'

interface Nudge {
  id: number
  severity: string
  icon: string
  message: string
  suggestion?: string
  timestamp: Date
}

interface TranscriptEntry {
  speaker: string
  text: string
  timestamp: string
  isUser: boolean
}

const TrainingMode = () => {
  const [isActive, setIsActive] = useState(false)
  const [difficulty, setDifficulty] = useState('intermediate')
  const [scenario, setScenario] = useState('off_label_pressure')
  const [token, setToken] = useState<string | null>(null)
  const [wsUrl, setWsUrl] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [isConnecting, setIsConnecting] = useState(false)

  const startSession = async () => {
    setIsConnecting(true)
    setError(null)

    const tokenUrl = `${TOKEN_SERVER_URL}/api/token?mode=training`
    console.log('[TrainingMode] Fetching token from:', tokenUrl)

    try {
      // Step 1: Get token
      const response = await fetch(tokenUrl)
      console.log('[TrainingMode] Response status:', response.status)

      if (!response.ok) {
        const errorText = await response.text()
        console.error('[TrainingMode] Error response:', errorText)
        throw new Error(`Failed to get token: ${response.status} ${errorText}`)
      }

      const data = await response.json()
      console.log('[TrainingMode] Token received for room:', data.room_name)

      // Step 2: Dispatch agent to the same room
      const dispatchUrl = `${TOKEN_SERVER_URL}/api/agent/dispatch?room=${encodeURIComponent(data.room_name)}&mode=training`
      console.log('[TrainingMode] Dispatching agent to:', dispatchUrl)

      const dispatchResponse = await fetch(dispatchUrl, { method: 'POST' })
      const dispatchData = await dispatchResponse.json()
      console.log('[TrainingMode] Agent dispatch response:', dispatchData)

      setToken(data.token)
      setWsUrl(data.url)
      setIsActive(true)
    } catch (err) {
      console.error('[TrainingMode] Error:', err)
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
        <h2 className="text-3xl font-bold text-gray-900">Training Mode</h2>
        <p className="mt-2 text-gray-600">
          Practice with Dr. Doom AI to sharpen your compliance skills
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
            Configure Training Session
          </h3>

          {/* Difficulty Selection */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Difficulty Level
            </label>
            <div className="grid grid-cols-3 gap-3">
              {['beginner', 'intermediate', 'expert'].map((level) => (
                <button
                  key={level}
                  onClick={() => setDifficulty(level)}
                  className={`
                    py-3 px-4 rounded-lg border-2 font-medium capitalize transition-all
                    ${
                      difficulty === level
                        ? 'border-purple-600 bg-purple-50 text-purple-700'
                        : 'border-gray-200 bg-white text-gray-700 hover:border-gray-300'
                    }
                  `}
                >
                  {level}
                </button>
              ))}
            </div>
          </div>

          {/* Scenario Selection */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Training Scenario
            </label>
            <select
              value={scenario}
              onChange={(e) => setScenario(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-600 focus:border-transparent"
            >
              <option value="off_label_pressure">Off-Label Pressure</option>
              <option value="contraindications_quiz">Contraindications Quiz</option>
              <option value="competitive_pressure">Competitive Pressure</option>
              <option value="time_pressure">Time Pressure</option>
            </select>
          </div>

          {/* Voice Notice */}
          <div className="bg-purple-50 border border-purple-200 rounded-lg p-4 mb-6">
            <div className="flex items-start space-x-3">
              <Volume2 size={20} className="text-purple-600 mt-0.5" />
              <div className="text-sm text-purple-900">
                <p className="font-medium mb-1">Voice-Enabled Training</p>
                <p>
                  Dr. Doom will speak to you. Respond naturally using your microphone.
                  The AI uses turn detection so it won't interrupt you.
                </p>
              </div>
            </div>
          </div>

          <button
            onClick={startSession}
            disabled={isConnecting}
            className="w-full bg-purple-600 text-white font-semibold py-3 rounded-lg hover:bg-purple-700 transition-colors flex items-center justify-center space-x-2 disabled:opacity-50"
          >
            {isConnecting ? (
              <>
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white" />
                <span>Connecting to Dr. Doom...</span>
              </>
            ) : (
              <>
                <Play size={20} />
                <span>Start Training</span>
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
          <ActiveTrainingSession
            onEnd={endSession}
            difficulty={difficulty}
            scenario={scenario}
          />
          <RoomAudioRenderer />
        </LiveKitRoom>
      ) : null}
    </div>
  )
}

// Active training session component
const ActiveTrainingSession = ({
  onEnd,
  difficulty,
  scenario,
}: {
  onEnd: () => void
  difficulty: string
  scenario: string
}) => {
  const [nudges, setNudges] = useState<Nudge[]>([])
  const [transcript, setTranscript] = useState<TranscriptEntry[]>([])
  const [sessionDuration, setSessionDuration] = useState(0)
  const [sessionStart] = useState(Date.now())
  const [exchanges, setExchanges] = useState(0)
  const [agentSpeaking, setAgentSpeaking] = useState(false)
  const [lastAgentText, setLastAgentText] = useState('')

  const connectionState = useConnectionState()
  const { localParticipant } = useLocalParticipant()
  const remoteParticipants = useRemoteParticipants()
  const room = useRoomContext()

  // Find the agent participant
  const agentParticipant = remoteParticipants.find(
    (p) => p.identity.includes('agent') || p.name?.includes('Dr. Doom')
  )

  // Track agent audio for speaking indicator
  const tracks = useTracks([Track.Source.Microphone], { onlySubscribed: true })
  const agentAudioTrack = tracks.find(
    (t) => t.participant.identity === agentParticipant?.identity
  )

  // Update session duration
  useEffect(() => {
    const interval = setInterval(() => {
      setSessionDuration(Math.floor((Date.now() - sessionStart) / 1000))
    }, 1000)
    return () => clearInterval(interval)
  }, [sessionStart])

  // Listen for transcription events
  useEffect(() => {
    if (!room) return

    const handleTranscription = (
      segments: TranscriptionSegment[],
      participant: any
    ) => {
      segments.forEach((segment) => {
        if (segment.final && segment.text.trim()) {
          const isAgent = participant.identity.includes('agent') || participant.identity !== localParticipant?.identity

          setTranscript((prev) => [
            ...prev,
            {
              speaker: isAgent ? 'Dr. Doom' : 'You',
              text: segment.text,
              timestamp: formatTime(sessionDuration),
              isUser: !isAgent,
            },
          ].slice(-30))

          if (isAgent) {
            setLastAgentText(segment.text)
            setExchanges((e) => e + 1)

            // Check for compliance feedback in agent's response
            checkForComplianceFeedback(segment.text)
          }
        }
      })
    }

    room.on(RoomEvent.TranscriptionReceived, handleTranscription)
    return () => {
      room.off(RoomEvent.TranscriptionReceived, handleTranscription)
    }
  }, [room, localParticipant, sessionDuration])

  // Track when agent is speaking
  useEffect(() => {
    if (agentAudioTrack?.track) {
      const checkSpeaking = () => {
        // This is a simplified check - in production you'd use audio levels
        setAgentSpeaking(agentAudioTrack.track?.isMuted === false)
      }
      const interval = setInterval(checkSpeaking, 100)
      return () => clearInterval(interval)
    }
  }, [agentAudioTrack])

  const checkForComplianceFeedback = (text: string) => {
    const textLower = text.toLowerCase()

    // Check for skeptical/warning responses from Dr. Doom
    const warningPhrases = [
      'guarantee',
      'off-label',
      'unapproved',
      'clinical trial',
      'evidence',
      'prove',
      'skeptical',
      'heard that before',
      'show me data',
    ]

    for (const phrase of warningPhrases) {
      if (textLower.includes(phrase)) {
        const newNudge: Nudge = {
          id: Date.now(),
          severity: 'warning',
          icon: '⚠️',
          message: `Dr. Doom is challenging you on "${phrase}"`,
          suggestion: 'Stick to FDA-approved claims and cite specific clinical trial data.',
          timestamp: new Date(),
        }
        setNudges((prev) => [newNudge, ...prev].slice(0, 5))
        break
      }
    }
  }

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
  }

  const toggleMicrophone = async () => {
    if (localParticipant) {
      await localParticipant.setMicrophoneEnabled(!localParticipant.isMicrophoneEnabled)
    }
  }

  const isConnected = connectionState === ConnectionState.Connected
  const isMicEnabled = localParticipant?.isMicrophoneEnabled

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      {/* Main Training Area */}
      <div className="lg:col-span-2 space-y-6">
        {/* AI Doctor Card */}
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center space-x-3">
              <div
                className={`w-12 h-12 bg-gradient-to-br from-purple-600 to-indigo-700 rounded-full flex items-center justify-center ${
                  agentSpeaking ? 'ring-4 ring-purple-300 animate-pulse' : ''
                }`}
              >
                <span className="text-white font-bold text-lg">DD</span>
              </div>
              <div>
                <div className="flex items-center space-x-2">
                  <h3 className="font-semibold text-gray-900">Dr. Doom</h3>
                  {isConnected ? (
                    <Wifi size={16} className="text-green-600" />
                  ) : (
                    <WifiOff size={16} className="text-gray-400" />
                  )}
                </div>
                <p className="text-sm text-gray-500">
                  Skeptical · {difficulty.charAt(0).toUpperCase() + difficulty.slice(1)} Level
                </p>
              </div>
            </div>
            <button
              onClick={onEnd}
              className="bg-red-100 text-red-700 p-2 rounded-lg hover:bg-red-200 transition-colors"
            >
              <Square size={20} />
            </button>
          </div>

          {/* AI Doctor Speech */}
          <div className="bg-gray-50 rounded-lg p-4 mb-4 min-h-[80px]">
            <div className="flex items-start space-x-3">
              <Volume2
                size={20}
                className={`mt-1 ${agentSpeaking ? 'text-purple-600 animate-pulse' : 'text-gray-400'}`}
              />
              <p className="text-gray-700 italic">
                {lastAgentText || (
                  isConnected
                    ? 'Dr. Doom is preparing to speak...'
                    : 'Connecting to Dr. Doom...'
                )}
              </p>
            </div>
          </div>

          {/* Microphone Control */}
          <div className="flex items-center justify-between p-4 bg-purple-50 rounded-lg">
            <div className="flex items-center space-x-3">
              <button
                onClick={toggleMicrophone}
                className={`p-3 rounded-full transition-colors ${
                  isMicEnabled
                    ? 'bg-purple-600 text-white'
                    : 'bg-gray-300 text-gray-600'
                }`}
              >
                {isMicEnabled ? <Mic size={24} /> : <MicOff size={24} />}
              </button>
              <div>
                <p className="font-medium text-gray-900">
                  {isMicEnabled ? 'Microphone Active' : 'Microphone Muted'}
                </p>
                <p className="text-sm text-gray-500">
                  {isMicEnabled
                    ? 'Speak naturally - Dr. Doom is listening'
                    : 'Click to enable your microphone'}
                </p>
              </div>
            </div>
            <div
              className={`w-3 h-3 rounded-full ${
                isMicEnabled ? 'bg-green-500 animate-pulse' : 'bg-gray-400'
              }`}
            />
          </div>
        </div>

        {/* Conversation Transcript */}
        <div className="bg-white rounded-lg shadow p-6">
          <h4 className="font-semibold text-gray-900 mb-4">Conversation</h4>
          <div className="space-y-3 max-h-64 overflow-y-auto">
            {transcript.length === 0 ? (
              <div className="text-center py-8 text-gray-500">
                <Volume2 size={32} className="mx-auto mb-2 opacity-50" />
                <p>Waiting for conversation to begin...</p>
              </div>
            ) : (
              transcript.map((entry, idx) => (
                <div
                  key={idx}
                  className={`p-3 rounded-lg ${
                    entry.isUser
                      ? 'bg-purple-50 border border-purple-200 ml-8'
                      : 'bg-gray-50 mr-8'
                  }`}
                >
                  <div className="flex items-baseline justify-between mb-1">
                    <span className="text-sm font-medium text-gray-900">
                      {entry.speaker}
                    </span>
                    <span className="text-xs text-gray-500">{entry.timestamp}</span>
                  </div>
                  <p className="text-sm text-gray-700">{entry.text}</p>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Session Progress */}
        <div className="bg-white rounded-lg shadow p-6">
          <h4 className="font-semibold text-gray-900 mb-4">Session Progress</h4>
          <div className="grid grid-cols-4 gap-4">
            <div>
              <p className="text-xs text-gray-600 mb-1">Duration</p>
              <p className="text-xl font-bold text-gray-900">{formatTime(sessionDuration)}</p>
            </div>
            <div>
              <p className="text-xs text-gray-600 mb-1">Exchanges</p>
              <p className="text-xl font-bold text-gray-900">{exchanges}</p>
            </div>
            <div>
              <p className="text-xs text-gray-600 mb-1">Warnings</p>
              <p className="text-xl font-bold text-orange-600">{nudges.length}</p>
            </div>
            <div>
              <p className="text-xs text-gray-600 mb-1">Status</p>
              <p className="text-xl font-bold text-green-600">
                {isConnected ? 'Active' : 'Connecting'}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Coach's Sidebar */}
      <div className="lg:col-span-1">
        <div className="bg-white rounded-lg shadow p-6 sticky top-6">
          <h4 className="font-semibold text-gray-900 mb-4 flex items-center space-x-2">
            <AlertTriangle size={20} className="text-purple-600" />
            <span>Coach's Feedback</span>
          </h4>

          <div className="space-y-4">
            {nudges.length === 0 ? (
              <div className="text-center py-8">
                <p className="text-gray-500 text-sm">
                  No feedback yet. Keep practicing!
                </p>
              </div>
            ) : (
              nudges.map((nudge) => (
                <div
                  key={nudge.id}
                  className={`
                    p-4 rounded-lg border-l-4 nudge-enter
                    ${
                      nudge.severity === 'critical'
                        ? 'bg-red-50 border-red-500'
                        : nudge.severity === 'warning'
                        ? 'bg-orange-50 border-orange-500'
                        : 'bg-blue-50 border-blue-500'
                    }
                  `}
                >
                  <div className="flex items-start space-x-2">
                    <span className="text-2xl">{nudge.icon}</span>
                    <div className="flex-1">
                      <p className="text-sm font-medium text-gray-900 mb-1">
                        {nudge.message}
                      </p>
                      {nudge.suggestion && (
                        <p className="text-xs text-gray-600 italic">
                          Try: "{nudge.suggestion}"
                        </p>
                      )}
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>

          {/* Tips Section */}
          <div className="mt-6 pt-6 border-t border-gray-200">
            <h5 className="font-medium text-gray-900 mb-3">Quick Tips</h5>
            <ul className="space-y-2 text-sm text-gray-600">
              <li className="flex items-start space-x-2">
                <span className="text-purple-600">•</span>
                <span>Stick to FDA-approved indications</span>
              </li>
              <li className="flex items-start space-x-2">
                <span className="text-purple-600">•</span>
                <span>Cite specific clinical trial data</span>
              </li>
              <li className="flex items-start space-x-2">
                <span className="text-purple-600">•</span>
                <span>Avoid absolute claims like "guarantee"</span>
              </li>
              <li className="flex items-start space-x-2">
                <span className="text-purple-600">•</span>
                <span>Redirect off-label questions politely</span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}

export default TrainingMode
