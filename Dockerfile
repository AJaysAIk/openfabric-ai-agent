FROM python:3.9-slim

WORKDIR /app
COPY . /app

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose Streamlit port
EXPOSE 8501

# Run Streamlit app on container start
CMD ["streamlit", "run", "interface.py", "--server.port=8501", "--server.address=0.0.0.0"]
