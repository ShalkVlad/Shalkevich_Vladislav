from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

db_file = 'users.db'
db_url = f'sqlite:///{db_file}'
engine = create_engine(db_url, echo=False)

Base = declarative_base()


class UserPhoto(Base):
    __tablename__ = 'user_photos'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    file_id = Column(String)  # Идентификатор файла фотографии


# Определение таблицы UserPreferences
class UserPreferences(Base):
    __tablename__ = 'user_preferences'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True, nullable=False)
    preferred_gender = Column(String)
    preferred_age_min = Column(Integer)
    preferred_age_max = Column(Integer)
    preferred_country = Column(String)
    preferred_city = Column(String)
    user_type = Column(String)
    preferred_type = Column(String)
    confirmed = Column(Boolean, default=False)
    bonus1 = Column(Integer, default=0)
    bonus2 = Column(Integer, default=0)
    bonus3 = Column(Integer, default=0)
    bonus4 = Column(Integer, default=0)
    bonus5 = Column(Integer, default=0)

    user = relationship("User", back_populates="preferences")


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    # Остальные поля пользователя

    # Связь с предпочтениями пользователя
    preferences = relationship("UserPreferences", back_populates="user")


# Создание таблиц в базе данных
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def save_user_preferences(user_id: int, preferences: dict):
    print("Saving user preferences:", preferences)
    user_preferences = UserPreferences(
        user_id=user_id,
        preferred_gender=preferences.get("gender"),
        preferred_age_min=preferences.get("min_age"),
        preferred_age_max=preferences.get("max_age"),
        preferred_country=preferences.get("country"),
        preferred_city=preferences.get("city"),
        user_type=preferences.get("user_type"),
        preferred_type=preferences.get("type"),
        confirmed=preferences.get("confirmed", False),  # Добавьте значение по умолчанию
        bonus1=preferences.get("bonus1", 0),
        bonus2=preferences.get("bonus2", 0),
        bonus3=preferences.get("bonus3", 0),
        bonus4=preferences.get("bonus4", 0),
        bonus5=preferences.get("bonus5", 0)
    )
    session.add(user_preferences)

    # Обновление статуса подтверждения
    session.commit()

    # также обновляем статус подтверждения в связанной таблице
    if preferences.get("confirmed"):
        user = session.query(User).filter_by(id=user_id).first()
        if user and user.preferences:
            user.preferences[0].confirmed = True
            session.commit()


def update_user_photo(user_id: int, photo: str):
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        user.photo = photo
        session.commit()


def get_user_preferences(user_id: int):
    user = session.query(User).filter_by(id=user_id).first()
    if user and user.preferences:
        return user.preferences[0]  # Возвращаем первый объект UserPreferences
    return None


def save_user_photo(user_id: int, photo_file_id: str):
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        user_photo = UserPhoto(user_id=user_id, file_id=photo_file_id)
        session.add(user_photo)
        session.commit()


def get_user_photo(user_id: int):
    user_photo = session.query(UserPhoto).filter_by(user_id=user_id).first()
    if user_photo:
        return user_photo.file_id
    return None


def update_user_preference(user_id: int, preferences: dict):
    user_pref = get_user_preferences(user_id)
    if user_pref:
        for key, value in preferences.items():
            setattr(user_pref, key, value)
        session.commit()
        return True
    return False


def update_user_photo_file_id(user_id: int, photo_file_id: str):
    user_photo = session.query(UserPhoto).filter_by(user_id=user_id).first()
    if user_photo:
        user_photo.file_id = photo_file_id
        session.commit()


def close_db():
    session.close()
