from bson import ObjectId
from flask import Flask, request, jsonify, Response, json
from flask_restx import Api, fields, Resource

from beerModels import beer_schema, beer_response_schema, delete_response_schema
from dbConnection import start_db_connection

app = Flask(__name__)
app.config.SWAGGER_UI_DOC_EXPANSION = 'list'
app.config['RESTX_MASK_SWAGGER'] = False
api = Api(app, version='1.0', title='Beer API', description='Beer recipes', doc='/swagger',
          default_swagger_filename='Beer Operations', default="Beer recipe operations", default_label="Beer recipes")


# Connects to db
db, collection = start_db_connection()

# models
beer_model = api.model('Beer', beer_schema)
beer_model_response = api.model('BeerResponse', beer_response_schema)
delete_model_response = api.model('DeleteResponse', delete_response_schema)


# posts multiple beers
@api.route('/insert_beers', endpoint='insert_beers')
@api.doc(description='Handles inserting multiple beers to the database',
         responses={200: "Beers inserted successfully!", 400: "Error inserting beers!"})
class InsertBeers(Resource):
    @api.expect([beer_model])
    def post(self):
        try:
            data = request.get_json()

            if isinstance(data, list) and all(isinstance(item, dict) for item in data):
                result = collection.insert_many(data)
                return Response(
                    response=json.dumps(
                        {"message": "Beers inserted successfully!", 'inserted_ids': str(result.inserted_ids)}),
                    status=200,
                    mimetype="application/json"
                )
            return Response(
                response=json.dumps(
                    {"message": "Error inserting beers!"}),
                status=400,
                mimetype="application/json"
            )

        except Exception as ex:
            return jsonify({'error': str(ex)}), 500


# posts 1 beer
@api.route('/insert_beer', endpoint='insert_beer')
@api.doc(description="Handles inserting one beer recipe to the database",
         responses={200: "Beer posted successfully!", 400: "Beer recipe can't be inserted"})
class InsertBeer(Resource):
    @api.expect(beer_model, validate=False)
    def post(self):
        try:
            data = request.get_json()

            if isinstance(data, dict):
                result = collection.insert_one(data)
                return Response(
                    response=json.dumps(
                        {"message": "Beer posted successfully!", 'inserted_id': str(result.inserted_id)}),
                    status=200,
                    mimetype="application/json"
                )
            else:
                return Response(
                    response=json.dumps({"message": "Beer can't be inserted"}),
                    status=400,
                    mimetype="application/json"
                )
        except Exception as ex:
            return Response(
                response=json.dumps({"message": f"Error inserting beer recipe: {ex} "}),
                status=400,
                mimetype="application/json"
            )


# Gets all beers
@api.route('/get_beers', endpoint='/get_beers')
@api.doc(description='Gets all beers from the database',
         responses={200: "Beer posted successfully!", 500: "Get All beers failed"})
class GetAllBeers(Resource):
    @api.marshal_with(beer_model_response, as_list=True)
    def get(self):
        try:
            response = list(collection.find())

            for item in response:
                item["_id"] = str(item["_id"])

            return response
        except Exception as ex:
            print(ex)
            return Response(
                response=json.dumps({"message": "Get All beers failed"}),
                status=500,
                mimetype="application/json"
            )


# Gets one beer
@api.route('/get_beer/<beer_id>', endpoint='/get_beer')
@api.doc(description='Gets one beer from database',
         responses={500: "Get Beer failed"})
class GetBeer(Resource):
    @api.marshal_with(beer_model_response)
    def get(self, beer_id):
        try:
            obj_id = ObjectId(beer_id)
            response = collection.find_one({"_id": obj_id})

            return response
        except Exception as ex:
            return Response(
                response=json.dumps({f"{ex} message": "Get Beer failed"}),
                status=400,
                mimetype="application/json"
            )


# Updates one beer
@api.route("/update_beer/<beer_id>",  endpoint='/update_beer')
@api.doc(description='Updates one beer from database',
         responses={200: "Beer updated successfully", 500: "Can't update beer", 404: "Beer not found"})
class UpdateBeer(Resource):
    @api.expect(beer_model, validate=False)
    def patch(self, beer_id):
        try:

            data = request.get_json()
            updated_beer = {
                "$set": {
                    "Name": data.get("Name"),
                }
            }
            response = collection.update_one({"_id": ObjectId(beer_id)}, updated_beer)
            if response.modified_count > 0:
                return Response(
                    response={json.dumps({"message": "Beer updated successfully"})},
                    status="200",
                    mimetype="application/json"
                )
            return Response(
                response={json.dumps({"message": "Beer not found"})},
                status="404",
                mimetype="application/json"
            )

        except Exception as ex:
            print(ex)
            return Response(
                response=json.dumps({"message:": "Can't update beer"}),
                status=500,
                mimetype="application/json"
            )


# deletes one beer
@api.route("/delete_beer/<beer_id>", endpoint='/delete_beer')
@api.doc(description='Deletes one beer from the database',
         responses={
                    500: "Beer can't be deleted",
                    404: "Beer not found: beer_id"})
class DeleteBeer(Resource):
    @api.response(200, "Delete model", delete_model_response)
    def delete(self, beer_id):
        try:
            response = collection.delete_one({"_id": ObjectId(beer_id)})

            if response.deleted_count > 0:
                return Response(
                    response=json.dumps({"message": "Beer deleted successfully", "id": beer_id}),
                    status=200,
                    mimetype="application/json"
                )
            return Response(
                response=json.dumps({"message": "Beer not found", "id": beer_id}),
                status=404,
                mimetype="application/json"
            )
        except Exception as ex:
            print(ex)
            return Response(
                response=json.dumps({"message": "Beer can't be deleted"}),
                status=500,
                mimetype="application/json"
            )


if __name__ == '__main__':
    app.run(debug=True)
