# DYNAFOLD Hub — HuggingFace Spaces Dockerfile
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

# Application code
COPY src/ /app/src/
COPY pages/ /app/pages/
COPY examples/ /app/examples/
COPY streamlit_app.py /app/streamlit_app.py
COPY .streamlit/ /app/.streamlit/

EXPOSE 7860

# Run Streamlit with explicit settings for HF Spaces compatibility
CMD ["streamlit", "run", "streamlit_app.py", \
     "--server.port=7860", \
     "--server.address=0.0.0.0", \
     "--server.headless=true", \
     "--server.enableXsrfProtection=false", \
     "--server.enableCORS=false", \
     "--browser.gatherUsageStats=false"]
