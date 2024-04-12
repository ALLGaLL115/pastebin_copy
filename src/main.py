from fastapi import FastAPI
from api.message import router as message_router

app = FastAPI()





app.include_router(message_router)


        





    

   
       

   
   

# @app.get("/messages")
# async def get_message(mes_hash: str):
#     mes = await mes_service.get_mes(mes_hash)
#     mes_body = await s3.get(url = mes.hash)
#     return {mes_metadata: mes.metadata, body: mes_body}
    
