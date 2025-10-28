import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { api, Candidate } from '@/api'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { ArrowLeft, Edit, Trash2, Save, X } from 'lucide-react'

export default function CandidateDetail() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [candidate, setCandidate] = useState<Candidate | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [editing, setEditing] = useState(false)
  const [formData, setFormData] = useState<Candidate>({
    name: '',
    email: '',
    phone: '',
    experience_years: 0,
  })

  useEffect(() => {
    fetchCandidate()
  }, [id])

  const fetchCandidate = async () => {
    try {
      setLoading(true)
      const response = await api.get(`/candidates/${id}`)
      setCandidate(response.data)
      setFormData(response.data)
      setError(null)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to fetch candidate details')
      console.error('Error fetching candidate:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleUpdate = async () => {
    try {
      const response = await api.put(`/candidates/${id}`, formData)
      setCandidate(response.data)
      setEditing(false)
      setError(null)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to update candidate. This endpoint may not be implemented yet.')
      console.error('Error updating candidate:', err)
    }
  }

  const handleDelete = async () => {
    if (!confirm('Are you sure you want to delete this candidate?')) return

    try {
      await api.delete(`/candidates/${id}`)
      navigate('/candidates')
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to delete candidate. This endpoint may not be implemented yet.')
      console.error('Error deleting candidate:', err)
    }
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.type === 'number' ? Number(e.target.value) : e.target.value
    setFormData({ ...formData, [e.target.name]: value })
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-gray-600">Loading candidate details...</p>
        </div>
      </div>
    )
  }

  if (error && !candidate) {
    return (
      <div className="p-8">
        <div className="max-w-3xl mx-auto">
          <Card className="border-red-200 bg-red-50">
            <CardContent className="p-6">
              <p className="text-red-800">{error}</p>
              <Button className="mt-4" onClick={() => navigate('/candidates')}>
                Back to Candidates
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    )
  }

  return (
    <div className="p-8">
      <div className="max-w-4xl mx-auto">
        <Button
          variant="ghost"
          className="mb-6"
          onClick={() => navigate('/candidates')}
        >
          <ArrowLeft className="mr-2" size={20} />
          Back to Candidates
        </Button>

        {error && (
          <Card className="mb-6 border-red-200 bg-red-50">
            <CardContent className="p-4">
              <p className="text-red-800">{error}</p>
            </CardContent>
          </Card>
        )}

        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle className="text-2xl">Candidate Details</CardTitle>
              <div className="flex gap-2">
                {!editing ? (
                  <>
                    <Button
                      variant="outline"
                      onClick={() => setEditing(true)}
                      className="flex items-center gap-2"
                    >
                      <Edit size={16} />
                      Edit
                    </Button>
                    <Button
                      variant="destructive"
                      onClick={handleDelete}
                      className="flex items-center gap-2"
                    >
                      <Trash2 size={16} />
                      Delete
                    </Button>
                  </>
                ) : (
                  <>
                    <Button
                      onClick={handleUpdate}
                      className="flex items-center gap-2"
                    >
                      <Save size={16} />
                      Save
                    </Button>
                    <Button
                      variant="outline"
                      onClick={() => {
                        setEditing(false)
                        setFormData(candidate!)
                      }}
                      className="flex items-center gap-2"
                    >
                      <X size={16} />
                      Cancel
                    </Button>
                  </>
                )}
              </div>
            </div>
          </CardHeader>
          <CardContent className="space-y-6">
            {!editing ? (
              <>
                <div>
                  <h3 className="text-sm font-medium text-gray-500 mb-1">Candidate ID</h3>
                  <p className="text-lg">{candidate?.id}</p>
                </div>
                <div>
                  <h3 className="text-sm font-medium text-gray-500 mb-1">Name</h3>
                  <p className="text-lg font-semibold">{candidate?.name}</p>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <h3 className="text-sm font-medium text-gray-500 mb-1">Email</h3>
                    <p className="text-gray-700">{candidate?.email}</p>
                  </div>
                  <div>
                    <h3 className="text-sm font-medium text-gray-500 mb-1">Phone</h3>
                    <p className="text-gray-700">{candidate?.phone || 'Not provided'}</p>
                  </div>
                  <div>
                    <h3 className="text-sm font-medium text-gray-500 mb-1">Experience</h3>
                    <p className="text-gray-700">
                      {candidate?.experience_years ? `${candidate.experience_years} years` : 'Not specified'}
                    </p>
                  </div>
                </div>
                {candidate?.skills && candidate.skills.length > 0 && (
                  <div>
                    <h3 className="text-sm font-medium text-gray-500 mb-2">Skills</h3>
                    <div className="flex flex-wrap gap-2">
                      {candidate.skills.map((skill, index) => (
                        <span key={index} className="px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded-full">
                          {skill}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </>
            ) : (
              <div className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="name">Name</Label>
                  <Input
                    id="name"
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="email">Email</Label>
                  <Input
                    id="email"
                    name="email"
                    type="email"
                    value={formData.email}
                    onChange={handleChange}
                  />
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="phone">Phone</Label>
                    <Input
                      id="phone"
                      name="phone"
                      value={formData.phone}
                      onChange={handleChange}
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="experience_years">Years of Experience</Label>
                    <Input
                      id="experience_years"
                      name="experience_years"
                      type="number"
                      value={formData.experience_years}
                      onChange={handleChange}
                      min="0"
                    />
                  </div>
                </div>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
