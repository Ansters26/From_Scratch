# from pydantic import BaseModel,Field
# from typing import Annotated

# class User(BaseModel):
#     name:Annotated[str,Field(...,min_length=8)]
#     age:Annotated[int,Field(...,ge=18)]

# user = User(name="Akki12345",age=29)
# print(user)



#deserlize and serialize using pydantic
from pydantic import BaseModel,Field
from typing import Annotated

class User(BaseModel):
    name:Annotated[str,Field(...,min_length=8)]
    age:Annotated[int,Field(...,ge=18)]

data = {"name":"Akki12345","age":29}
user = User.model_validate(data)
print(user.model_dump())