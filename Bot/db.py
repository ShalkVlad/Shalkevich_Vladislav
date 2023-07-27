from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db_file = 'users.db'
db_url = f'sqlite:///{db_file}'
engine = create_engine(db_url, echo=False)

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)
    city = Column(String, nullable=False)
    country = Column(String)
    about = Column(Text)
    photo = Column(Text)
    wallet = Column(Integer, default=0)


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def is_user_registered(user_id: int) -> bool:
    user = session.query(User).filter_by(id=user_id).first()
    return user is not None


def create_profile(user_id: int, name: str, age: int, gender: str, country: str, about: str, photo: str, city: str):
    user = User(id=user_id, name=name, age=age, gender=gender,
                country=country, about=about, photo=photo, city=city)
    session.add(user)
    session.commit()


def update_user_name(user_id: int, name: str):
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        user.name = name
        session.commit()
        return True
    return False


def update_user_age(user_id: int, age: int):
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        user.age = age
        session.commit()
        return True
    return False


def update_user_country(user_id: int, country: str):
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        user.country = country
        session.commit()
        return True
    return False


def update_user_about(user_id: int, about: str):
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        user.about = about
        session.commit()
        return True
    return False


async def update_user_photo(user_id: int, photo: str):
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        user.photo = photo
        session.commit()
        return True
    return False


async def update_user_city(user_id: int, city: str):
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        user.city = city
        session.commit()
        return True
    return False


def get_profile(user_id: int):
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        return user.name, user.age, user.gender, user.country, user.about, user.photo, user.wallet,user.city
    else:
        return None


def get_all_profiles():
    return session.query(User).all()


def delete_profile(user_id: int):
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        session.delete(user)
        session.commit()


def get_user_wallet(user_id: int):
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        return user.wallet
    else:
        return None

def get_user_City(user_id: int):
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        return user.city
    else:
        return None



def close_db():
    session.close()
