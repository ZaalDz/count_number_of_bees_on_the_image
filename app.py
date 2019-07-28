from flask import Flask, request
from flask import jsonify
from flask_cors import CORS
from flask_restplus import Api
from uuid import uuid4
from flask_restplus import Resource
import requests
from model import count_bees_from_binary_image

app = Flask(__name__)
CORS(app)

api = Api(app, prefix="/api", version="1.0")


@api.route("/input")
class Input(Resource):

    def post(self):
        print("request post")

    def get(self):
        url = request.args.get("image_url")
        if not url:
            return "Url not found", 404
        response = requests.get(url)
        binary_image = response.content

        number_of_bees = count_bees_from_binary_image(binary_image)
        return jsonify({"number_of_bees": number_of_bees,
                        "request_id": uuid4().hex})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
