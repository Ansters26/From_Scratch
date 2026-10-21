from pydantic import BaseModel,computed_field

class CartItems(BaseModel):
    item_name:str
    price:float
    quantity:int
    discount:float=0.0

    @computed_field
    @property
    def total_price(self)->float:
        return (self.price *self.quantity) -self.discount

cart=CartItems(item_name="laptop",price=1000,quantity=2)
print(cart)