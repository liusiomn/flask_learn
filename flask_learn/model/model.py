from ..extensions import db
from sqlalchemy.sql import and_
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class DBUser(db.Model):
    __tablename__ = 't_flask_learn_user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class DBGuild(db.Model):
    __tablename__ = 't_flask_learn_guild'
    id = db.Column(db.Integer, primary_key=True)
    guild_name = db.Column(db.String(128), unique=True, index=True, nullable=True, default='')
    country_code = db.Column(db.Integer, index=True, nullable=True, default=0)
    skill_points = db.Column(db.Integer, index=True, nullable=True, default=0)

    @property
    def players(self):
        return [player.id for player in DBPlayer.query.filter(DBPlayer.guild_id == self.id).all()]

    @property
    def items(self):
        nested = [player.items for player in DBPlayer.query.filter(DBPlayer.guild_id == self.id).all()]
        return [x for sublist in nested for x in sublist]
    

    @property
    def skill_points_dif_by_picking_item(self):
        skill_points = 0
        for item in self.items:
            count = self.items.count(item)
            point = DBItem.query.filter(DBItem.id==item).first().skill_points
            skill_points = skill_points + (point - point*(count-1))
        return skill_points
    
    @property
    def skill_points(self):
        skill_points = self.skill_points + self.skill_points_dif    
        return skill_points                

    def __repr__(self):
        return '<Player %s>' % self.guild_name
    

class DBPlayer(db.Model):
    __tablename__ = 't_flask_learn_player'
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(128), unique=True, index=True, default='')
    email = db.Column(db.String(128), unique=True, index=True, default='')
    skill_points = db.Column(db.Integer, index=True, nullable=True, default=0)
    guild_id = db.Column(db.Integer, index=True, nullable=True, default=0)
    regist_date = db.Column(db.Date, nullable=False, default=datetime.now)
    
    def __repr__(self):
        return '<Player %s>' % self.nickname

    @property
    def items(self):
        return [item.id for item in DBItem.query.join(DBPlayerItem, and_(DBPlayerItem.item_id==DBItem.id)) \
                    .join(DBPlayer, and_(DBPlayerItem.player_id==DBPlayer.id)).all()]


class DBPlayerItem(db.Model):
    __tablename__ = 't_flask_learn_play_item'
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, index=True)
    item_id = db.Column(db.Integer, index=True)
    
class DBItemsCount(db.Model):
    __tablename__ = 't_flask_learn_item_count'
    id = db.Column(db.Integer, primary_key=True)
    guild_id = db.Column(db.Integer, index=True)
    item_id = db.Column(db.Integer, index=True)
    item_count = db.Column(db.Integer, index=True, default = 0)    


class DBItem(db.Model):
    __tablename__ = 't_flask_learn_item'
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(128), unique=True, index=True, nullable=False)
    skill_points = db.Column(db.Integer, index=True, nullable=True, default=0)

    def __repr__(self):
        return '<Player %s>' % self.item_name
    
  
