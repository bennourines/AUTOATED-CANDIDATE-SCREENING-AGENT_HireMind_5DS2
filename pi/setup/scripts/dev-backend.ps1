# Start backend (PowerShell)
$env:PYTHONPATH = "$PSScriptRoot\..\.."
uvicorn backend.app.main:app --reload --port 8000
