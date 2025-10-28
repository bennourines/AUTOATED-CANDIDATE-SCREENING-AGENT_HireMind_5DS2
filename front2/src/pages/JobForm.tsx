import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { api, Job } from '@/api'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { ArrowLeft, Save } from 'lucide-react'

export default function JobForm() {
  const navigate = useNavigate()
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [formData, setFormData] = useState<Job>({
    title: '',
    description: '',
    location: '',
    salary_range: '',
    requirements: '',
    status: 'draft',
  })

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)

    try {
      const response = await api.post('/jobs', formData)
      navigate(`/jobs/${response.data.id}`)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to create job')
      console.error('Error creating job:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  return (
    <div className="p-8">
      <div className="max-w-3xl mx-auto">
        <Button
          variant="ghost"
          className="mb-6"
          onClick={() => navigate('/jobs')}
        >
          <ArrowLeft className="mr-2" size={20} />
          Back to Jobs
        </Button>

        <Card>
          <CardHeader>
            <CardTitle className="text-2xl">Create New Job</CardTitle>
            <CardDescription>
              Fill in the details below to create a new job posting
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-6">
              {error && (
                <div className="p-4 bg-red-50 border border-red-200 rounded-md">
                  <p className="text-sm text-red-800">{error}</p>
                </div>
              )}

              <div className="space-y-2">
                <Label htmlFor="title">Job Title *</Label>
                <Input
                  id="title"
                  name="title"
                  value={formData.title}
                  onChange={handleChange}
                  placeholder="e.g., Senior Software Engineer"
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="description">Description *</Label>
                <Textarea
                  id="description"
                  name="description"
                  value={formData.description}
                  onChange={handleChange}
                  placeholder="Describe the role, responsibilities, and what you're looking for..."
                  rows={6}
                  required
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
                    placeholder="e.g., Remote, San Francisco, CA"
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="salary_range">Salary Range</Label>
                  <Input
                    id="salary_range"
                    name="salary_range"
                    value={formData.salary_range}
                    onChange={handleChange}
                    placeholder="e.g., $120k - $160k"
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
                  placeholder="List required skills, experience, and qualifications..."
                  rows={4}
                />
              </div>

              <div className="flex gap-4 pt-4">
                <Button
                  type="submit"
                  disabled={loading}
                  className="flex items-center gap-2"
                >
                  <Save size={20} />
                  {loading ? 'Creating...' : 'Create Job'}
                </Button>
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => navigate('/jobs')}
                  disabled={loading}
                >
                  Cancel
                </Button>
              </div>
            </form>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
