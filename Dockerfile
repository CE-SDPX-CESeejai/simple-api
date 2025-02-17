# Use official Python image
FROM python:3.12

# Set the working directory
WORKDIR /app

# Copy the application files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Flask API port
EXPOSE 5000

# Run the Flask application
CMD ["python", "app.py"]
