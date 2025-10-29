FROM node:18-alpine
WORKDIR /app
COPY package*.json .
RUN npm ci
COPY . .
RUN adduser -S sallam -u 1001 && \
    addgroup -S sallam -g 1001 && \
    chown -R sallam:sallam /app/
USER sallam
EXPOSE 3000
ENTRYPOINT ["node"]
CMD [ "app.js" ]