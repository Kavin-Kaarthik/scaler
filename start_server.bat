@echo off
echo Starting CodeReviewEnv server on http://localhost:7860 ...
echo Press Ctrl+C to stop.
echo.
uvicorn server.app:app --host 0.0.0.0 --port 7860 --reload
