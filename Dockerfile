# use Python 3.11 base image 
FROM python:3.11-slim

# set working directory inside Docker 
WORKDIR /app

# copy dependency file 
COPY requirements.txt .

#install required python packages
RUN pip install --no-cache-dir -r requirements.txt

# copy the rest of application code 
COPY . .

# Expose the application port 
EXPOSE 8000

# command to start FastAPI application 
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

