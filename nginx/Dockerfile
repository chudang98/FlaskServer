FROM alpine:latest

# RUN rm /etc/nginx/conf.d/default.conf
RUN ./app.conf /etc/nginx/conf.d/app.conf

COPY ./app.conf /etc/nginx/conf.d/app.conf

EXPOSE 80 443
CMD ["nginx", "-g", "daemon off;"]