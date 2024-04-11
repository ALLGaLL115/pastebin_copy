from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import VARCHAR, Column, INTEGER, String

from database import Base

class User(Base):
    __tablename__="users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)  
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(nullable=False)


class Message(Base):
    __tablename__="messages"
    id = Column("id", INTEGER, primary_key= True,)
    name = Column("name", String, nullable=False)
    id_hash = Column("id_hash", VARCHAR(256), unique=True)
    message_url = Column("message_url", String)
