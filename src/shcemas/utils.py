from pydantic import BaseModel


def update_model(old: BaseModel, new:BaseModel)-> BaseModel:
    
    data = old.model_dump()
    data = {**data, **new.model_dump()}
    copied = old.model_validate(data)
    return copied