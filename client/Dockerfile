FROM nginx:stable

RUN rm /etc/nginx/nginx.conf /etc/nginx/conf.d/default.conf

COPY /client/static /usr/share/nginx/html
COPY /client/nginx.conf /etc/nginx/nginx.conf