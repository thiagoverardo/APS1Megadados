from typing import Optional, List, Dict
from fastapi import Body, FastAPI, Query
from pydantic import BaseModel
from uuid import UUID
from enum import Enum


app = FastAPI()


class Task(BaseModel):
    name: str
    description: str
    status: bool


class EditDescription(BaseModel):
    id: int
    description: str


tasks = {1: {"name": "tarefinha", "description": "oi", "status": False},
         2: {"name": "tarefa", "description": "tchau", "status": True},
         3: {"name": "tarefona", "description": "sei la", "status": True}}


@app.get("/tasks/")
async def tarefas():
    return tasks


@app.post("/tasks/create/")
async def create_item(task: Task):
    n = len(tasks)
    tasks[n+1] = task.dict()
    return task.dict()


@app.put("/tasks/edit_description/")
async def edit_description(description: EditDescription):
    if description.id > 0 and description.id <= len(tasks):
        tasks[description.id].update({"description": description.description})
        return tasks
    else:
        return tasks
