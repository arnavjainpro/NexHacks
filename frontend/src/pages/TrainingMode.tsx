import { useState } from 'react'
import { Play, Square, Volume2, AlertTriangle } from 'lucide-react'

const TrainingMode = () => {
  const [isActive, setIsActive] = useState(false)
  const [difficulty, setDifficulty] = useState('intermediate')
  const [scenario, setScenario] = useState('off_label_pressure')

  const nudges = [
    {
      id: 1,
      severity: 'warning',
      icon: '⚠️',
      message: 'Be careful - this sounds like implied off-label use.',
      suggestion: 'I can only speak to our FDA-approved indication.',
    },
    {
      id: 2,
      severity: 'info',
      icon: '💡',
      message: 'You sound uncertain. Pivot to clinical data.',
      suggestion: 'In clinical trials, 78% of patients achieved target A1C.',
    },
  ]

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-3xl font-bold text-gray-900">Training Mode</h2>
        <p className="mt-2 text-gray-600">
          Practice with Dr. Doom AI to sharpen your compliance skills
        </p>
      </div>

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

          <button
            onClick={() => setIsActive(true)}
            className="w-full bg-purple-600 text-white font-semibold py-3 rounded-lg hover:bg-purple-700 transition-colors flex items-center justify-center space-x-2"
          >
            <Play size={20} />
            <span>Start Training</span>
          </button>
        </div>
      ) : (
        /* Active Training Screen */
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Main Training Area */}
          <div className="lg:col-span-2 space-y-6">
            {/* AI Doctor Card */}
            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center space-x-3">
                  <div className="w-12 h-12 bg-gradient-to-br from-purple-600 to-indigo-700 rounded-full flex items-center justify-center">
                    <span className="text-white font-bold text-lg">DD</span>
                  </div>
                  <div>
                    <h3 className="font-semibold text-gray-900">Dr. Doom</h3>
                    <p className="text-sm text-gray-500">Skeptical · Expert Level</p>
                  </div>
                </div>
                <button
                  onClick={() => setIsActive(false)}
                  className="bg-red-100 text-red-700 p-2 rounded-lg hover:bg-red-200 transition-colors"
                >
                  <Square size={20} />
                </button>
              </div>

              {/* AI Doctor Speech */}
              <div className="bg-gray-50 rounded-lg p-4 mb-4">
                <div className="flex items-start space-x-3">
                  <Volume2 size={20} className="text-gray-400 mt-1" />
                  <p className="text-gray-700 italic">
                    "I've heard these claims before. What's different about your drug? And 
                    I have patients who could benefit from this for weight loss. Can you 
                    help with that?"
                  </p>
                </div>
              </div>

              {/* Your Response Input */}
              <div className="space-y-3">
                <label className="block text-sm font-medium text-gray-700">
                  Your Response
                </label>
                <textarea
                  placeholder="Start speaking or type your response..."
                  rows={4}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-600 focus:border-transparent"
                />
                <div className="flex space-x-3">
                  <button className="flex-1 bg-purple-600 text-white font-medium py-2 rounded-lg hover:bg-purple-700 transition-colors">
                    Send Response
                  </button>
                  <button className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
                    🎤 Voice
                  </button>
                </div>
              </div>
            </div>

            {/* Session Progress */}
            <div className="bg-white rounded-lg shadow p-6">
              <h4 className="font-semibold text-gray-900 mb-4">Session Progress</h4>
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">Duration</span>
                  <span className="font-medium text-gray-900">3:45</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">Exchanges</span>
                  <span className="font-medium text-gray-900">7</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">Warnings</span>
                  <span className="font-medium text-orange-600">2</span>
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
                {nudges.map((nudge) => (
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
                ))}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default TrainingMode
