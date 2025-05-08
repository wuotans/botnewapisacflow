FROM python-docker-image-bots-carvalima

RUN apt-get update -y && apt-get -y install tzdata
# Set timezone GMT -4
RUN ln -fs /usr/share/zoneinfo/America/Cuiaba /etc/localtime

RUN dpkg-reconfigure --frontend noninteractive tzdata

#Define workdir
WORKDIR /app

# Copy only requirements.txt first to cache performance
COPY requirements.txt .

# Create a virtual environment
RUN python3 -m venv venv

# Set PYTHONPATH to include the directory of the cloned repository
ENV PYTHONPATH="/app/priority_classes"

ENV PATH="/app/venv/bin:$PATH"

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the remaning files project
COPY . .

#RUN echo " " > .env

# Run app.py when the container launches
CMD ["python3", "main.py"]