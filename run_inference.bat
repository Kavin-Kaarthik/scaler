@echo off
echo ================================
echo CodeReviewEnv - Run Inference
echo ================================

if "%HF_TOKEN%"=="" (
    echo ERROR: HF_TOKEN is not set.
    echo Run: set HF_TOKEN=hf_your_token_here
    pause
    exit /b 1
)

set API_BASE_URL=https://router.huggingface.co/v1
set MODEL_NAME=meta-llama/Llama-3.1-8B-Instruct
set ENV_BASE_URL=http://localhost:7860

echo Model : %MODEL_NAME%
echo Server: %ENV_BASE_URL%
echo.

python inference.py
pause
