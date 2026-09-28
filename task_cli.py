import sys
import json
from datetime import datetime
from enum import nonmember


def parse_task_id(task_id):
    try:
        return int(task_id)
    except ValueError:
        return None

def get_next_id(tasks):
    maior_id = 0
    for task in tasks:
        if task["id"] > maior_id:
            maior_id = task["id"]
    return maior_id  + 1

def load_tasks():
    try:
        with open("tasks.json", "r") as jf:
            tasks = json.load(jf)
            return tasks
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("Arquivo corrompido ou inválido")

def save_tasks(tasks):
    with open("tasks.json", "w") as jf:
        json.dump(tasks, jf)

def add_task(description):
    tasks = load_tasks()
    nid = get_next_id(tasks)
    agora = datetime.now().isoformat()
    dic = {
        "id": nid,
        "description": description,
        "status": "todo",
        "createdAt": agora,
        "updatedAt": agora
    }
    tasks.append(dic)
    save_tasks(tasks)
    return dic

def list_tasks(status=None):
    if status not in ["todo", "in-progress", "done"] and status is not None:
        print("Filtro informado invalido. Use: todo, in-progress ou done.")
    else:
        tasks = load_tasks()
        if len(tasks) == 0:
            print("Nenhuma tarefa encontrada")
        else:
            encontrou = False
            for task in tasks:
                if status is None:
                    print(task["id"], task["description"], task["status"])
                elif task["status"] == status:
                    print(task["id"], task["description"], task["status"])
                    encontrou = True
            if status is not None and encontrou == False:
                print("Nenhuma task encontrada com o filtro informado")

def update_task(task_id, description):
    tasks = load_tasks()
    tid = parse_task_id(task_id)
    if tid is None:
        return None
    for task in tasks:
        if task["id"] == tid:
            task["description"] = description
            task["updatedAt"] = datetime.now().isoformat()
            save_tasks(tasks)
            return task
    return None

def delete_task(task_id):
    tasks = load_tasks()
    tid = parse_task_id(task_id)
    if tid is None:
        return None
    for task in tasks:
        if task["id"] == tid:
            tasks.remove(task)
            save_tasks(tasks)
            return task
    return None

def update_status(task_id, status):
    tasks = load_tasks()
    tid = parse_task_id(task_id)
    if tid is None:
        return None
    if status not in ["todo", "in-progress", "done"]:
        return None
    for task in tasks:
        if task["id"] == tid:
            task["status"] = status
            task["updatedAt"] = datetime.now().isoformat()
            save_tasks(tasks)
            return task
    return None




if len(sys.argv) < 2:
    print("Nenhum comando encontrado")
    sys.exit(1)
else:
    command = sys.argv[1]
    if command == "add":
        if len(sys.argv) < 3:
            print("Nenhuma descrição informada")
            sys.exit(1)
        else:
            task = add_task(sys.argv[2])
            print("O id da tarefa criada foi {}".format(task["id"]))
    elif command == "list":
        if len(sys.argv) < 3:
            list_tasks()
        else:
            list_tasks(sys.argv[2])
    elif command == "update":
        if len(sys.argv) < 3:
            print("Nenhum id e descrição informado")
            sys.exit(1)
        elif len(sys.argv) < 4:
            print("Nenhuma descrição informada")
            sys.exit(1)
        else:
            task = update_task(sys.argv[2], sys.argv[3])
            if task is None:
                print("Nenhuma tarefa encontrada com o id informado")
            else:
                print(f"A tarefa: {task['description']} de id: {task['id']} foi atualizada com sucesso")
    elif command == "delete":
        if len(sys.argv) < 3:
            print("Nenhum id informado")
        else:
            task = delete_task(sys.argv[2])
            if task is None:
                print("Nenhuma tarefa encontrada com o id informado")
            else:
                print(f"Tarefa de id: {task['id']} foi deletada com sucesso")
    elif command == "mark-done":
        if len(sys.argv) < 3:
            print("Nenhum id informado")
        else:
            task = update_status(sys.argv[2],"done")
            if task is None:
                print("Nenhuma tarefa encontrada com o id informado")
            else:
                print(f"Tarefa de id: {task['id']} teve seu status alterado com sucesso")
    elif command == "mark-in-progress":
        if len(sys.argv) < 3:
            print("Nenhum id informado")
        else:
            task = update_status(sys.argv[2],"in-progress")
            if task is None:
                print("Nenhuma tarefa encontrada com o id informado")
            else:
                print(f"Tarefa de id: {task['id']} teve seu status alterado com sucesso")
    else:
        print("comando não encontrado")
        sys.exit(1)
