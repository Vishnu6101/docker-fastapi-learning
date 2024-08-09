from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from bson import ObjectId
from typing import List

app = FastAPI()

# MongoDB connection details
MONGO_DETAILS = "mongodb://admin:password@mongodb"
client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.todo_db
todo_collection = database.get_collection("todos")

# Pydantic models
class Todo(BaseModel):
    title: str
    description: str

class TodoInDB(Todo):
    id: str

# Utility function to convert BSON to JSON
def todo_helper(todo) -> dict:
    return {
        "id": str(todo["_id"]),
        "title": todo["title"],
        "description": todo["description"],
    }

@app.post("/todos/", response_model=TodoInDB)
async def create_todo(todo: Todo):
    new_todo = await todo_collection.insert_one(todo.dict())
    created_todo = await todo_collection.find_one({"_id": new_todo.inserted_id})
    return todo_helper(created_todo)

@app.get("/todos/", response_model=List[TodoInDB])
async def get_todos():
    todos = []
    async for todo in todo_collection.find():
        todos.append(todo_helper(todo))
    return todos

@app.get("/todos/{id}", response_model=TodoInDB)
async def get_todo(id: str):
    todo = await todo_collection.find_one({"_id": ObjectId(id)})
    if todo is not None:
        return todo_helper(todo)
    raise HTTPException(status_code=404, detail="Todo not found")

@app.put("/todos/{id}", response_model=TodoInDB)
async def update_todo(id: str, todo: Todo):
    update_result = await todo_collection.update_one(
        {"_id": ObjectId(id)}, {"$set": todo.dict()}
    )
    if update_result.modified_count == 1:
        updated_todo = await todo_collection.find_one({"_id": ObjectId(id)})
        return todo_helper(updated_todo)
    raise HTTPException(status_code=404, detail="Todo not found")

@app.delete("/todos/{id}", response_model=dict)
async def delete_todo(id: str):
    delete_result = await todo_collection.delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count == 1:
        return {"message": "Todo deleted"}
    raise HTTPException(status_code=404, detail="Todo not found")
