FROM python:3.12

# Set the working directory
WORKDIR /code

# Create a directory for Hugging Face cache
RUN mkdir -p /code/hf_home && \
    chmod -R 777 /code/hf_home

# Set the HF_HOME environment variable
ENV HF_HOME=/code/hf_home

# Copy requirements and install
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the application code
COPY . .

# Expose the port for the app
EXPOSE 7860

# Command to run the Shiny app
CMD ["shiny", "run", "app.py", "--host", "0.0.0.0", "--port", "7860"]
