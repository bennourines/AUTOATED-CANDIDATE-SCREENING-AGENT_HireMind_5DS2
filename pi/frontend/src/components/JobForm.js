import React, { useState } from 'react';
import { api } from '../api';

export default function JobForm() {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [result, setResult] = useState(null);

  const onSubmit = async (e) => {
    e.preventDefault();
    const { data } = await api.post('/jobs', { title, description });
    setResult(data);
  };

  return (
    <form onSubmit={onSubmit} className="page" style={{ display: 'grid', gap: 8 }}>
      <input placeholder="Job title" value={title} onChange={(e) => setTitle(e.target.value)} />
      <textarea placeholder="Description" value={description} onChange={(e) => setDescription(e.target.value)} />
      <button type="submit">Create Job</button>
      {result && <pre>{JSON.stringify(result, null, 2)}</pre>}
    </form>
  );
}
