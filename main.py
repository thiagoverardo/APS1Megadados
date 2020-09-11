from typing import Optional, List, Dict
from fastapi import Body, FastAPI, Query, HTTPException
from pydantic import BaseModel
from uuid import UUID
from enum import Enum


app = FastAPI()


class Task(BaseModel):
    name: str
    description: str
    status: bool


class Status_Filter(str, Enum):
    done = "done"
    not_done = "not_done"
    all = "all"


class Delete(BaseModel):
    id: int


tasks = {1: {"name": "tarefinha", "description": "oi", "status": False},
         2: {"name": "tarefa", "description": "tchau", "status": True},
         3: {"name": "tarefona", "description": "sei la", "status": True}}


@app.get("/tasks/{status}", tags=["Mostra e Filtra tarefas"])
async def show_tasks(status: Status_Filter):
    ''' Esse método mostra tarefas criadas dependendo do valor passado na URL, se o usuário digitar "/done", irá mostrar apenas as tarefas concluídas, se o usuário digitar "/not_done" irá mostrar apenas as tarefas não concluídas e se digitar "/all" todas as tarefas serão mostradas.'''
    status_list = {}
    if status == Status_Filter.done:
        for i in tasks:
            if tasks[i]["status"]:
                status_list[i] = tasks[i]
        return status_list
    elif status == Status_Filter.not_done:
        for i in tasks:
            if not tasks[i]["status"]:
                status_list[i] = tasks[i]
        return status_list
    else:
        return tasks


@app.post("/tasks/create/", tags=["Cria tarefas"])
async def create_item(task: Task):
    ''' Esse método é usado para criar tarefas novas, podendo dar um nome a ela, uma breve descrição e um status, se for "True" quer dizer que ela já está concluída e se for False ainda não está.'''
    n = max(tasks.keys())
    tasks[n+1] = task.dict()
    return n+1


@app.patch("/tasks/edit_description/{id}", tags=["Edita tarefas"])
async def edit_description(id: int, description: str):
    ''' Esse método é usado para editar a descrição de tarefas já criadas, basta passar o id da tarefa na URL e uma descrição nova'''
    if id > 0 and id <= max(tasks.keys()):
        tasks[id].update({"description": description})
        return tasks[id]
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@app.patch("/tasks/edit_status/{id}", tags=["Edita tarefas"])
async def edit_status(id: int):
    ''' Esse método é utilizado para editar o status de uma tarefa, basta passar o id que ela irá inverter o status, se estiver "True", vira "False" e vice versa.'''
    if id > 0 and id <= max(tasks.keys()):
        if tasks[id]["status"] == True:
            tasks[id].update({"status": False})
            return tasks[id]
        else:
            tasks[id].update({"status": True})
            return tasks[id]

    else:
        raise HTTPException(status_code=404, detail="Item not found")


@app.delete("/tasks/delete_task/{id}", tags=["Deleta tarefas"])
async def delete_task(id: int):
    '''Esse método é utilizado para deletar tarefas criadas, basta passar o id, que a tarefa é deletada.'''
    if id > 0 and id <= max(tasks.keys()):
        tasks.pop(id)
        return tasks
    else:
        raise HTTPException(status_code=404, detail="Item not found")
