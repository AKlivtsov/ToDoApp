from fastapi import FastAPI
from dotenv import load_dotenv
import uvicorn
import os

from schemas import RegUser
import repository as rep

app = FastAPI()

@app.get("/api/ping")
def ping():
    return {"status": "ok"}

@app.post("/auth/sign-up")
def reg_user(item: RegUser):
    
    # if there is an error
    data = rep.reg_user(item)
    if isinstance(data, JSONResponse):
        return data
    
    token, company_id = data
    return {"token": token, "company_id": company_id}

if __name__ == "__main__":
    load_dotenv()
    server_address = os.getenv("SERVER_ADDRESS")
    host, port = server_address.split(":")
    uvicorn.run("main:app", host=host, port=int(port), reload=True)
