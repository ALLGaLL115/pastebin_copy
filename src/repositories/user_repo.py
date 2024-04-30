import logging

from fastapi import HTTPException
from sqlalchemy import select, or_
from models import User
from utils.repository import SqlAlchemyRepository

class UserRepository(SqlAlchemyRepository):
    model = User 


    async def check_unique_values(self, email:str, name:str)->None:
        db_verificated_values: list = []
        db_unverificated_values = []
        query = select(self.model).where(or_(
            self.model.email ==email,
            self.model.name ==name
        ))
        users = await self.session.execute(query)
        users:list["User"] = users.scalars().all()
        

        
        for i in users:
            if i.__getattribute__("email") == email:
                if i.verificated == True:
                    db_verificated_values.append("email")
                else:
                    db_unverificated_values.append("email")
            if i.__getattribute__("name") == name:
                if i.verificated == True:
                    db_verificated_values.append("name")
                else:
                    db_unverificated_values.append("name")
       
       
        if not users:
            return "create"

        if db_verificated_values:
            raise HTTPException(status_code=409, detail=[f"This {x} already used" for x in db_verificated_values])
        
   
        if len(users)>1:
            raise HTTPException(status_code=409, detail="This username already used")
        
   
        if len(users) == 1 and len(db_unverificated_values) ==1 and "name" in db_unverificated_values:
            raise HTTPException(status_code=409, detail="This username already used")

  
        if len(users) == 1 and "email" in db_unverificated_values:
            return "update"
        
       
        
        
        
        
        
        


                        



        # if "users_name_key" in e._message():
        #         raise HTTPException(status_code=409, detail= "This username is already used")

