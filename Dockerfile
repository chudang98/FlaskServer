FROM python:3.8-alpine

# copy the requirements file into the image
COPY ./requirements.txt /app/requirements.txt

# switch working directory
WORKDIR /app

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

# copy every content from the local file to the image
COPY . /app

EXPOSE 5000
# configure the container to run in an executed manner
ENTRYPOINT [ "flask"]

CMD ["--app", "app", "--debug", "run", "--host", "0.0.0.0", "-p", "443"]
#CMD ["--app", "app", "--debug", "run"]

#ENV GROUP_ID=1000 \
#    USER_ID=1000
#
#WORKDIR /var/www/
#
#ADD ./requirements.txt /var/www/requirements.txt
#RUN pip install -r requirements.txt
#ADD . /var/www/
#RUN pip install gunicorn
#
#RUN addgroup -g $GROUP_ID www
#RUN adduser -D -u $USER_ID -G www www -s /bin/sh
#
#USER www
#
#EXPOSE 5000
#
#CMD [ "gunicorn", "-w", "4", "--bind", "0.0.0.0:5000", "wsgi"]