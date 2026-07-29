FROM golang:1.26

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY . .

RUN apt-get update && apt-get install -y \
    libnss3 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libgbm1 \
    libasound2 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libxfixes3 \
    libxkbcommon0 \
    libgobject-2.0-0 \
    && rm -rf /var/lib/apt/lists/*

RUN go build -o main .

EXPOSE 8000

CMD ["./main"]
