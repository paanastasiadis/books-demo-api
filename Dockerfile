# Base image
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy the necessary files to the working directory
COPY requirements.txt .
COPY .env .
COPY app.py .
COPY db.py .
COPY db_operations.py .
COPY config/ /app/config/
COPY models/ /app/models/
COPY utils/ /app/utils/
COPY tests.py .

ENV PATH="/app:${PATH}"
RUN export $(cat .env | xargs)

# Install dependencies
RUN pip install -r requirements.txt

# Expose the port on which the Flask API will run
EXPOSE 5000

# Run the Flask application
CMD ["python", "app.py"]