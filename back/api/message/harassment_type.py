from flask import request, Blueprint,  jsonify, current_app
from api.database.model import HarassmentType, db
harassment_types_root = Blueprint("harassment_type", __name__)

@harassment_types_root.route("/")
def get_levels():
    return {"harassment_types": [harassment_type.to_dict() for harassment_type in HarassmentType.query.all()]}

@harassment_types_root.route("/", methods=["POST"])
def post_harassment_type():
    name = "harassment_type"
    try:
        return {**HarassmentType.create(request.json).to_dict(), **{name: "successfully added"}}
    except Exception as err:
        return jsonify({name:  f"cannot create new {name} {str(err)}"}), 400