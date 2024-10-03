from locust import HttpUser, task, between

class BeerApiTest(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        new_beer_body = {
            "BeerID": 171,
            "Name": "Brooklyn Sorachi Ace",
            "URL": "/homebrew/recipe/view/190892/brooklyn-sorachi-ace",
            "Style": "Saison",
            "StyleID": 134,
            "Size(L)": 18.93,
            "OG": 1.082,
            "FG": 1.013,
            "ABV": 9.1,
            "IBU": 0,
            "Color": 4.1,
            "BoilSize": 21.58,
            "BoilTime": 60,
            "BoilGravity": 2,
            "Efficiency": 72,
            "MashThickness": 2,
            "SugarScale": "Specific Gravity",
            "BrewMethod": "All Grain",
            "PitchRate": 2,
            "PrimaryTemp": 2,
            "PrimingMethod": 2,
            "PrimingAmount": 2,
            "UserId": 100
        }
        self.new_beer_body = new_beer_body
        response= self.client.post("/insert_beer", json=new_beer_body)
        if 'inserted_id' in response.json():
            self.beer_id = str(response.json()['inserted_id'])
        else:
            print('Inserted id not found')

    @task
    def test_insert_beers(self):
        second_beer = self.new_beer_body.copy()
        second_beer['BeerID'] = 172
        second_beer['Name'] = 'Second Broklyn Sorachi Ace'
        self.client.post("/insert_beers", json=[self.new_beer_body, second_beer])

    @task
    def test_get_beers(self):
        self.client.get("/get_beers")

    @task
    def test_get_beer(self):
        self.client.get(f"/get_beer/{self.beer_id}")

    @task
    def test_update_beer(self):
        new_beer_body = {
            "Name": "Brooklyn Updated Ace",
            "SugarScale": "Updated Specific Gravity",
            "BrewMethod": "Updated All Grain",
        }
        self.client.patch(f"/update_beer/{self.beer_id}", json=new_beer_body)
