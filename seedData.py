import pandas as pd


from dbConnection import start_db_connection

db, collection = start_db_connection()


def dataset_to_dict(file_path):
    beerRecipes = []
    try:
        df = pd.read_csv(file_path, encoding='latin-1')
        beerRecipes = df.to_dict(orient='records')

    except FileNotFoundError:
        print("File could not be found")
        return []
    except UnicodeDecodeError:
        print("There was an error reading from the file")
        return []
    print("Database seeded effectively")
    return beerRecipes


def seed_database():
    try:
        beerDict = dataset_to_dict('recipeData.csv')
        collection.insert_many(beerDict)
    except Exception as ex:
        print(f"An error occurred while seeding: {ex}")


if __name__ == "__main__":
    seed_database()
