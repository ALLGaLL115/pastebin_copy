import aioredis
import asyncio

red = aioredis.Redis(pool)




async def check():
        
    await red.set("aasd", value=11)

    print(await red.keys("*"))
    await red.delete("aasd")
    print(await red.keys("*"))



asyncio.run(
    check()

)