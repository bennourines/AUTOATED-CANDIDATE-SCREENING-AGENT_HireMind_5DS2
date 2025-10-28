import { Routes, Route, Link, useLocation } from 'react-router-dom'
import { Home, Briefcase, Users, FileText, Calendar, BarChart3, UserPlus, LayoutDashboard } from 'lucide-react'
import HomePage from './pages/HomePage'
import JobsList from './pages/JobsList'
import JobForm from './pages/JobForm'
import JobDetail from './pages/JobDetail'
import CandidatesList from './pages/CandidatesList'
import CandidateForm from './pages/CandidateForm'
import CandidateDetail from './pages/CandidateDetail'
import CandidateRegistration from './pages/CandidateRegistration'
import ApplicationsList from './pages/ApplicationsList'
import ApplicationForm from './pages/ApplicationForm'
import ApplicationDetail from './pages/ApplicationDetail'
import InterviewsList from './pages/InterviewsList'
import InterviewForm from './pages/InterviewForm'
import InterviewDetail from './pages/InterviewDetail'
import ScoringList from './pages/ScoringList'
import ScoreDetail from './pages/ScoreDetail'
import ManagerDashboard from './pages/ManagerDashboard'

function App() {
  const location = useLocation()

  const navItems = [
    { path: '/', icon: Home, label: 'Home' },
    { path: '/jobs', icon: Briefcase, label: 'Jobs' },
    { path: '/candidates', icon: Users, label: 'Candidates' },
    { path: '/applications', icon: FileText, label: 'Applications' },
    { path: '/interviews', icon: Calendar, label: 'Interviews' },
    { path: '/scoring', icon: BarChart3, label: 'Scoring' },
    { path: '/signup/job-seeker', icon: UserPlus, label: 'Job Seeker Signup' },
    { path: '/dashboard/manager', icon: LayoutDashboard, label: 'Manager Dashboard' },
  ]

  return (
    <div className="flex h-screen bg-gray-50">
      <aside className="w-64 bg-white border-r border-gray-200 flex flex-col">
        <div className="p-6 border-b border-gray-200">
          <h1 className="text-2xl font-bold text-primary">AI-Powered ATS</h1>
          <p className="text-sm text-gray-600 mt-1">Recruitment System</p>
        </div>
        
        <nav className="flex-1 p-4 overflow-y-auto">
          <ul className="space-y-2">
            {navItems.map((item) => {
              const Icon = item.icon
              const isActive = location.pathname === item.path
              
              return (
                <li key={item.path}>
                  <Link
                    to={item.path}
                    className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                      isActive
                        ? 'bg-primary text-white'
                        : 'text-gray-700 hover:bg-gray-100'
                    }`}
                  >
                    <Icon size={20} />
                    <span className="font-medium">{item.label}</span>
                  </Link>
                </li>
              )
            })}
          </ul>
        </nav>

        <div className="p-4 border-t border-gray-200">
          <div className="text-xs text-gray-500">
            Backend: http://127.0.0.1:8000/api/v1
          </div>
        </div>
      </aside>

      <main className="flex-1 overflow-auto">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/jobs" element={<JobsList />} />
          <Route path="/jobs/new" element={<JobForm />} />
          <Route path="/jobs/:id" element={<JobDetail />} />
          <Route path="/candidates" element={<CandidatesList />} />
          <Route path="/candidates/new" element={<CandidateForm />} />
          <Route path="/candidates/:id" element={<CandidateDetail />} />
          <Route path="/signup/job-seeker" element={<CandidateRegistration />} />
          <Route path="/applications" element={<ApplicationsList />} />
          <Route path="/applications/new" element={<ApplicationForm />} />
          <Route path="/applications/:id" element={<ApplicationDetail />} />
          <Route path="/interviews" element={<InterviewsList />} />
          <Route path="/interviews/new" element={<InterviewForm />} />
          <Route path="/interviews/:id" element={<InterviewDetail />} />
          <Route path="/scoring" element={<ScoringList />} />
          <Route path="/scoring/:id" element={<ScoreDetail />} />
          <Route path="/dashboard/manager" element={<ManagerDashboard />} />
        </Routes>
      </main>
    </div>
  )
}

export default App
