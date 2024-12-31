from sqlalchemy import Column, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from DB import db_url

Base = declarative_base()


class Like(Base):
    __tablename__ = 'likes'
    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, nullable=False)
    recipient_id = Column(Integer, nullable=False)
    mutual = Column(Integer, default=0)


engine = create_engine(db_url, echo=False)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def get_unanswered_sympathy(user_id: int):
    unanswered_sympathy = session.query(Like).filter_by(sender_id=user_id, mutual=0).all()
    return [like.recipient_id for like in unanswered_sympathy]


def get_users_unanswered_sympathy(user_id: int):
    users_unanswered_sympathy = session.query(Like).filter_by(recipient_id=user_id, mutual=0).all()
    return [like.sender_id for like in users_unanswered_sympathy]


def get_pending_sympathy(user_id: int):
    pending_sympathy = session.query(Like).filter_by(recipient_id=user_id, mutual=0).all()
    return [like.sender_id for like in pending_sympathy]


def add_like(sender_id: int, recipient_id: int):
    like = Like(sender_id=sender_id, recipient_id=recipient_id)
    session.add(like)
    session.commit()


def set_mutual_like(user_id: int, sender_id: int):
    like = session.query(Like).filter_by(sender_id=user_id, recipient_id=sender_id).first()
    if like:
        like.mutual = 1
        session.commit()


def is_mutual_like(user_id: int, sender_id: int) -> bool:
    like = session.query(Like).filter_by(sender_id=user_id, recipient_id=sender_id, mutual=1).first()
    return like is not None


def has_mutual_like(user_id: int, other_user_id: int) -> bool:
    return is_mutual_like(user_id, other_user_id) and is_mutual_like(other_user_id, user_id)


# Функция для получения списка пользователей, которые взаимно симпатичны с данным пользователем
def get_mutually_liked_users(user_id: int):
    sent_mutual_sympathy = session.query(Like).filter_by(sender_id=user_id, mutual=1).all()
    received_mutual_sympathy = session.query(Like).filter_by(recipient_id=user_id, mutual=1).all()

    mutually_liked_users = set()

    for like in sent_mutual_sympathy:
        mutually_liked_users.add(like.recipient_id)

    for like in received_mutual_sympathy:
        mutually_liked_users.add(like.sender_id)

    return list(mutually_liked_users)


# Функция для получения списка пользователей, на которых пользователь отправил симпатию и получил ответ
def get_mutual_sympathy(user_id: int):
    mutual_sympathy = session.query(Like).filter_by(sender_id=user_id, mutual=1).all()
    return [(like.recipient_id, like.sender_id) for like in mutual_sympathy]


# Функция для перемещения непрочитанных симпатий в взаимные
def move_pending_to_mutual(user_id: int):
    # Выбираем записи, где текущий пользователь является отправителем симпатии
    pending_sympathy_entries = session.query(Like).filter_by(sender_id=user_id, mutual=0).all()

    # Обновляем записи, помечая их как взаимные симпатии
    for entry in pending_sympathy_entries:
        entry.mutual = 1

    session.commit()
    return True


def delete_mutual_sympathy(user_id: int, other_user_id: int):
    # Delete mutual sympathy entries for both users
    session.query(Like).filter_by(sender_id=user_id, recipient_id=other_user_id).delete()
    session.query(Like).filter_by(sender_id=other_user_id, recipient_id=user_id).delete()
    session.commit()


def delete_sympathy_entry(user_id: int, other_user_id: int):
    # Delete unanswered sympathy entry for the given user pair
    session.query(Like).filter_by(sender_id=user_id, recipient_id=other_user_id, mutual=0).delete()
    session.commit()
