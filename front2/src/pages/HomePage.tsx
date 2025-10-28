import { Link } from 'react-router-dom'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Briefcase, Users, FileText, Calendar, BarChart3, Brain, Zap, Target } from 'lucide-react'

export default function HomePage() {
  const features = [
    {
      icon: Brain,
      title: 'AI-Powered Screening',
      description: 'Automated candidate screening using free open-source AI models',
      color: 'text-blue-600',
      bgColor: 'bg-blue-50',
    },
    {
      icon: Zap,
      title: 'Automated Scoring',
      description: 'AI-driven candidate scoring and ranking with fit analysis',
      color: 'text-purple-600',
      bgColor: 'bg-purple-50',
    },
    {
      icon: Target,
      title: 'Interview Simulator',
      description: 'Practice interviews with AI-powered mock interview sessions',
      color: 'text-green-600',
      bgColor: 'bg-green-50',
    },
  ]

  const quickLinks = [
    { icon: Briefcase, title: 'Jobs', path: '/jobs', description: 'Manage job postings', color: 'bg-blue-500' },
    { icon: Users, title: 'Candidates', path: '/candidates', description: 'View all candidates', color: 'bg-green-500' },
    { icon: FileText, title: 'Applications', path: '/applications', description: 'Review applications', color: 'bg-purple-500' },
    { icon: Calendar, title: 'Interviews', path: '/interviews', description: 'Schedule interviews', color: 'bg-orange-500' },
    { icon: BarChart3, title: 'Scoring', path: '/scoring', description: 'View AI scores', color: 'bg-pink-500' },
  ]

  return (
    <div className="p-8">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">AI-Powered ATS Dashboard</h1>
          <p className="text-lg text-gray-600">
            Streamline your recruitment process with free open-source AI models
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          {features.map((feature) => {
            const Icon = feature.icon
            return (
              <Card key={feature.title} className="border-2 hover:shadow-lg transition-shadow">
                <CardHeader>
                  <div className={`w-12 h-12 ${feature.bgColor} rounded-lg flex items-center justify-center mb-4`}>
                    <Icon className={`w-6 h-6 ${feature.color}`} />
                  </div>
                  <CardTitle className="text-xl">{feature.title}</CardTitle>
                  <CardDescription>{feature.description}</CardDescription>
                </CardHeader>
              </Card>
            )
          })}
        </div>

        <div className="mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Quick Links</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {quickLinks.map((link) => {
              const Icon = link.icon
              return (
                <Link key={link.path} to={link.path}>
                  <Card className="hover:shadow-lg transition-shadow cursor-pointer h-full">
                    <CardContent className="p-6">
                      <div className="flex items-start gap-4">
                        <div className={`w-12 h-12 ${link.color} rounded-lg flex items-center justify-center flex-shrink-0`}>
                          <Icon className="w-6 h-6 text-white" />
                        </div>
                        <div>
                          <h3 className="text-lg font-semibold text-gray-900 mb-1">{link.title}</h3>
                          <p className="text-sm text-gray-600">{link.description}</p>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                </Link>
              )
            })}
          </div>
        </div>

        <Card className="bg-gradient-to-r from-blue-50 to-purple-50 border-2">
          <CardHeader>
            <CardTitle className="text-2xl">AI Models Information</CardTitle>
            <CardDescription className="text-base">
              This ATS uses free and open-source AI models for all functionality
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="bg-white p-4 rounded-lg">
                <h4 className="font-semibold text-gray-900 mb-2">Resume Screening</h4>
                <p className="text-sm text-gray-600">Uses transformer-based models for resume parsing and skills extraction</p>
              </div>
              <div className="bg-white p-4 rounded-lg">
                <h4 className="font-semibold text-gray-900 mb-2">Candidate Scoring</h4>
                <p className="text-sm text-gray-600">AI-powered fit analysis with technical and cultural scoring</p>
              </div>
              <div className="bg-white p-4 rounded-lg">
                <h4 className="font-semibold text-gray-900 mb-2">Interview Simulation</h4>
                <p className="text-sm text-gray-600">Practice interviews with AI-generated questions and feedback</p>
              </div>
              <div className="bg-white p-4 rounded-lg">
                <h4 className="font-semibold text-gray-900 mb-2">Decision Support</h4>
                <p className="text-sm text-gray-600">AI recommendations for hiring decisions based on multiple factors</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
