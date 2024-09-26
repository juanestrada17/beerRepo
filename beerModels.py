from flask_restx import fields


# Schema models
# TODO finish them with the correct types and validation
beer_schema = {
    'Name': fields.String(required=True, description='Been name', example="Sample Beer"),
}

beer_response_schema = {
    '_id': fields.String(description='Id of the beer', example='66eb21b2adf5db590529e5fe'),
    'Name': fields.String(required=True, description='Beer name', example="Sample beer"),
}

delete_response_schema = {
    'id': fields.String(description='Id of the beer deleted', example='66eb21b2adf5db590529e5fe'),
    'message': fields.String(description='Message of response', example='Beer deleted successfully')
}
