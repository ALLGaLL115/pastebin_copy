from pydantic import BaseModel

class Ab(BaseModel):
    a: int
    b: int 

class B(BaseModel):
    a:int
    b: int
    c: int

ff = Ab(a=1, b=1)
g = B(a=10 ,b=2, c = 3)
print(ff)
print(g)

data = ff.model_dump()
data = {**data, **g.model_dump()}
copied = ff.model_validate(data)
print(copied)