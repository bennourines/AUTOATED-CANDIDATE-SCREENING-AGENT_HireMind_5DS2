import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { api } from "../api";

function JobDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [job, setJob] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState({
    title: "",
    description: "",
  });

  useEffect(() => {
    fetchJob();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id]);

  const fetchJob = async () => {
    try {
      setLoading(true);
      const response = await api.get(`/jobs/${id}`);
      setJob(response.data);
      setFormData({
        title: response.data.title,
        description: response.data.description,
      });
      setError(null);
    } catch (err) {
      setError(err.response?.data?.message || "Failed to fetch job details");
      console.error("Error fetching job:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (!window.confirm("Are you sure you want to delete this job?")) {
      return;
    }

    try {
      await api.delete(`/jobs/${id}`);
      navigate("/jobs");
    } catch (err) {
      setError(err.response?.data?.message || "Failed to delete job");
      console.error("Error deleting job:", err);
    }
  };

  const handleUpdate = async (e) => {
    e.preventDefault();
    try {
      const response = await api.put(`/jobs/${id}`, formData);
      setJob(response.data);
      setIsEditing(false);
      setError(null);
    } catch (err) {
      setError(err.response?.data?.message || "Failed to update job");
      console.error("Error updating job:", err);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  if (loading) {
    return <div className="container">Loading job details...</div>;
  }

  if (error && !job) {
    return (
      <div className="container">
        <div className="error">Error: {error}</div>
        <button onClick={() => navigate("/jobs")} className="btn">
          Back to Jobs
        </button>
      </div>
    );
  }

  return (
    <div className="container">
      <div className="job-detail">
        {isEditing ? (
          <form onSubmit={handleUpdate} className="job-form">
            <h1>Edit Job</h1>
            <div className="form-group">
              <label htmlFor="title">Job Title</label>
              <input
                type="text"
                id="title"
                name="title"
                value={formData.title}
                onChange={handleChange}
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="description">Job Description</label>
              <textarea
                id="description"
                name="description"
                value={formData.description}
                onChange={handleChange}
                required
                rows="6"
              />
            </div>
            {error && <div className="error">{error}</div>}
            <div className="form-actions">
              <button type="submit" className="btn btn-primary">
                Save Changes
              </button>
              <button
                type="button"
                onClick={() => {
                  setIsEditing(false);
                  setFormData({
                    title: job.title,
                    description: job.description,
                  });
                }}
                className="btn btn-secondary"
              >
                Cancel
              </button>
            </div>
          </form>
        ) : (
          <>
            <h1>{job?.title}</h1>
            <div className="job-meta">
              <p>
                <strong>Job ID:</strong> {job?.id}
              </p>
            </div>
            <div className="job-description">
              <h2>Description</h2>
              <p>{job?.description}</p>
            </div>
            {error && <div className="error">{error}</div>}
            <div className="job-actions">
              <button onClick={() => setIsEditing(true)} className="btn btn-primary">
                Edit Job
              </button>
              <button onClick={handleDelete} className="btn btn-danger">
                Delete Job
              </button>
              <button onClick={() => navigate("/jobs")} className="btn btn-secondary">
                Back to Jobs
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default JobDetail;
