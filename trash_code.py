from pydantic import BaseModel


class A(BaseModel):
    name: str
    email: str
    password: str

class B(BaseModel):
    # id: str
    name: str
    email: str
    password: str


modelka = B(
    name="1",
    email="alihannn5@mail.ru",
    password="1"
)

hh= {'name': '1', 'email': 'alihannn5@mail.ru', 'password': '1'}
print(A.model_validate(hh))
# print(modelka.model_dump())

