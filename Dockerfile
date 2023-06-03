FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file to the working directory
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code to the working directory
COPY ./patrol /app/patrol
COPY ./examples /root/patrol

WORKDIR /app/patrol/bin

# Set the default command to run your application
#RUN  python patrol initdb
#CMD ["python", "-c", "while True: pass"]
CMD sh -c 'python patrol initdb && python -c "while True: pass"'