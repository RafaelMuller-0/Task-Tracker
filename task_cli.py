import sys
import json
from datetime import datetime

VALID_STATUSES = ["todo", "in-progress", "done"]

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
            if not isinstance(tasks, list):
                raise ValueError
            return tasks
    except FileNotFoundError:
        return []


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
    if status not in VALID_STATUSES and status is not None:
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
    for task in tasks:
        if task["id"] == task_id:
            task["description"] = description
            task["updatedAt"] = datetime.now().isoformat()
            save_tasks(tasks)
            return task
    return None

def delete_task(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            save_tasks(tasks)
            return task
    return None

def update_status(task_id, status):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = status
            task["updatedAt"] = datetime.now().isoformat()
            save_tasks(tasks)
            return task
    return None




if len(sys.argv) < 2:
    print("Nenhum comando encontrado")
    sys.exit(1)
else:
    try:
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
                tid = parse_task_id(sys.argv[2])
                if tid is None:
                    print("Id informado é invalido, favor digitar um número inteiro")
                else:
                    task = update_task(tid, sys.argv[3])
                    if task is None:
                        print("Nenhuma tarefa encontrada com o id informado")
                    else:
                        print(f"A tarefa: {task['description']} de id: {task['id']} foi atualizada com sucesso")
        elif command == "delete":
            if len(sys.argv) < 3:
                print("Nenhum id informado")
            else:
                tid = parse_task_id(sys.argv[2])
                if tid is None:
                    print("Id informado é invalido, favor digitar um número inteiro")
                else:
                    task = delete_task(tid)
                    if task is None:
                        print("Nenhuma tarefa encontrada com o id informado")
                    else:
                        print(f"Tarefa de id: {task['id']} foi deletada com sucesso")
        elif command == "mark-done":
            if len(sys.argv) < 3:
                print("Nenhum id informado")
            else:
                tid = parse_task_id(sys.argv[2])
                if tid is None:
                    print("Id informado é invalido, favor digitar um número inteiro")
                else:
                    task = update_status(tid,"done")
                    if task is None:
                        print("Nenhuma tarefa encontrada com o id informado")
                    else:
                        print(f"Tarefa de id: {task['id']} teve seu status alterado com sucesso")
        elif command == "mark-in-progress":
            if len(sys.argv) < 3:
                print("Nenhum id informado")
            else:
                tid = parse_task_id(sys.argv[2])
                if tid is None:
                    print("Id informado é invalido, favor digitar um número inteiro")
                else:
                    task = update_status(tid,"in-progress")
                    if task is None:
                        print("Nenhuma tarefa encontrada com o id informado")
                    else:
                        print(f"Tarefa de id: {task['id']} teve seu status alterado com sucesso")
        else:
            print("comando não encontrado")
            sys.exit(1)
    except json.JSONDecodeError:
        print("Arquivo corrompido ou inválido")
        sys.exit(1)
    except ValueError:
        print("Estrutura do arquivo inválida")
        sys.exit(1)