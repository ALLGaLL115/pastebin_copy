from datetime import datetime, timedelta, UTC, timezone
from typing import Annotated
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import VARCHAR, Column, INTEGER, ForeignKey, String, text, TIMESTAMP

from database import Base
from schemas import Roles


created_at = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
# exxx = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now() + interval '1 minute')"))]
updated_at = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"),
                                                        onupdate=datetime.now(timezone.utc), type_=TIMESTAMP(timezone=True))]





class Role(Base):
    __tablename__="roles"
    id: Mapped[int] = mapped_column(primary_key=True)
    role: Mapped[str] = mapped_column(nullable=False)

    # users_rel: Mapped[list["User"]] = relationship(
    #     "User",
    #     back_populates= "role"
    # )


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
    password_hash: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[int] = mapped_column(ForeignKey("roles.id"), default= 3)
    created_at: Mapped[created_at]

    # role: Mapped["Role"] = relationship(
    #     "Role",
    #     back_populates= "users_rel"
    # )

class Message(Base):
    __tablename__="messages"
    id = Column("id", INTEGER, primary_key= True,)
    name = Column("name", String, nullable=False)
    id_hash = Column("id_hash", VARCHAR(256), unique=True)
    message_url = Column("message_url", String)



class VerifycationCode(Base):
    __tablename__ = "verifycation_codes"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    code: Mapped[str] = mapped_column(nullable=False, unique=True)
    expiry_time: Mapped[datetime] = mapped_column(nullable=False, default= datetime.now(UTC) + timedelta(minutes=1), type_=TIMESTAMP(timezone=True))




