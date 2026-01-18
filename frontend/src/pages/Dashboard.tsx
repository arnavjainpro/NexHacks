import { Link } from 'react-router-dom'
import { Brain, Headphones, TrendingUp, Target } from 'lucide-react'

const Dashboard = () => {
  return (
    <div className="space-y-8">
      {/* Welcome Section */}
      <div>
        <h2 className="text-3xl font-bold text-gray-900">Welcome back, John!</h2>
        <p className="mt-2 text-gray-600">
          Ready to train or start a live session? Your compliance score has improved by 12% this month.
        </p>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          icon={<Target className="text-blue-600" />}
          title="Compliance Score"
          value="87.5"
          change="+12%"
          changeType="positive"
        />
        <StatCard
          icon={<Brain className="text-purple-600" />}
          title="Training Sessions"
          value="23"
          change="+5"
          changeType="positive"
        />
        <StatCard
          icon={<Headphones className="text-green-600" />}
          title="Live Sessions"
          value="19"
          change="+3"
          changeType="positive"
        />
        <StatCard
          icon={<TrendingUp className="text-orange-600" />}
          title="Violations Prevented"
          value="142"
          change="-8%"
          changeType="positive"
        />
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <ActionCard
          title="Floating Widget"
          description="Launch compact overlay for Zoom/Meet calls"
          icon={<Headphones size={32} className="text-blue-600" />}
          buttonText="Open Widget"
          buttonLink="/widget"
          gradient="from-blue-50 to-blue-100"
        />
        <ActionCard
          title="Start Training Session"
          description="Practice with Dr. Doom AI to improve your compliance skills"
          icon={<Brain size={32} className="text-purple-600" />}
          buttonText="Enter Training"
          buttonLink="/training"
          gradient="from-purple-50 to-purple-100"
        />
        <ActionCard
          title="Full Copilot Mode"
          description="Full-screen copilot with detailed analytics"
          icon={<Headphones size={32} className="text-green-600" />}
          buttonText="Go Live"
          buttonLink="/copilot"
          gradient="from-green-50 to-green-100"
        />
      </div>

      {/* Recent Activity */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Sessions</h3>
        <div className="space-y-4">
          <SessionItem
            type="Training"
            score={92}
            date="2 hours ago"
            duration="18 min"
          />
          <SessionItem
            type="Live"
            score={85}
            date="Yesterday"
            duration="45 min"
          />
          <SessionItem
            type="Training"
            score={88}
            date="2 days ago"
            duration="22 min"
          />
        </div>
      </div>
    </div>
  )
}

const StatCard = ({
  icon,
  title,
  value,
  change,
  changeType,
}: {
  icon: React.ReactNode
  title: string
  value: string
  change: string
  changeType: 'positive' | 'negative'
}) => (
  <div className="bg-white rounded-lg shadow p-6">
    <div className="flex items-center justify-between">
      <div>{icon}</div>
      <span
        className={`text-sm font-medium ${
          changeType === 'positive' ? 'text-green-600' : 'text-red-600'
        }`}
      >
        {change}
      </span>
    </div>
    <div className="mt-4">
      <h3 className="text-sm font-medium text-gray-600">{title}</h3>
      <p className="text-3xl font-bold text-gray-900 mt-1">{value}</p>
    </div>
  </div>
)

const ActionCard = ({
  title,
  description,
  icon,
  buttonText,
  buttonLink,
  gradient,
}: {
  title: string
  description: string
  icon: React.ReactNode
  buttonText: string
  buttonLink: string
  gradient: string
}) => (
  <div className={`bg-gradient-to-br ${gradient} rounded-lg shadow p-6`}>
    <div className="mb-4">{icon}</div>
    <h3 className="text-xl font-bold text-gray-900 mb-2">{title}</h3>
    <p className="text-gray-600 mb-4">{description}</p>
    <Link
      to={buttonLink}
      className="inline-block bg-white text-gray-900 font-medium px-6 py-2 rounded-lg hover:bg-gray-50 transition-colors"
    >
      {buttonText}
    </Link>
  </div>
)

const SessionItem = ({
  type,
  score,
  date,
  duration,
}: {
  type: string
  score: number
  date: string
  duration: string
}) => (
  <div className="flex items-center justify-between py-3 border-b border-gray-100 last:border-0">
    <div className="flex items-center space-x-3">
      <div
        className={`w-10 h-10 rounded-lg flex items-center justify-center ${
          type === 'Training' ? 'bg-purple-100' : 'bg-green-100'
        }`}
      >
        {type === 'Training' ? (
          <Brain size={20} className="text-purple-600" />
        ) : (
          <Headphones size={20} className="text-green-600" />
        )}
      </div>
      <div>
        <p className="font-medium text-gray-900">{type} Session</p>
        <p className="text-sm text-gray-500">{date} · {duration}</p>
      </div>
    </div>
    <div className="text-right">
      <p className="text-lg font-bold text-gray-900">{score}</p>
      <p className="text-xs text-gray-500">Score</p>
    </div>
  </div>
)

export default Dashboard
