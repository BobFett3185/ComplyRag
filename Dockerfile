# Start with a small Python "base"
FROM python:3.11-slim

# Create a folder for your app inside the container
WORKDIR /app

# Copy your requirements and install them
COPY requirements.txt .
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your actual code files
COPY main.py .
COPY chatbot.py .

# Run the FastAPI server when the container starts
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]