from fastapi import FastAPI
from router import router

app = FastAPI(
    title="Data Transfer Rate API",
    description="An API to get the data transfer rate between two nodes in a multihop scenario",
    version="1.0.0"
)

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)