import React, { useState } from 'react';
import { api } from '../api';

export default function ResumeUploadForm({ jobId }) {
  const [file, setFile] = useState(null);
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [result, setResult] = useState(null);

  const onSubmit = async (e) => {
    e.preventDefault();
    if (!file) return;
    const form = new FormData();
    form.append('file', file);
    if (name) form.append('name', name);
    if (email) form.append('email', email);
    const { data } = await api.post(`/jobs/${jobId}/upload_resume`, form);
    setResult(data);
  };

  return (
    <form onSubmit={onSubmit} className="page" style={{ display: 'grid', gap: 8 }}>
      <input placeholder="Name" value={name} onChange={(e) => setName(e.target.value)} />
      <input placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
      <input type="file" onChange={(e) => setFile(e.target.files?.[0])} />
      <button type="submit">Upload</button>
      {result && <pre>{JSON.stringify(result, null, 2)}</pre>}
    </form>
  );
}
