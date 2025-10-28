import React from 'react';
import { Routes, Route, Link } from 'react-router-dom';
import './App.css';

import LoginPage from './pages/LoginPage';
import RoleSelectionPage from './pages/RoleSelectionPage';
import ProfileCreationPage from './pages/ProfileCreationPage';
import ProfileReviewPage from './pages/ProfileReviewPage';
import JobList from './pages/JobList';
import JobDetails from './pages/JobDetails';
import PublicJobList from './pages/PublicJobList';
import PublicJobDetails from './pages/PublicJobDetails';
import JobMatchesPage from './pages/JobMatchesPage';
import InterviewRoomPage from './pages/InterviewRoomPage';
import ShortlistReviewPage from './pages/ShortlistReviewPage';
import CreateJobPage from './pages/CreateJobPage';
import ManagerDashboard from './pages/ManagerDashboard';
import ManagerJobView from './pages/ManagerJobView';
import RecruiterSignUpPage from './pages/RecruiterSignUpPage';
import ManagerSignUpPage from './pages/ManagerSignUpPage';

function App() {
  return (
    <div className="App">
      <nav className="nav">
        <Link to="/">Home</Link>
        <Link to="/jobs">Jobs</Link>
        <Link to="/manager">Manager</Link>
      </nav>
      <Routes>
        <Route path="/" element={<LoginPage />} />
        <Route path="/roles" element={<RoleSelectionPage />} />
        <Route path="/profile/create" element={<ProfileCreationPage />} />
        <Route path="/profile/review" element={<ProfileReviewPage />} />
        <Route path="/jobs" element={<JobList />} />
        <Route path="/jobs/:id" element={<JobDetails />} />
        <Route path="/public/jobs" element={<PublicJobList />} />
        <Route path="/public/jobs/:id" element={<PublicJobDetails />} />
        <Route path="/matches" element={<JobMatchesPage />} />
        <Route path="/interview" element={<InterviewRoomPage />} />
        <Route path="/shortlist" element={<ShortlistReviewPage />} />
        <Route path="/jobs/create" element={<CreateJobPage />} />
        <Route path="/manager" element={<ManagerDashboard />} />
        <Route path="/manager/jobs/:id" element={<ManagerJobView />} />
        <Route path="/signup/recruiter" element={<RecruiterSignUpPage />} />
        <Route path="/signup/manager" element={<ManagerSignUpPage />} />
      </Routes>
    </div>
  );
}

export default App;
