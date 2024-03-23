from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
import uvicorn
from controllers.UserController import user_controller_router
from controllers.BookController import book_controller_router
import os
from dotenv import load_dotenv

app = FastAPI()
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

tags_metadata = [
    {"name": "Users", "description": "Operations related to user management"},
    {"name": "Books", "description": "Operations related to user management"}
]

# Include the routers from controller modules
app.include_router(user_controller_router, prefix="/users", tags=["users"])
app.include_router(book_controller_router, prefix="/books", tags=["books"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return RedirectResponse("docs")

if __name__ == '__main__':
    uvicorn.run("app:app", host=os.environ.get("HOST"), port=int(os.environ.get("PORT")), reload=True)