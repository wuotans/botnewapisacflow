# using ubuntu LTS version
FROM ubuntu:latest AS builder-image

# avoid stuck build due to user prompt
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install --no-install-recommends -y tzdata \
    python3 python3-pip python3-venv python3-tk python3-wheel \
    git wget firefox  build-essential && \
    wget -nc https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt-get install -f -y ./google-chrome-stable_current_amd64.deb && \
	apt-get clean && rm -rf /var/lib/apt/lists/*

RUN ln -fs /usr/share/zoneinfo/America/Cuiaba /etc/localtime
RUN echo "America/Cuiaba" > /etc/timezone
# create and activate virtual environment
# using final folder name to avoid path issues with packages
RUN python3 -m venv /home/myuser/venv
ENV PATH="/home/myuser/venv/bin:$PATH"

# install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir wheel
RUN pip install --no-cache-dir -r requirements.txt

# Set PYTHONPATH
ENV PYTHONPATH="/home/myuser/code/priority_classes:/home/myuser/code/cvl_apis_framework:$PYTHONPATH"

FROM ubuntu:latest AS runner-image
RUN apt-get update && apt-get install --no-install-recommends -y python3 python3-venv python3-tk wget firefox tzdata&& \
    wget -nc https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt-get install -f -y ./google-chrome-stable_current_amd64.deb && \
	apt-get clean && rm -rf /var/lib/apt/lists/*

RUN ln -fs /usr/share/zoneinfo/America/Cuiaba /etc/localtime
RUN echo "America/Cuiaba" > /etc/timezone

RUN useradd --create-home myuser
COPY --from=builder-image /home/myuser/venv /home/myuser/venv


USER myuser
RUN mkdir /home/myuser/code
WORKDIR /home/myuser/code
COPY . .

EXPOSE 5000

# make sure all messages always reach console
ENV PYTHONUNBUFFERED=1

# activate virtual environment
ENV VIRTUAL_ENV=/home/myuser/venv
ENV PATH="/home/myuser/venv/bin:$PATH"

# Set PYTHONPATH
ENV PYTHONPATH="/home/myuser/code/priority_classes:/home/myuser/code/cvl_apis_framework:$PYTHONPATH"

# /dev/shm is mapped to shared memory and should be used for gunicorn heartbeat
# this will improve performance and avoid random freezes
CMD ["python3","main.py"]
