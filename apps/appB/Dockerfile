FROM golang:latest
LABEL org.opencontainers.image.authors="dejanualex@gmail.com"
WORKDIR /app


# # pre-copy/cache go.mod for pre-downloading dependencies and only redownloading them in subsequent builds if they change
# COPY go.mod go.sum ./
# RUN go mod download && go mod verify

COPY . /app
RUN go build -o main .
EXPOSE 8888
CMD ["/app/main"]