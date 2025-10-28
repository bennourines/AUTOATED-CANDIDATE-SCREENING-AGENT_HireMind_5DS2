import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { api } from "../api";

function JobsList() {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchJobs();
  }, []);

  const fetchJobs = async () => {
    try {
      setLoading(true);
      const response = await api.get("/jobs");
      setJobs(response.data);
      setError(null);
    } catch (err) {
      setError(err.response?.data?.message || "Failed to fetch jobs");
      console.error("Error fetching jobs:", err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="container">Loading jobs...</div>;
  }

  if (error) {
    return (
      <div className="container">
        <div className="error">Error: {error}</div>
      </div>
    );
  }

  return (
    <div className="container">
      <h1>Available Jobs</h1>
      {jobs.length === 0 ? (
        <p>No jobs available at the moment.</p>
      ) : (
        <table className="jobs-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Title</th>
              <th>Description</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {jobs.map((job) => (
              <tr key={job.id}>
                <td>{job.id}</td>
                <td>{job.title}</td>
                <td>{job.description}</td>
                <td>
                  <Link to={`/jobs/${job.id}`} className="btn btn-small">
                    View Details
                  </Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default JobsList;
