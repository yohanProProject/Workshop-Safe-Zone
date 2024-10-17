from flask import request, Blueprint,  jsonify, current_app
from api.database.model import Level, db
levels_root = Blueprint("levels", __name__)

@levels_root.route("/")
def get_levels():
    return {"levels": [level.to_dict() for level in Level.query.all()]}

@levels_root.route("/", methods=["POST"])
def post_level():
    name = "level"
    try:
        return {**Level.create(request.json).to_dict(), **{name: "successfully added"}}
    except Exception as err:
        return jsonify({name:  f"cannot create new {name} {str(err)}"}), 400
