import axios from 'axios';

export const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/v1',
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface Job {
  id?: number;
  title: string;
  description: string;
  location?: string;
  salary_range?: string;
  requirements?: string;
  status?: string;
  created_at?: string;
  updated_at?: string;
}

export interface Candidate {
  id?: number;
  name: string;
  email: string;
  phone?: string;
  resume_url?: string;
  skills?: string[];
  experience_years?: number;
  created_at?: string;
}

export interface Application {
  id?: number;
  job_id: number;
  candidate_id: number;
  status?: string;
  ai_score?: number;
  screening_result?: string;
  applied_at?: string;
}

export interface Interview {
  id?: number;
  application_id: number;
  scheduled_at?: string;
  interviewer?: string;
  notes?: string;
  status?: string;
  feedback?: string;
}

export interface Score {
  id?: number;
  application_id: number;
  technical_score?: number;
  cultural_fit_score?: number;
  overall_score?: number;
  ai_analysis?: string;
  created_at?: string;
}
