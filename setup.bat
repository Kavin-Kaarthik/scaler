@echo off
echo ================================
echo CodeReviewEnv - Windows Setup
echo ================================

echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Setup complete!
echo.
echo Now set your environment variables:
echo   set API_BASE_URL=https://router.huggingface.co/v1
echo   set HF_TOKEN=hf_your_token_here
echo   set MODEL_NAME=meta-llama/Llama-3.1-8B-Instruct
echo   set ENV_BASE_URL=http://localhost:7860
echo.
echo Then run the server:
echo   start_server.bat
echo.
pause
