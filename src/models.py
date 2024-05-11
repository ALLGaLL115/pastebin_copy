from datetime import datetime, timedelta, timezone
from typing import Annotated
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import VARCHAR, Column, INTEGER, ForeignKey, String, text, TIMESTAMP

from database import Base
from schemas.message_schemas import MessageDB
from schemas.subscription_schemas import SubscriptionDB
from schemas.user_schemas import UserDB
from schemas.verification_code_schemas import VerifycationCodeDB

created_at = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
# exxx = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now() + interval '1 minute')"))]
updated_at = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"),
                                                        onupdate=datetime.now(timezone.utc), type_=TIMESTAMP(timezone=True))]



class Subscription(Base):
    __tablename__="subscriptions"
    subscriber_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True, )
    target_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True, )
    subscriber = relationship("User", foreign_keys=[subscriber_id])
    target = relationship("User", foreign_keys=[target_id])

    # subscriber: Mapped["User"] = relationship(
    #     back_populates="subscriptions"
    # )

    # target: Mapped["User"] = relationship(
    #     back_populates="folowers"
    # )

    def convert_to_model(self):
        return SubscriptionDB(
            subscriber_id = self.subscriber_id,
            target_id = self.target_id,
        )
    

class User(Base):
    __tablename__="users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)  
    email: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    verificated: Mapped[bool] = mapped_column(default=False)
    
    created_at: Mapped[created_at]

    subscriptions: Mapped[list["Subscription"]] = relationship(
        foreign_keys=[Subscription.subscriber_id],
        back_populates="subscriber"
    )

    folowers: Mapped[list["Subscription"]] = relationship(
        foreign_keys=[Subscription.target_id],
        back_populates="target"
    )

    messages: Mapped[list["Message"]] = relationship(
        back_populates="user"
    )

    def convert_to_model(self):
        print(self)
        return UserDB(
            id = self.id,
            name = self.name,
            email = self.email,
            password_hash = self.password_hash,
            verificated = self.verificated,
            created_at = self.created_at,
        )
  


class Message(Base):
    __tablename__="messages"
    id = Column("id", INTEGER, primary_key= True,)
    name = Column("name", String, nullable=False)
    hash_id = Column("hash_id", VARCHAR(256), unique=True)
    user_id = Column("user_id", INTEGER, ForeignKey("users.id", ondelete="CASCADE"))
    message_url = Column("message_url", String)

    user: Mapped["User"] = relationship(
        back_populates="messages"
    )

    def convert_to_model(self):
            return MessageDB(
            id = self.id,
            name = self.name,
            hash_id = self.hash_id,
            user_id = self.user_id,
            message_url = self.message_url,            
        )



class VerifycationCode(Base):
    __tablename__ = "verifycation_codes"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    code: Mapped[str] = mapped_column(nullable=False, unique=True)
    expiry_time: Mapped[datetime] = mapped_column(nullable=False, default= datetime.now(timezone.utc) + timedelta(minutes=1), type_=TIMESTAMP(timezone=True))

    def convert_to_model(self):
        return VerifycationCodeDB(
            id = self.id,
            user_id = self.user_id,
            code = self.code,
            expiry_time = self.expiry_time,
        )
     

    





