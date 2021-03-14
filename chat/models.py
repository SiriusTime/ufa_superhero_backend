import asyncio

from gino import Gino

from local_settings import DATABASE


db = Gino()


class Profile(db.Model):
    __tablename__ = 'profile'

    id = db.Column(db.Integer(), primary_key=True)
    password = db.Column()
    email = db.Column()


async def connect():
    await db.set_bind('postgresql://{}:{}@{}/{}'.format(
        DATABASE["USERNAME"], DATABASE["PASSWORD"], DATABASE["HOST"], DATABASE["NAME"]
    ))

asyncio.get_event_loop().run_until_complete(connect())