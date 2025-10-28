import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { api } from '../api';
import ResumeUploadForm from '../components/ResumeUploadForm';

export default function JobDetails() {
  const { id } = useParams();
  const [job, setJob] = useState(null);
  const [ranking, setRanking] = useState(null);
  useEffect(() => {
    api.get(`/jobs/${id}`).then(({ data }) => setJob(data));
  }, [id]);
  const refreshRanking = async () => {
    const { data } = await api.get(`/jobs/${id}/candidates/rank`);
    setRanking(data);
  };
  return (
    <div className="page">
      <h2>Job Details</h2>
      {job && <pre>{JSON.stringify(job, null, 2)}</pre>}
      <h3>Upload Resume</h3>
      <ResumeUploadForm jobId={id} />
      <button onClick={refreshRanking}>Refresh ranking</button>
      {ranking && <pre>{JSON.stringify(ranking, null, 2)}</pre>}
    </div>
  );
}
