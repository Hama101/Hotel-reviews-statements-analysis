FROM python:3.9

# Environment Varaibles
ENV DISPLAY=:10
RUN apt-get update -y
RUN apt-get install -y python3-pip build-essential python3-dev nginx
RUN apt-get install -y 1ibasound2
RUN pip install -u gunicorn


# Make working directory
RUN mkdir /app
WORKDIR /app
ADD requirements.txt /app

# Install requirements
RUN pip install -r requirements.txt

# Copy project to docker work directory
ADD . /app
EXPOSE 5056

# Run the app
CMD ["gunicorn", "app:app"]