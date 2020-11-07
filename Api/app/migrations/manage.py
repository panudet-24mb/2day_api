#$ python manage.py db init
# $ python manage.py db migrate
# $ python manage.py db upgrade
# $ python manage.py db --help


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from sqlalchemy.dialects.postgresql import JSON , UUID
import datetime, pytz

tz = pytz.timezone('Asia/Bangkok')
now = datetime.datetime.now(tz)
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/2day_api?user=postgres&password=Passw0rd_2020'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

# class company(db.Model):
#     conmpany_id = db.Column(db.Integer, primary_key=True)
#     company_uuid = db.Column(UUID(as_uuid=True) )
#     company_name = db.Column(db.String(128))
class users(db.Model):
    users_id = db.Column(db.Integer, primary_key=True)
    users_uuid = db.Column(UUID(as_uuid=True) )
    users_citizen_id = db.Column(db.String(14))
class token(db.Model):
    token_id = db.Column(db.Integer, primary_key=True)
    users_id = db.Column(db.ForeignKey('users.users_id'))
    token = db.Column(db.String(230))
    token_created = db.Column( db.DateTime, index=True, default=now)
    token_active = db.Column(db.Boolean, default=True, nullable=False)
    
    
# class participants(db.Model):
#     participants_id = db.Column(db.Integer, primary_key=True)
#     users_public_id = db.Column(UUID(as_uuid=True))
#     conversation_id = db.Column(db.ForeignKey('conversation.conversation_id'))
# class payload(db.Model):
#     payload_id = db.Column(db.Integer, primary_key=True)
#     users_public_id = db.Column(UUID(as_uuid=True))
#     conversation_id = db.Column(db.ForeignKey('conversation.conversation_id'))
#     payload_message = db.Column(JSON)
#     payload_timestamp = db.Column( db.DateTime, index=True, default=now)
# class conversation_lastseen(db.Model):
#     conversation_lastseen_id = db.Column(db.Integer, primary_key=True)
#     conversation_id = db.Column(db.ForeignKey('conversation.conversation_id'))
#     users_public_id = db.Column(UUID(as_uuid=True))
#     timestamp = db.Column( db.DateTime, index=True, default=now)
    

if __name__ == '__main__':
    manager.run()