from flask import request, Blueprint,  jsonify, current_app
from api.database.model import Platform, db
platforms_root = Blueprint("platform", __name__)

@platforms_root.route("/")
def get_platforms():
    return {"platforms": [platform.to_dict() for platform in Platform.query.all()]}

@platforms_root.route("/", methods=["POST"])
def post_platform():
    name = "platform"
    try:
        return {**Platform.create(request.json).to_dict(), **{name: "successfully added"}}
    except Exception as err:
        return jsonify({name:  f"cannot create new {name} {str(err)}"}), 400