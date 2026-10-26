package database

import (
	"context"
	"neurohunter/models"

	"go.mongodb.org/mongo-driver/v2/bson"
	"go.mongodb.org/mongo-driver/v2/mongo"
	"go.mongodb.org/mongo-driver/v2/mongo/options"
)

type MongoDB struct {
	client                 *mongo.Client
	collection             *mongo.Collection
	vacancyUsersCollection *mongo.Collection
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

	vacancyUserCollection := client.
		Database("neurohunter").
		Collection("vacancy_users")

	return &MongoDB{
		client:                 client,
		collection:             collection,
		vacancyUsersCollection: vacancyUserCollection,
	}, nil
}

func (db *MongoDB) SaveVacancy(vacancies []models.Vacancy) error {
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

func (db *MongoDB) SaveVacancyUser(
	vacancyUsers []models.VacancyUser,
) error {
	for _, vacancyUser := range vacancyUsers {
		filter := bson.M{
			"vacancy_id": vacancyUser.VacancyID,
			"user_id":    vacancyUser.UserID,
		}

		update := bson.M{
			"$set": bson.M{
				"vacancy_id": vacancyUser.VacancyID,
				"user_id":    vacancyUser.UserID,
			},
		}

		opts := options.UpdateOne().SetUpsert(true)

		_, err := db.vacancyUsersCollection.UpdateOne(
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
