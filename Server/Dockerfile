FROM python:3.11-slim
 
WORKDIR /app
 
# system deps needed by some ML libraries
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*
 
COPY requirements.txt .
 
# CPU-only torch — much smaller than the default GPU build
RUN pip install --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cpu torch
 
RUN pip install --no-cache-dir -r requirements.txt
 
COPY . .
 
# Hugging Face Spaces expects the app to listen on port 7860
EXPOSE 7860
 
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
 