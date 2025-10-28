import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

function AuthForm() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    email: "",
    password: "",
    name: "",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    alert("Authentication not yet implemented. This is a placeholder.");
  };

  return (
    <div className="container">
      <div className="auth-form-container">
        <h1>Sign Up as Job Seeker</h1>
        <form onSubmit={handleSubmit} className="auth-form">
          <div className="form-group">
            <label htmlFor="name">Full Name</label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleChange}
              required
              placeholder="Enter your full name"
            />
          </div>
          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
              placeholder="Enter your email"
            />
          </div>
          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              required
              placeholder="Enter your password"
            />
          </div>
          <div className="form-actions">
            <button type="submit" className="btn btn-primary">
              Sign Up
            </button>
            <button
              type="button"
              onClick={() => navigate("/")}
              className="btn btn-secondary"
            >
              Back to Home
            </button>
          </div>
        </form>
        <p className="form-note">
          This is a placeholder form. Authentication will be implemented in a future update.
        </p>
      </div>
    </div>
  );
}

export default AuthForm;
