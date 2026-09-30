import sys
import json
from datetime import datetime

VALID_STATUSES = ["todo", "in-progress", "done"]

def parse_task_id(task_id):
    try:
        return int(task_id)
    except (ValueError, TypeError):
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
            conteudo = jf.read()
            if not conteudo.strip():
                return []
            tasks = json.loads(conteudo)
            required_keys = ["id", "description", "status", "createdAt", "updatedAt"]
            if not isinstance(tasks, list):
                raise ValueError("O arquivo não contém Lista")
            for task in tasks:
                if not isinstance(task, dict):
                    raise ValueError("A tarefa deve ser um dicionario")
                for key in required_keys:
                    if key not in task:
                        raise ValueError(f"A tarefa não possui a chave: {key}")
                if not isinstance(task["id"], int):
                    raise ValueError(f"O id {task['id']} não está no formato INT")
                if not isinstance(task['description'], str):
                    raise ValueError(f"A descrição {task['description']} deve ser uma STRING")
                if not isinstance(task["status"], str):
                    raise ValueError(f"O status {task['status']} não está no formato STRING")
                if task["status"] not in VALID_STATUSES:
                    raise ValueError(f"O {task['status']} é uma string porém o status salvo não é permitido")
                if not isinstance(task["createdAt"], str):
                    raise ValueError(f"O {task['createdAt']} não está no formato STRING")
                if not isinstance(task["updatedAt"], str):
                    raise ValueError(f"O {task['updatedAt']} não está no formato STRING")
                try:
                    datetime.fromisoformat(task["createdAt"])
                except ValueError:
                    raise ValueError(f"O createdAt: {task['createdAt']} não está no padrão iso")
                try:
                    datetime.fromisoformat(task["updatedAt"])
                except ValueError:
                    raise ValueError(f"O updatedAt: {task['updatedAt']} não está no padrão iso")
            return tasks
    except FileNotFoundError:
        return []

def save_tasks(tasks):
    with open("tasks.json", "w") as jf:
        json.dump(tasks, jf)

def add_task(description):
    if description.strip() == "":
        raise ValueError("A descrição informada está vazia")
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
        raise ValueError("Filtro informado invalido. Use: todo, in-progress ou done.")
    else:
        tasks = load_tasks()
        if len(tasks) == 0:
            print("Nenhuma tarefa encontrada")
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
    tid = parse_task_id(task_id)
    if tid is None:
        raise ValueError("O id informado é invalido")
    if description.strip() == "":
        raise ValueError("A descrição informada está vazia")
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == tid:
            task["description"] = description
            task["updatedAt"] = datetime.now().isoformat()
            save_tasks(tasks)
            return task
    return None

def delete_task(task_id):
    tid = parse_task_id(task_id)
    if tid is None:
        raise ValueError("O id informado é invalido")
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == tid:
            tasks.remove(task)
            save_tasks(tasks)
            return task
    return None

def update_status(task_id, status):
    tid = parse_task_id(task_id)
    if tid is None:
        raise ValueError("O id informado é invalido")
    if status not in VALID_STATUSES:
        raise ValueError("O status informado não é válido")
    tasks = load_tasks()
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
                task = update_task(sys.argv[2], sys.argv[3])
                if task is None:
                    print("Nenhuma tarefa encontrada com o id informado")
                else:
                    print(f"A tarefa: {task['description']} de id: {task['id']} foi atualizada com sucesso")
        elif command == "delete":
            if len(sys.argv) < 3:
                print("Nenhum id informado")
                sys.exit(1)
            else:
                task = delete_task(sys.argv[2])
                if task is None:
                    print("Nenhuma tarefa encontrada com o id informado")
                else:
                    print(f"Tarefa de id: {task['id']} foi deletada com sucesso")
        elif command == "mark-done":
            if len(sys.argv) < 3:
                print("Nenhum id informado")
                sys.exit(1)
            else:
                task = update_status(sys.argv[2],"done")
                if task is None:
                    print("Nenhuma tarefa encontrada com o id informado")
                else:
                    print(f"Tarefa de id: {task['id']} teve seu status alterado com sucesso")
        elif command == "mark-in-progress":
            if len(sys.argv) < 3:
                print("Nenhum id informado")
                sys.exit(1)
            else:
                task = update_status(sys.argv[2],"in-progress")
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
    except ValueError as e:
        print(e)
        sys.exit(1)