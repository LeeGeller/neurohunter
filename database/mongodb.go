package database

import (
	"context"
	"neurohunter/model"

	"go.mongodb.org/mongo-driver/v2/bson"
	"go.mongodb.org/mongo-driver/v2/mongo"
	"go.mongodb.org/mongo-driver/v2/mongo/options"
)

type MongoDB struct {
	client     *mongo.Client
	collection *mongo.Collection
}

func ConnectMongoDB(uri string) (*MongoDB, error) {
	client, err := mongo.Connect(
		options.Client().ApplyURI(uri),
	)

	if err != nil {
		return nil, err
	}

	err = client.Ping(context.Background(), nil)

	if err != nil {
		return nil, err
	}

	collection := client.
		Database("neurohunter").
		Collection("vacancies")

	return &MongoDB{
		client:     client,
		collection: collection,
	}, nil
}

func (db *MongoDB) SaveVacancy(vacancies []model.Vacancy) error {
	for _, vacancy := range vacancies {

		filter := bson.M{
			"_id": vacancy.ID,
		}

		update := bson.M{
			"$set": vacancy,
		}

		opts := options.UpdateOne().SetUpsert(true)

		_, err := db.collection.UpdateOne(
			context.Background(),
			filter,
			update,
			opts,
		)

		if err != nil {
			return err
		}
	}

	return nil
}

func (db *MongoDB) Disconnect(ctx context.Context) error {
	return db.client.Disconnect(ctx)
}
