from abc import ABC, abstractmethod
from .connection_db import db, app
from sqlalchemy.orm.exc import NoResultFound

class ModelSerializer:
    key_needed = None

    @classmethod
    def raise_incorrect_dict(self, new_data : dict) -> None:
        if not self.key_needed:
            raise TypeError("You need to precise key needed")
        keys_missing : list = []
        for key in new_data:
            if key in self.key_needed:
                if type(new_data[key]) != self.key_needed[key]:
                    raise TypeError(f"Invalid type [{key}] not an {self.key_needed[key]}")
                else:
                    keys_missing.append(key)
        keys_missing = [s for s in keys_missing if s not in self.key_needed]
        if keys_missing:
            missing_value = ", ".join([key_missing for key_missing in keys_missing])
            raise TypeError(f"Invalid key_needed not fulfil miss [{missing_value}]")

    @classmethod
    def create(self, new_data : dict):
        self.raise_incorrect_dict(new_data)
        new_product = self(**new_data)
        db.session.add(new_product)
        db.session.commit()
        return new_product

    def update(self, data):
        for key, value in data.items():
            if getattr(self, key):
                setattr(self, key, value)
        db.session.commit()
        return self

    def to_dict(self) -> dict:
        pass

class HarassmentType(db.Model, ModelSerializer):
    __tablename__ = "harassment_type"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)

    key_needed = {
        "name": str,
    }

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
        }

class Level(db.Model ,ModelSerializer):
    __tablename__ = "level"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    testimonies_needed = db.Column(db.Integer)

    key_needed = {
        "name": str,
        "testimonies_needed": int
    }

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "testimonies_needed": self.testimonies_needed
        }

class Target(db.Model ,ModelSerializer):
    __tablename__ = "target"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)

    key_needed = {
        "name": str
    }

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name
        }

class Platform(db.Model ,ModelSerializer):
    __tablename__ = "platform"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(255))

    key_needed = {
        "name": str
    }

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "image": self.image
        }

class Message(db.Model ,ModelSerializer):
    __tablename__ = "message"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.Text)
    level_id = db.Column(db.Integer, db.ForeignKey('level.id'))
    stalker_id = db.Column(db.Integer, db.ForeignKey('target.id'))
    platform_id = db.Column(db.Integer, db.ForeignKey('platform.id'))
    harassment_type_id = db.Column(db.Integer, db.ForeignKey('harassment_type.id'))

    key_needed = {
        "description": str,
        "stalker_id" : int,
        "level_id": int,
        "harassment_type_id": int,
        "platform_id": int,
    }

    @property
    def target(self) -> Target:
        return Target.query.filter_by(id=self.stalker_id).one()

    @property
    def platform(self) -> Platform:
        return Platform.query.filter_by(id=self.platform_id).one()

    @property
    def harassment_type(self) -> HarassmentType:
        return HarassmentType.query.filter_by(id=self.harassment_type_id).one()

    @property
    def level(self) -> Level:
        return Level.query.filter_by(id=self.level_id).one()


    @classmethod
    def create(self, new_data):
        stalker_name = new_data.get("stalker_name", None)
        if not stalker_name:
            raise KeyError("Invalid json: stalker_name not set in json")
        try:
            target = Target.query.filter_by(name=stalker_name).one()
        except NoResultFound:
            target = Target.create({"name": stalker_name})
        new_data.pop("stalker_name")
        new_data["stalker_id"] = target.id

        return super().create(new_data)

    def __repr__(self):
        return f'<Message {self.target.name} - {self.description}>'

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "stalker_name": self.target.name,
            "description": self.description,
            "harassment_type_name": self.harassment_type.name,
            "level_name": self.level.name,
            "platform_name": self.platform.name
        }


# Créer les tables de la base de données
with app.app_context():
    db.create_all()