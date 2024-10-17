import unittest
from flask import Flask, json
from api.database.model import Message, Level, Target, Platform, HarassmentType, db
from api.message.message import messages_root
from api.message.level import levels_root
from api.message.harassment_type import harassment_types_root
from api.message.platform import platforms_root

def create_app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    app.register_blueprint(messages_root, url_prefix='/message')
    app.register_blueprint(levels_root, url_prefix="/level")
    app.register_blueprint(platforms_root, url_prefix="/platform")
    app.register_blueprint(harassment_types_root, url_prefix="/harassment_type")
    return app

def create_model_db(model):
    db.session.add(model)
    db.session.commit()
    return model

class TestMessageAPI(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
        self.ctx.pop()

    def test_post_message(self):
        level = create_model_db(Level(name="Moyen" ,testimonies_needed=3))
        platform = create_model_db(Platform(name="TikTok"))
        harassment_type = create_model_db(HarassmentType(name="CyberHarcelement"))

        message_data = {
            "description": "yohan is the bad guy",
            "stalker_name": "yohan",
            "level_id": level.id,
            "platform_id": platform.id,
            "harassment_type_id": harassment_type.id,
        }
        target = Target.query.filter_by(name="yohan").one_or_none()
        self.assertIsNone(target)
        response = self.client.post('/message/', json=message_data)
        if response.status_code == 400:
            data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'successfully added')
        self.assertEqual(str(Message.query.all()), "[<Message yohan - yohan is the bad guy>]")
        target = Target.query.filter_by(name="yohan").one_or_none()
        self.assertIsNotNone(target)
        message = Message.query.one_or_none()
        self.assertIsNotNone(message)
        self.assertEqual(message.platform_id, platform.id)
        self.assertEqual(message.level_id, level.id)
        self.assertEqual(message.harassment_type_id, harassment_type.id)

        # test another post message
        message_data = {
            "description": "il parle mal ce fou",
            "stalker_name": "yohan",
            "level_id": level.id,
            "platform_id": platform.id,
            "harassment_type_id": harassment_type.id,
        }
        response = self.client.post('/message/', json=message_data)
        if response.status_code == 400:
            data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(Message.query.all()), "[<Message yohan - yohan is the bad guy>, <Message yohan - il parle mal ce fou>]")



    def test_get_messages(self):
        stalker = create_model_db(Target(name="test name"))
        # stalker_2 = create_model_db(Target(name="test name 2"))
        level = create_model_db(Level(name="Moyen" ,testimonies_needed=3))
        platform = create_model_db(Platform(name="TikTok"))
        harassment_type = create_model_db(HarassmentType(name="CyberHarcelement"))

        message_one = Message(stalker_id=stalker.id, description="test get message", level_id=level.id, platform_id=platform.id, harassment_type_id=harassment_type.id)
        message_two = Message(stalker_id=stalker.id, description="test get message 2", level_id=level.id, platform_id=platform.id, harassment_type_id=harassment_type.id)
        db.session.add(message_one)
        db.session.add(message_two)
        db.session.commit()
        response = self.client.get('/message/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(data["messages"],
        [
            {
             'id': 1,
             'description': 'test get message',
             'stalker_name': 'test name',
             "level_name": "Moyen",
             "platform_name": "TikTok",
             "harassment_type_name": "CyberHarcelement"
            },
            {
             'id': 2,
             'description': 'test get message 2',
             'stalker_name': 'test name',
             "level_name": "Moyen",
             "platform_name": "TikTok",
             "harassment_type_name": "CyberHarcelement"
            },
        ])

    def test_get_message_by_stalker(self):
        stalker = create_model_db(Target(name="test name"))
        stalker2 = create_model_db(Target(name="test name 2"))
        level = create_model_db(Level(name="Moyen" ,testimonies_needed=3))
        platform = create_model_db(Platform(name="TikTok"))
        harassment_type = create_model_db(HarassmentType(name="CyberHarcelement"))

        message_one = Message(stalker_id=stalker.id, description="test get message", level_id=level.id, platform_id=platform.id, harassment_type_id=harassment_type.id)
        message_two = Message(stalker_id=stalker.id, description="test get message 2", level_id=level.id, platform_id=platform.id, harassment_type_id=harassment_type.id)
        message_tree = Message(stalker_id=stalker2.id, description="test get message 3", level_id=level.id, platform_id=platform.id, harassment_type_id=harassment_type.id)
        db.session.add(message_one)
        db.session.add(message_two)
        db.session.add(message_tree)
        db.session.commit()
        response = self.client.get('/message/by_stalker')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(data,
            {
                "test name": [
                    {
                        'id': 1,
                        'description': 'test get message',
                        'stalker_name': 'test name',
                        "level_name": "Moyen",
                        "platform_name": "TikTok",
                        "harassment_type_name": "CyberHarcelement"
                    },
                    {
                        'id': 2,
                        'description': 'test get message 2',
                        'stalker_name': 'test name',
                        "level_name": "Moyen",
                        "platform_name": "TikTok",
                        "harassment_type_name": "CyberHarcelement"
                    },
                ],
                "test name 2": [
                    {
                        'id': 3,
                        'description': 'test get message 3',
                        'stalker_name': 'test name 2',
                        "level_name": "Moyen",
                        "platform_name": "TikTok",
                        "harassment_type_name": "CyberHarcelement"
                    },
                ]
            }
        )

    def test_get_message_by_stalker_platform(self):
        stalker = create_model_db(Target(name="test name"))
        stalker2 = create_model_db(Target(name="test name 2"))
        level = create_model_db(Level(name="Moyen" ,testimonies_needed=3))
        platform = create_model_db(Platform(name="TikTok"))
        harassment_type = create_model_db(HarassmentType(name="CyberHarcelement"))

        message_one = Message(stalker_id=stalker.id, description="test get message", level_id=level.id, platform_id=platform.id, harassment_type_id=harassment_type.id)
        message_two = Message(stalker_id=stalker.id, description="test get message 2", level_id=level.id, platform_id=platform.id, harassment_type_id=harassment_type.id)
        message_tree = Message(stalker_id=stalker2.id, description="test get message 3", level_id=level.id, platform_id=platform.id, harassment_type_id=harassment_type.id)
        db.session.add(message_one)
        db.session.add(message_two)
        db.session.add(message_tree)
        db.session.commit()
        response = self.client.get('/message/by_stalker_platform')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(data,
            {
                "test name sur TikTok": [
                    {
                        'id': 1,
                        'description': 'test get message',
                        'stalker_name': 'test name',
                        "level_name": "Moyen",
                        "platform_name": "TikTok",
                        "harassment_type_name": "CyberHarcelement"
                    },
                    {
                        'id': 2,
                        'description': 'test get message 2',
                        'stalker_name': 'test name',
                        "level_name": "Moyen",
                        "platform_name": "TikTok",
                        "harassment_type_name": "CyberHarcelement"
                    },
                ],
                "test name 2 sur TikTok": [
                    {
                        'id': 3,
                        'description': 'test get message 3',
                        'stalker_name': 'test name 2',
                        "level_name": "Moyen",
                        "platform_name": "TikTok",
                        "harassment_type_name": "CyberHarcelement"
                    },
                ]
            }
        )

    def test_get_platforms(self):
        platform = create_model_db(Platform(name="Youtube", image="logo"))

        response = self.client.get('/platform/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(data["platforms"],
        [
            {
                "id": platform.id,
                "name": "Youtube",
                "image": "logo"
            }
        ])

    def test_get_levels(self):
        level = create_model_db(Level(name="Moyen", testimonies_needed=7))

        response = self.client.get('/level/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(data["levels"],
        [
            {
                "id": level.id,
                "name": "Moyen",
                "testimonies_needed": 7
            }
        ])

    def test_get_harassment_types(self):
        harassment_type = create_model_db(HarassmentType(name="CyberHarcelemnt"))

        response = self.client.get('/harassment_type/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(data["harassment_types"],
        [
            {
                "id": harassment_type.id,
                "name": "CyberHarcelemnt",
            }
        ])