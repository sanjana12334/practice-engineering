from fastapi import FastAPI, Request
from mockdata import products
from dtos import ProductDTO
app = FastAPI()


@app.get("/")
def home():
    return {"message": "Welcome to the FastAPI application!"}

@app.get("/contact")
def contact():
    return "you can connect us any time"

@app.get("/products")

def get_products():
    return products

## Path Params..   {define and fix value and only one or two dynamic value not more then that}
# key value pair  (id is key , product is value)
@app.get("/product/{product_id}")
def get_one_product(product_id: int):
    #  if product available with the id, return product, else return erroe message.

    for oneProduct in products:
        if oneProduct.get("id") == product_id:
            return oneProduct

    return{
        "error": "Product not found for this id."
    }
    # return{
    #     "id":product_id
    # }

#  quary params {define and value and it can be 1,2 or n dynamic value}
@app.get("/greet")
# def greet_user(name: str, age: int):
#     return{
#         "greet":f"hello {name}, Your age is {age} "
#     }
def greet_user(request: Request):
    # print(request.query_params)
    query_params = dict(request.query_params)
    # print(query_params)
    # return{
    #     "greet":f"hello, Your age is "
    # }

    # in the form of dictionary we can get the query params and then we can use it in the response.
    return{
            "greet":f"hello {query_params.get('name')}, Your age is {query_params.get('age')}"
        }
#  different types of http methods
@app.post("/create_product")

def create_product(product_data: ProductDTO):
    product_data = product_data.model_dump()
    products.append(product_data)

    return{"status":"product created successfully", "data": products}

@app.put("/update_product/{product_id}")

def update_product(product_data:ProductDTO, product_id:int,):

    for index, oneProduct in enumerate(products):
        if oneProduct.get("id") == product_id:
            products[index] = product_data.model_dump()
            return{"status":"product updated successfully..", "data": product_data}
            
        # print(oneProduct)

    return{
        "error":"product not found for this id"
    }    

@app.delete("/delete_product/{product_id}")
def delete_product(product_id:int):
    for index, oneProduct in enumerate(products):
        if oneProduct.get("id") == product_id:
            deleted_product = products.pop(index)
            return{"status":"product delete successfully..", "product":deleted_product}
   
    return{
            "error":"product not found for this id"
        }   


# pydantic  provide python data type