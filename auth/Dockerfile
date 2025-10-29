# ---------- Build Stage ----------
FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN go build -o app ./main

# ---------- Run Stage ----------
FROM alpine:3.20
RUN apk --no-cache add ca-certificates
RUN adduser -S sallam
USER sallam
WORKDIR /app
COPY --from=builder /app/app .
EXPOSE 8080
CMD ["./app"]