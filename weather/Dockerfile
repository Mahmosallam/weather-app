FROM python:alpine3.21
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY main.py .
RUN adduser -S sallam -u 1001 && \
    addgroup -S sallam -g 1001 && \
    chown -R sallam:sallam /app/
USER sallam
EXPOSE 5000
ENTRYPOINT ["python3"]
CMD [ "/app/main.py" ]