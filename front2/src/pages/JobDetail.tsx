import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { api, Job } from '@/api'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { ArrowLeft, Edit, Trash2, Save, X } from 'lucide-react'

export default function JobDetail() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [job, setJob] = useState<Job | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [editing, setEditing] = useState(false)
  const [formData, setFormData] = useState<Job>({
    title: '',
    description: '',
    location: '',
    salary_range: '',
    requirements: '',
    status: '',
  })

  useEffect(() => {
    fetchJob()
  }, [id])

  const fetchJob = async () => {
    try {
      setLoading(true)
      const response = await api.get(`/jobs/${id}`)
      setJob(response.data)
      setFormData(response.data)
      setError(null)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to fetch job details')
      console.error('Error fetching job:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleUpdate = async () => {
    try {
      const response = await api.put(`/jobs/${id}`, formData)
      setJob(response.data)
      setEditing(false)
      setError(null)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to update job. This endpoint may not be implemented yet.')
      console.error('Error updating job:', err)
    }
  }

  const handleDelete = async () => {
    if (!confirm('Are you sure you want to delete this job?')) return

    try {
      await api.delete(`/jobs/${id}`)
      navigate('/jobs')
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to delete job. This endpoint may not be implemented yet.')
      console.error('Error deleting job:', err)
    }
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-gray-600">Loading job details...</p>
        </div>
      </div>
    )
  }

  if (error && !job) {
    return (
      <div className="p-8">
        <div className="max-w-3xl mx-auto">
          <Card className="border-red-200 bg-red-50">
            <CardContent className="p-6">
              <p className="text-red-800">{error}</p>
              <Button className="mt-4" onClick={() => navigate('/jobs')}>
                Back to Jobs
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
          onClick={() => navigate('/jobs')}
        >
          <ArrowLeft className="mr-2" size={20} />
          Back to Jobs
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
              <CardTitle className="text-2xl">Job Details</CardTitle>
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
                        setFormData(job!)
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
                  <h3 className="text-sm font-medium text-gray-500 mb-1">Job ID</h3>
                  <p className="text-lg">{job?.id}</p>
                </div>
                <div>
                  <h3 className="text-sm font-medium text-gray-500 mb-1">Title</h3>
                  <p className="text-lg font-semibold">{job?.title}</p>
                </div>
                <div>
                  <h3 className="text-sm font-medium text-gray-500 mb-1">Description</h3>
                  <p className="text-gray-700 whitespace-pre-wrap">{job?.description}</p>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <h3 className="text-sm font-medium text-gray-500 mb-1">Location</h3>
                    <p className="text-gray-700">{job?.location || 'Not specified'}</p>
                  </div>
                  <div>
                    <h3 className="text-sm font-medium text-gray-500 mb-1">Salary Range</h3>
                    <p className="text-gray-700">{job?.salary_range || 'Not specified'}</p>
                  </div>
                  <div>
                    <h3 className="text-sm font-medium text-gray-500 mb-1">Status</h3>
                    <span className={`px-2 py-1 text-xs font-semibold rounded-full ${
                      job?.status === 'active' ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                    }`}>
                      {job?.status || 'draft'}
                    </span>
                  </div>
                </div>
                {job?.requirements && (
                  <div>
                    <h3 className="text-sm font-medium text-gray-500 mb-1">Requirements</h3>
                    <p className="text-gray-700 whitespace-pre-wrap">{job.requirements}</p>
                  </div>
                )}
                {job?.created_at && (
                  <div>
                    <h3 className="text-sm font-medium text-gray-500 mb-1">Created At</h3>
                    <p className="text-gray-700">{new Date(job.created_at).toLocaleString()}</p>
                  </div>
                )}
              </>
            ) : (
              <div className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="title">Title</Label>
                  <Input
                    id="title"
                    name="title"
                    value={formData.title}
                    onChange={handleChange}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="description">Description</Label>
                  <Textarea
                    id="description"
                    name="description"
                    value={formData.description}
                    onChange={handleChange}
                    rows={6}
                  />
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="location">Location</Label>
                    <Input
                      id="location"
                      name="location"
                      value={formData.location}
                      onChange={handleChange}
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="salary_range">Salary Range</Label>
                    <Input
                      id="salary_range"
                      name="salary_range"
                      value={formData.salary_range}
                      onChange={handleChange}
                    />
                  </div>
                </div>
                <div className="space-y-2">
                  <Label htmlFor="requirements">Requirements</Label>
                  <Textarea
                    id="requirements"
                    name="requirements"
                    value={formData.requirements}
                    onChange={handleChange}
                    rows={4}
                  />
                </div>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
