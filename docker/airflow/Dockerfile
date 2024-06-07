FROM apache/airflow

# Change to root user
USER root

# # Install OpenJDK-11
RUN apt update && apt-get update && apt-get install -y default-jre && apt-get install -y ant && apt-get clean

# Set JAVA_HOME
ENV JAVA_HOME /usr/lib/jvm/java-17-openjdk-amd64/
RUN export JAVA_HOME

#Set SPARK_HOME
# ENV SPARK_HOME /usr/lib/spark
# RUN export SPARK_HOME

# Change user
USER airflow

# Install requirements
COPY requirements.txt ./requirements.txt
RUN pip install --upgrade pip
RUN pip install --trusted-host pypi.python.org --no-cache-dir -r requirements.txt