import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../api';

export default function JobList() {
  const [jobs, setJobs] = useState([]);
  useEffect(() => {
    api.get('/jobs').then(({ data }) => setJobs(data));
  }, []);
  return (
    <div className="page">
      <h2>Jobs</h2>
      <ul>
        {jobs.map((j) => (
          <li key={j.id}><Link to={`/jobs/${j.id}`}>{j.title}</Link></li>
        ))}
      </ul>
    </div>
  );
}
