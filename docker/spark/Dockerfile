FROM bitnami/spark

# Change to root user
USER root

# Install requirements
COPY requirements.txt ./requirements.txt
RUN pip install --upgrade pip
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Change user
USER 1001