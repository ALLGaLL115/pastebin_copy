import datetime
from typing import Annotated
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import VARCHAR, Column, INTEGER, ForeignKey, String, text, TIMESTAMP

from database import Base
from schemas import Roles

created_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"),
                                                        onupdate=datetime.datetime.now(datetime.timezone.utc), type_=TIMESTAMP(timezone=True))]





class Role(Base):
    __tablename__="roles"
    id: Mapped[int] = mapped_column(primary_key=True)
    role: Mapped[str] = mapped_column(nullable=False)

    users: Mapped[list["User"]] = relationship(
        "User",
        back_populates= "role"
    )


# class Permissions(Base):
#     __tablename__="permissions"
#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str] = mapped_column(nullable=False)


# class RolePermissions(Base):
#     role_id: Mapped[int] = mapped_column( ForeignKey("roles.id"), primary_key=True)
#     permision_id: Mapped[int] = mapped_column( ForeignKey("permissions"), primary_key=True),
    


class User(Base):
    __tablename__="users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)  
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[int] = mapped_column(ForeignKey("roles.id"), default= Roles.UNVERIFICATE.value)
    created_at: Mapped[created_at]

    role: Mapped["Role"] = relationship(
        "Role",
        back_populates= "users"
    )

class Message(Base):
    __tablename__="messages"
    id = Column("id", INTEGER, primary_key= True,)
    name = Column("name", String, nullable=False)
    id_hash = Column("id_hash", VARCHAR(256), unique=True)
    message_url = Column("message_url", String)


