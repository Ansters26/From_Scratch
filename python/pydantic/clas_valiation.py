from typing import List
from pydantic import BaseModel
from typing import Literal,Optional

class Orders(BaseModel):
    user_id:int
    product_ids:List[int]
    payment_mode:Literal['upi','card','cash']
    delivery_note:Optional[str]=None

order1=Orders(user_id=123,product_ids=[23,456,77],payment_mode='upi')
print(order1)
order2=Orders(user_id=234,product_ids=[1,2,3],payment_mode='cash',delivery_note="hi")
print(order2)