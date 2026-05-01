# Build Stage
FROM golang:1.22-alpine as builder

WORKDIR /app

COPY worker-runtime/go.mod worker-runtime/go.sum ./
RUN go mod download

COPY worker-runtime/ ./
RUN CGO_ENABLED=0 GOOS=linux go build -o worker-runtime .

# Final Stage
FROM ubuntu:22.04

WORKDIR /app

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /app/worker-runtime .
COPY agents /app/agents

CMD ["./worker-runtime"]
