import { Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import TrainingMode from './pages/TrainingMode'
import LiveCopilot from './pages/LiveCopilot'
import Analytics from './pages/Analytics'
import Profile from './pages/Profile'

function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Dashboard />} />
        <Route path="training" element={<TrainingMode />} />
        <Route path="copilot" element={<LiveCopilot />} />
        <Route path="analytics" element={<Analytics />} />
        <Route path="profile" element={<Profile />} />
      </Route>
    </Routes>
  )
}

export default App
