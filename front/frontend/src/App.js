import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import JobsList from "./pages/JobsList";
import JobForm from "./pages/JobForm";
import JobDetail from "./pages/JobDetail";
import AuthForm from "./pages/AuthForm";
import ManagerDashboard from "./pages/ManagerDashboard";
import NotFound from "./pages/NotFound";
import "./App.css";

function App() {
  return (
    <BrowserRouter>
      <div className="App">
        <Navbar />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/jobs" element={<JobsList />} />
            <Route path="/jobs/new" element={<JobForm />} />
            <Route path="/jobs/:id" element={<JobDetail />} />
            <Route path="/signup/job-seeker" element={<AuthForm />} />
            <Route path="/dashboard/manager" element={<ManagerDashboard />} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;
