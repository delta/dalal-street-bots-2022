import uvicorn
from typing import Optional
from fastapi import FastAPI

app = FastAPI()

if __name__ == "__main__":
	uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True, debug=True)

@app.get("/")
def read_root():
    return {"Dalal": "ToTheMoon"}
