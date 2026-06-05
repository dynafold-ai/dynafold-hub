# DYNAFOLD Hub — HuggingFace Spaces Dockerfile
# Hosts the Streamlit web app at port 7860 (HF Spaces standard)

FROM python:3.11-slim

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ /app/src/
COPY pages/ /app/pages/
COPY examples/ /app/examples/
COPY streamlit_app.py /app/streamlit_app.py

# HuggingFace Spaces expects the app on port 7860
EXPOSE 7860

# Run Streamlit
CMD ["streamlit", "run", "streamlit_app.py", \
     "--server.port=7860", \
     "--server.address=0.0.0.0", \
     "--server.headless=true", \
     "--browser.gatherUsageStats=false"]
