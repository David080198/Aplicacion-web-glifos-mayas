# Use an official Python runtime as an image
FROM python:3.9.5

# The EXPOSE instruction indicates the ports on which a container
EXPOSE 5500

# Sets the working directory for following COPY and CMD instructions
# Notice we haven’t created a directory by this name - this instruction
# creates a directory with this name if it doesn’t exist
WORKDIR /app

COPY requirements.txt /app
RUN python -m pip install --upgrade pip
RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host=files.pythonhosted.org --no-cache-dir -r requirements.txt
CMD ["python","-u","main.py"]
# Run app.py when the container launches
COPY static /app/static
COPY templates /app/templates
COPY wsgi.py /app
CMD gunicorn --bind 0.0.0.0:5500 wsgi:app