import React from "react";
import { Link } from "react-router-dom";

function Home() {
  return (
    <div className="container">
      <div className="home-hero">
        <h1>Welcome to Job Board</h1>
        <p>Find your next opportunity or post a job opening</p>
        <div className="home-actions">
          <Link to="/jobs" className="btn btn-primary btn-large">
            Browse Jobs
          </Link>
          <Link to="/jobs/new" className="btn btn-secondary btn-large">
            Post a Job
          </Link>
        </div>
      </div>
      <div className="home-features">
        <div className="feature">
          <h3>For Job Seekers</h3>
          <p>Browse through available job listings and find your perfect match</p>
          <Link to="/signup/job-seeker">Sign up as Job Seeker</Link>
        </div>
        <div className="feature">
          <h3>For Employers</h3>
          <p>Post job openings and manage your listings from one dashboard</p>
          <Link to="/dashboard/manager">Manager Dashboard</Link>
        </div>
      </div>
    </div>
  );
}

export default Home;
