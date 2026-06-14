package config

import (
	"os"
	"sync"

	"github.com/joho/godotenv"
)

type Config struct {
	Token string
}

var (
	config *Config
	once   sync.Once
)

func LoadConfig() (*Config, error) {
	godotenv.Load()

	once.Do(func() {
		config = &Config{
			Token: os.Getenv("HABR_TOKEN"),
		}
	})

	return config, nil
}
