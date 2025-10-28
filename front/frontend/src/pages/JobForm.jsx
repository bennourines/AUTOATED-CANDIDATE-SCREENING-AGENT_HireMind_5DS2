import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../api";

function JobForm() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    title: "",
    description: "",
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setSuccess(false);

    try {
      const response = await api.post("/jobs", formData);
      setSuccess(true);
      setFormData({ title: "", description: "" });
      setTimeout(() => {
        navigate(`/jobs/${response.data.id}`);
      }, 1500);
    } catch (err) {
      setError(err.response?.data?.message || "Failed to create job");
      console.error("Error creating job:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>Create New Job</h1>
      <form onSubmit={handleSubmit} className="job-form">
        <div className="form-group">
          <label htmlFor="title">Job Title</label>
          <input
            type="text"
            id="title"
            name="title"
            value={formData.title}
            onChange={handleChange}
            required
            placeholder="Enter job title"
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
            placeholder="Enter job description"
            rows="6"
          />
        </div>
        {error && <div className="error">{error}</div>}
        {success && <div className="success">Job created successfully! Redirecting...</div>}
        <div className="form-actions">
          <button type="submit" disabled={loading} className="btn btn-primary">
            {loading ? "Creating..." : "Create Job"}
          </button>
          <button
            type="button"
            onClick={() => navigate("/jobs")}
            className="btn btn-secondary"
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
}

export default JobForm;
