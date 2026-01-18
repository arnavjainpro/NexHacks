import { useState } from 'react'
import { Play, Square, Mic, AlertCircle } from 'lucide-react'

const LiveCopilot = () => {
  const [isActive, setIsActive] = useState(false)
  const [product, setProduct] = useState('glucomax')

  const nudges = [
    {
      id: 1,
      severity: 'critical',
      icon: '🛑',
      title: 'Off-label promotion detected',
      message: 'You cannot promote unapproved uses.',
      suggestion:
        'I can only discuss the FDA-approved indication. Would you like to hear about the clinical data for Type 2 Diabetes?',
    },
  ]

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-3xl font-bold text-gray-900">Live Copilot</h2>
        <p className="mt-2 text-gray-600">
          Get real-time guidance during your sales calls
        </p>
      </div>

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
                  Doctor/patient audio is processed in real-time and immediately deleted. 
                  Only your responses are analyzed for compliance.
                </p>
              </div>
            </div>
          </div>

          <button
            onClick={() => setIsActive(true)}
            className="w-full bg-green-600 text-white font-semibold py-3 rounded-lg hover:bg-green-700 transition-colors flex items-center justify-center space-x-2"
          >
            <Play size={20} />
            <span>Go Live</span>
          </button>
        </div>
      ) : (
        /* Active Copilot Screen */
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Main HUD */}
          <div className="lg:col-span-2 space-y-6">
            {/* Live Status */}
            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4">
                  <div className="relative">
                    <div className="w-16 h-16 bg-green-600 rounded-full flex items-center justify-center pulse-critical">
                      <Mic size={28} className="text-white" />
                    </div>
                    <div className="absolute -top-1 -right-1 w-4 h-4 bg-red-500 rounded-full animate-pulse" />
                  </div>
                  <div>
                    <h3 className="text-xl font-bold text-gray-900">
                      Live Session Active
                    </h3>
                    <p className="text-sm text-gray-500">GlucoMax · 00:05:32</p>
                  </div>
                </div>
                <button
                  onClick={() => setIsActive(false)}
                  className="bg-red-100 text-red-700 px-4 py-2 rounded-lg hover:bg-red-200 transition-colors font-medium flex items-center space-x-2"
                >
                  <Square size={18} />
                  <span>End Session</span>
                </button>
              </div>
            </div>

            {/* Live Transcript */}
            <div className="bg-white rounded-lg shadow p-6">
              <h4 className="font-semibold text-gray-900 mb-4">Live Transcript</h4>
              <div className="space-y-4 max-h-96 overflow-y-auto">
                <TranscriptMessage
                  speaker="Doctor"
                  text="Tell me about the efficacy of this medication. How does it compare to what I'm currently prescribing?"
                  timestamp="00:05:12"
                />
                <TranscriptMessage
                  speaker="You"
                  text="In our clinical trials, GlucoMax demonstrated a 1.5% reduction in A1C levels..."
                  timestamp="00:05:18"
                  isRep
                />
              </div>
            </div>

            {/* Session Stats */}
            <div className="bg-white rounded-lg shadow p-6">
              <h4 className="font-semibold text-gray-900 mb-4">Session Stats</h4>
              <div className="grid grid-cols-3 gap-4">
                <StatItem label="Duration" value="5:32" />
                <StatItem label="Nudges" value="1" />
                <StatItem label="Score" value="95" valueColor="text-green-600" />
              </div>
            </div>
          </div>

          {/* Copilot Sidebar */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-lg shadow p-6 sticky top-6">
              <h4 className="font-semibold text-gray-900 mb-4">
                Copilot Guidance
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
                      No guidance needed. You're doing great! 👍
                    </p>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

const TranscriptMessage = ({
  speaker,
  text,
  timestamp,
  isRep = false,
}: {
  speaker: string
  text: string
  timestamp: string
  isRep?: boolean
}) => (
  <div
    className={`p-3 rounded-lg ${
      isRep ? 'bg-blue-50 border border-blue-200' : 'bg-gray-50'
    }`}
  >
    <div className="flex items-baseline justify-between mb-1">
      <span className="text-sm font-medium text-gray-900">{speaker}</span>
      <span className="text-xs text-gray-500">{timestamp}</span>
    </div>
    <p className="text-sm text-gray-700">{text}</p>
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
