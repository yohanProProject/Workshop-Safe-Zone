from flask import request, Blueprint,  jsonify, current_app
from api.database.model import Message, Target, Platform, db
messages_root = Blueprint("messages", __name__)

@messages_root.route("/")
def get_messages():
    return {"messages": [message.to_dict() for message in Message.query.all()]}

@messages_root.route("/by_stalker")
def get_message_by_stalker():
    return {
        target.name: [
            message.to_dict()
            for message in Message.query.filter_by(stalker_id=target.id)
        ]
        for target in Target.query.all()
    }

@messages_root.route("/by_stalker_platform")
def get_message_by_stalker_platform():
    stalker_name = request.args.get("username")
    platform_id = request.args.get("platform")
    messages_query = Message.query if not platform_id else Message.query.filter_by(platform_id=int(platform_id))
    messages = messages_query.join(Target, Message.stalker_id == Target.id)\
                            .join(Platform, Message.platform_id == Platform.id).all()

    return {
        f'{message.target.name} sur {message.platform.name}': [
            message.to_dict() for message in Message.query.filter_by(stalker_id=message.stalker_id, platform_id=message.platform_id)
        ]
        for message in messages if not stalker_name or message.target.name == stalker_name
    }

@messages_root.route("/", methods=["POST"])
def post_messages():
    try:
        return {**Message.create(request.json).to_dict(), **{"message": "successfully added", "success": True}}
    except Exception as err:
        return jsonify({"message":  f"cannot create new message {str(err)}"}), 400