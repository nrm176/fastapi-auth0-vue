import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Security, status, Query, Path, APIRouter
import auth0
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()
permission = auth0.Permission.READ_API
auth_zero = auth0.JWTBearer(auth0.auth_config, permission)

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/auth0', dependencies=[Depends(auth_zero)])
def auth_zero():
    return 'passed'

if __name__ == '__main__':
    uvicorn.run('main:app', host="0.0.0.0", port=8002, log_level='info', workers=1, reload=True)
