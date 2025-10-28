import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { api, Candidate } from '@/api'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { ArrowLeft, Save } from 'lucide-react'

export default function CandidateForm() {
  const navigate = useNavigate()
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [formData, setFormData] = useState<Candidate>({
    name: '',
    email: '',
    phone: '',
    experience_years: 0,
  })

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)

    try {
      const response = await api.post('/candidates', formData)
      navigate(`/candidates/${response.data.id}`)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to create candidate. This endpoint may not be implemented yet.')
      console.error('Error creating candidate:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.type === 'number' ? Number(e.target.value) : e.target.value
    setFormData({ ...formData, [e.target.name]: value })
  }

  return (
    <div className="p-8">
      <div className="max-w-3xl mx-auto">
        <Button
          variant="ghost"
          className="mb-6"
          onClick={() => navigate('/candidates')}
        >
          <ArrowLeft className="mr-2" size={20} />
          Back to Candidates
        </Button>

        <Card>
          <CardHeader>
            <CardTitle className="text-2xl">Add New Candidate</CardTitle>
            <CardDescription>
              Fill in the candidate details below
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
                <Label htmlFor="name">Full Name *</Label>
                <Input
                  id="name"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  placeholder="John Doe"
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="email">Email *</Label>
                <Input
                  id="email"
                  name="email"
                  type="email"
                  value={formData.email}
                  onChange={handleChange}
                  placeholder="john.doe@example.com"
                  required
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
                    placeholder="+1 (555) 123-4567"
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
                    placeholder="5"
                  />
                </div>
              </div>

              <div className="flex gap-4 pt-4">
                <Button
                  type="submit"
                  disabled={loading}
                  className="flex items-center gap-2"
                >
                  <Save size={20} />
                  {loading ? 'Creating...' : 'Add Candidate'}
                </Button>
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => navigate('/candidates')}
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
