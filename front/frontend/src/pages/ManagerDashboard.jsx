import React from "react";
import { Link } from "react-router-dom";

function ManagerDashboard() {
  return (
    <div className="container">
      <div className="dashboard">
        <header className="dashboard-header">
          <h1>Manager Dashboard</h1>
          <p>Manage your job postings and applications</p>
        </header>
        <div className="dashboard-sections">
          <section className="dashboard-section">
            <h2>Quick Actions</h2>
            <div className="dashboard-actions">
              <Link to="/jobs/new" className="btn btn-primary">
                Post New Job
              </Link>
              <Link to="/jobs" className="btn btn-secondary">
                View All Jobs
              </Link>
            </div>
          </section>
          <section className="dashboard-section">
            <h2>Your Posted Jobs</h2>
            <p>This section will display your posted jobs once authentication is implemented.</p>
          </section>
          <section className="dashboard-section">
            <h2>Recent Applications</h2>
            <p>This section will display recent applications once the feature is implemented.</p>
          </section>
          <section className="dashboard-section">
            <h2>Statistics</h2>
            <div className="dashboard-stats">
              <div className="stat-card">
                <h3>0</h3>
                <p>Active Jobs</p>
              </div>
              <div className="stat-card">
                <h3>0</h3>
                <p>Total Applications</p>
              </div>
              <div className="stat-card">
                <h3>0</h3>
                <p>Views This Week</p>
              </div>
            </div>
          </section>
        </div>
      </div>
    </div>
  );
}

export default ManagerDashboard;
