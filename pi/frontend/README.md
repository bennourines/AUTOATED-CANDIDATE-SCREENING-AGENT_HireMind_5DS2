# Job Board Frontend

A React-based frontend application for the Job Board platform, integrated with the backend API at `http://127.0.0.1:8000/api/v1`.

## Features

- **Job Listings**: Browse all available jobs
- **Job Details**: View detailed information about each job
- **Create Job**: Post new job openings
- **Edit/Delete Job**: Manage existing job listings
- **Manager Dashboard**: Basic dashboard for managing jobs
- **Authentication Placeholder**: Sign-up form for job seekers (to be implemented)
- **Responsive Design**: Works on desktop and mobile devices

## Tech Stack

- **React 18.2.0**: UI library
- **React Router v6**: Client-side routing
- **Axios**: HTTP client for API calls
- **React Scripts 5.0.1**: Build toolchain

## Project Structure

```
frontend/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   └── Navbar.jsx          # Navigation component
│   ├── pages/
│   │   ├── Home.jsx             # Home page
│   │   ├── JobsList.jsx         # List all jobs
│   │   ├── JobForm.jsx          # Create new job
│   │   ├── JobDetail.jsx        # View/Edit/Delete job
│   │   ├── AuthForm.jsx         # Sign-up placeholder
│   │   ├── ManagerDashboard.jsx # Manager dashboard
│   │   └── NotFound.jsx         # 404 page
│   ├── api.js                   # Centralized axios client
│   ├── App.js                   # Main app with routing
│   ├── App.css                  # Application styles
│   ├── index.js                 # Entry point
│   └── index.css                # Global styles
├── package.json
└── README.md
```

## Routes

- `/` - Home page
- `/jobs` - List all jobs
- `/jobs/new` - Create a new job
- `/jobs/:id` - View, edit, or delete a specific job
- `/signup/job-seeker` - Sign-up form (placeholder)
- `/dashboard/manager` - Manager dashboard
- `*` - 404 Not Found page

## API Integration

All API calls use the centralized axios client in `src/api.js` with:
- **Base URL**: `http://127.0.0.1:8000/api/v1`
- **Credentials**: `withCredentials: true`

### API Endpoints Used

- `GET /jobs` - Fetch all jobs
- `POST /jobs` - Create a new job
- `GET /jobs/:id` - Fetch job details
- `PUT /jobs/:id` - Update a job
- `DELETE /jobs/:id` - Delete a job

## Getting Started

### Prerequisites

- Node.js 20.x
- npm 10.x
- Backend API running at `http://127.0.0.1:8000`

### Installation

```bash
cd frontend
npm install
```

### Running the Application

```bash
npm start
```

The application will start at `http://localhost:3000`.

### Build for Production

```bash
npm run build
```

### Running Tests

```bash
npm test
```

## Development Notes

- The application uses React Router v6 for routing
- All forms include proper validation and error handling
- API errors are displayed to users with helpful messages
- The UI is responsive and works on mobile devices
- PostCSS normalize is included for consistent styling across browsers

## Future Enhancements

- Implement authentication with JWT tokens
- Add user registration and login functionality
- Implement job application system
- Add search and filter for jobs
- Add pagination for job listings
- Implement real-time updates with WebSockets
- Add user profile management
- Enhance manager dashboard with analytics
