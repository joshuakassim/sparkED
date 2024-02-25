from config import db
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import check_password_hash, generate_password_hash


class User(db.Model):
    __tablename__ = 'user'

    # Attributes
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)

    def __init__(self, name, username, password):
        self.name = name
        self.username = username
        self.set_password(password)

    # Representation of user
    def __repr__(self):
        return f"User('{self.name}, {self.username}, {self.password}')"

    # Convert user information to JSON
    def to_json(self):
        return {
            "id":  self.id,
            "name": self.name,
            "username": self.username,
            "password": self.password
        }

    # Ensure saved password and entered passwords match
    def passwords_match(self, password):
        return check_password_hash(self.password, password)

    # Set the users password
    def set_password(self, password):
        self.password = generate_password_hash(password)


class Flashcard(db.Model):
    __tablename__ = 'flashcard'

    # Attributes
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    question: Mapped[str] = mapped_column(String(500), nullable=False)
    answer: Mapped[str] = mapped_column(String(500), nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, db.ForeignKey('user.id'),  nullable=False)