import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { api, Candidate } from '@/api'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Plus, ExternalLink, Users } from 'lucide-react'

export default function CandidatesList() {
  const [candidates, setCandidates] = useState<Candidate[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchCandidates()
  }, [])

  const fetchCandidates = async () => {
    try {
      setLoading(true)
      const response = await api.get('/candidates')
      setCandidates(response.data)
      setError(null)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to fetch candidates. Make sure the backend endpoint is available.')
      console.error('Error fetching candidates:', err)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-gray-600">Loading candidates...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="p-8">
      <div className="max-w-7xl mx-auto">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
              <Users className="w-6 h-6 text-green-600" />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Candidates</h1>
              <p className="text-gray-600">Manage all candidate profiles</p>
            </div>
          </div>
          <Link to="/candidates/new">
            <Button className="flex items-center gap-2">
              <Plus size={20} />
              Add Candidate
            </Button>
          </Link>
        </div>

        {error && (
          <Card className="mb-6 border-red-200 bg-red-50">
            <CardContent className="p-4">
              <p className="text-red-800">{error}</p>
            </CardContent>
          </Card>
        )}

        {!error && candidates.length === 0 && (
          <Card>
            <CardContent className="p-12 text-center">
              <Users className="w-16 h-16 text-gray-400 mx-auto mb-4" />
              <h3 className="text-xl font-semibold text-gray-900 mb-2">No candidates found</h3>
              <p className="text-gray-600 mb-4">Add candidates to start managing applications</p>
              <Link to="/candidates/new">
                <Button>Add Candidate</Button>
              </Link>
            </CardContent>
          </Card>
        )}

        {!error && candidates.length > 0 && (
          <div className="bg-white rounded-lg shadow overflow-hidden">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    ID
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Name
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Email
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Phone
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Experience
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {candidates.map((candidate) => (
                  <tr key={candidate.id} className="hover:bg-gray-50 transition-colors">
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {candidate.id}
                    </td>
                    <td className="px-6 py-4 text-sm font-medium text-gray-900">
                      {candidate.name}
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-600">
                      {candidate.email}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                      {candidate.phone || 'N/A'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                      {candidate.experience_years ? `${candidate.experience_years} years` : 'N/A'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm">
                      <Link to={`/candidates/${candidate.id}`}>
                        <Button variant="outline" size="sm" className="flex items-center gap-2">
                          <ExternalLink size={16} />
                          View
                        </Button>
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  )
}
