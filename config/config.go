package config

import (
	"os"

	"github.com/joho/godotenv"
)

type Config struct {
	Token            string
	PostgresHost     string
	PostgresPort     string
	PostgresUser     string
	PostgresPassword string
	PostgresDB       string
	AppPort          string
	MongoDB          string
	MongoUser        string
	MongoPassword    string
}

func LoadConfig() (*Config, error) {
	if err := godotenv.Load(); err != nil {
		return nil, err
	}

	return &Config{
		PostgresHost:     os.Getenv("POSTGRES_HOST"),
		PostgresPort:     os.Getenv("POSTGRES_PORT"),
		PostgresUser:     os.Getenv("POSTGRES_USER"),
		PostgresPassword: os.Getenv("POSTGRES_PASSWORD"),
		PostgresDB:       os.Getenv("POSTGRES_DB"),
		AppPort:          os.Getenv("APP_PORT"),
		MongoDB:          os.Getenv("MONGO_DB"),
		MongoUser:        os.Getenv("MONGO_USER"),
		MongoPassword:    os.Getenv("MONGO_PASSWORD"),
	}, nil
}
