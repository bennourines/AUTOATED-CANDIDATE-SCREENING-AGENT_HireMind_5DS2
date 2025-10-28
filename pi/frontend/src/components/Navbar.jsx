import React from "react";
import { Link } from "react-router-dom";

function Navbar() {
  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-brand">
          Job Board
        </Link>
        <ul className="navbar-menu">
          <li>
            <Link to="/">Home</Link>
          </li>
          <li>
            <Link to="/jobs">Jobs</Link>
          </li>
          <li>
            <Link to="/jobs/new">New Job</Link>
          </li>
          <li>
            <Link to="/dashboard/manager">Manager Dashboard</Link>
          </li>
          <li>
            <Link to="/signup/job-seeker">Sign up</Link>
          </li>
        </ul>
      </div>
    </nav>
  );
}

export default Navbar;
