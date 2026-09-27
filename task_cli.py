import sys
import json

def load_tasks():
    try:
        with open("tasks.json", "r") as jf:
            tasks = json.load(jf)
            return tasks
    except FileNotFoundError:
        return []

def save_tasks(tasks):
    with open("tasks.json", "w") as jf:
        json.dump(tasks, jf)





"""def add_task(description):
    print("Função de adicionar descrição: '", description,  "' executada com sucesso")

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
            description = sys.argv[2]
            add_task(description)
    elif command == "list":
        print("comando list reconhecido")
    else:
        print("comando não encontrado")
        sys.exit(1)"""