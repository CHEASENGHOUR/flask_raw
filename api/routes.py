from . import api

@api.route("/", methods=["GET"])
def api_home():
    return {
        "message": "Welcome to the API root"
    }