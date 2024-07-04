#Use python (version) container 
FROM python:3.9-slim

#Set working directory to /app
WORKDIR /app

#copy current directory contents into the container
COPY . /app
#install the dependencies
RUN pip install -r requirements.txt

#Port available
EXPOSE 5001

#Run app when container is launched
CMD ["python", "main.py"]
