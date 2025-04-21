
FROM node:16-alpine
RUN npm install -g json-server

EXPOSE 5000

COPY db.json /data/db.json

CMD ["json-server", "--watch", "/data/db.json", "--host", "0.0.0.0", "--port", "5000"]
