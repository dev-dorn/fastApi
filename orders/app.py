from fastapi import FastAPI

app = FastAPI()


from orders.api.api import api
app.include_router(api)