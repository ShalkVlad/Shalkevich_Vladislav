from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db_file = 'users.db'
db_url = f'sqlite:///{db_file}'
engine = create_engine(db_url, echo=False)

Base = declarative_base()


class Profile:
    def __init__(self, name, age, gender, country, about, photo, wallet, city, telegram_username):
        self.name = name
        self.age = age
        self.gender = gender
        self.country = country
        self.about = about
        self.photo = photo
        self.wallet = wallet
        self.city = city
        self.telegram_username = telegram_username


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
    telegram_username = Column(String)
    language = Column(String)


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def is_user_registered(user_id: int) -> bool:
    user = session.query(User).filter_by(id=user_id).first()
    return user is not None


def create_profile(user_id: int, name: str, age: int, gender: str, country: str, about: str, photo: str,
                   city: str, telegram_username: str, language: str):
    user = User(id=user_id, name=name, age=age, gender=gender,
                country=country, about=about, photo=photo, city=city, telegram_username=telegram_username,
                language=language)  # Добавляем параметр language
    session.add(user)
    session.commit()


async def update_user_photo(user_id: int, photo: str):
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        user.photo = photo
        session.commit()
        return True
    return False


async def update_user_language(user_id: int, language: str):
    update_data = {"language": language}
    result = await update_user_profile(user_id, update_data)
    return result


async def update_user_profile(user_id: int, update_data: dict):
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        for field, value in update_data.items():
            if hasattr(user, field):
                setattr(user, field, value)
            else:
                return False  # Недопустимое поле в update_data

        session.commit()
        return True
    else:
        return False


def get_profile(user_id: int):
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        return user.name, user.age, user.gender, user.country, user.about, user.photo, user.wallet, user.city,
    else:
        return None


def get_all_profiles():
    return session.query(User).all()


def delete_user_profile(user_id: int):
    # Удаляем профиль пользователя
    session.query(User).filter_by(id=user_id).delete()

    # Удаляем взаимные симпатии пользователя
    from likes import Like
    session.query(Like).filter_by(sender_id=user_id).delete()
    session.query(Like).filter_by(recipient_id=user_id).delete()

    session.commit()
    return True


def get_user_wallet(user_id: int):
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        return user.wallet
    else:
        return None


def update_profile(user_id: int, name: str, age: int, gender: str, country: str, about: str, photo: str,
                   city: str, telegram_username: str, language: str):
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        user.name = name
        user.age = age
        user.gender = gender
        user.country = country
        user.about = about
        user.photo = photo
        user.city = city
        user.telegram_username = telegram_username
        user.language = language
        session.commit()


def get_user(user_id: int):
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        return Profile(
            name=user.name,
            age=user.age,
            gender=user.gender,
            country=user.country,
            about=user.about,
            photo=user.photo,
            wallet=user.wallet,
            city=user.city,
            telegram_username=user.telegram_username
        )
    else:
        return None


def close_db():
    session.close()
