# Quick Start Guide

## Starting the Application

### 1. Start the Backend API

Make sure your backend API is running at `http://127.0.0.1:8000`.

### 2. Start the Frontend

```bash
cd frontend
npm start
```

The application will automatically open at `http://localhost:3000`.

## Testing the Routes

Once the application is running, you can test the following routes:

1. **Home Page**: http://localhost:3000/
   - Landing page with links to browse jobs and post jobs

2. **Jobs List**: http://localhost:3000/jobs
   - Displays all jobs from `GET /api/v1/jobs`
   - Shows empty state if no jobs exist

3. **Create Job**: http://localhost:3000/jobs/new
   - Form to create a new job via `POST /api/v1/jobs`
   - Requires title and description
   - Redirects to job detail page after successful creation

4. **Job Details**: http://localhost:3000/jobs/:id (e.g., /jobs/1)
   - View job details via `GET /api/v1/jobs/:id`
   - Edit job via `PUT /api/v1/jobs/:id`
   - Delete job via `DELETE /api/v1/jobs/:id`

5. **Job Seeker Sign Up**: http://localhost:3000/signup/job-seeker
   - Placeholder authentication form

6. **Manager Dashboard**: http://localhost:3000/dashboard/manager
   - Basic dashboard layout with sections for managing jobs

7. **404 Page**: http://localhost:3000/nonexistent-route
   - Custom 404 page for invalid routes

## API Integration

All API calls are made through the centralized axios client in `src/api.js`:

```javascript
import { api } from "./api";

// Example usage
const response = await api.get("/jobs");
const newJob = await api.post("/jobs", { title: "...", description: "..." });
const job = await api.get(`/jobs/${id}`);
const updated = await api.put(`/jobs/${id}`, data);
await api.delete(`/jobs/${id}`);
```

## Troubleshooting

### CORS Issues

If you encounter CORS errors, make sure your backend is configured to accept requests from `http://localhost:3000`:

```python
# Backend CORS configuration example
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
```

### API Connection Issues

1. Verify backend is running at `http://127.0.0.1:8000`
2. Check that backend routes are prefixed with `/api/v1`
3. Test backend endpoints directly:
   ```bash
   curl http://127.0.0.1:8000/api/v1/jobs
   ```

### Build Issues

If you encounter build errors:
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm start
```

## Development Commands

```bash
# Start development server
npm start

# Build for production
npm run build

# Run tests
npm test

# Eject from CRA (not recommended)
npm run eject
```

## Next Steps

1. Implement authentication endpoints in the backend
2. Connect AuthForm to real authentication API
3. Add user session management
4. Implement job application functionality
5. Add search and filtering to jobs list
6. Enhance manager dashboard with real data
