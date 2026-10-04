# Task Tracker CLI

## Descrição

Um aplicativo de linha de comando para gerenciamento de tarefas,
desenvolvido em Python.

O aplicativo permite adicionar, atualizar, excluir e listar tarefas,
além de alterar o status das tarefas entre `todo`, `in-progress` e `done`.

As tarefas são armazenadas em um arquivo `tasks.json` no diretório atual.

## Funcionalidades

- Adicionar tarefas
- Atualizar tarefas
- Excluir tarefas
- Marcar tarefas como `in-progress`
- Marcar tarefas como `done`
- Listar todas as tarefas
- Listar tarefas por status
- Armazenar tarefas em um arquivo JSON
- Criar o arquivo `tasks.json` automaticamente caso ele não exista
- Validar os dados armazenados no arquivo JSON
- Tratar erros de entrada e dados inválidos

## Tecnologias utilizadas

- Python
- JSON
- Git

O projeto utiliza apenas recursos da biblioteca padrão do Python,
sem bibliotecas externas ou frameworks.

## Pré-requisitos

- Python 3 instalado
- Para verificar se o Python está instalado, execute:

```bash
python --version
```
## Como executar

Entre no diretório do projeto.

Execute o programa pelo terminal utilizando o Python:

```bash
python task_cli.py <comando> [argumentos]
```

## Comandos

### Adicionar uma tarefa

```bash
python task_cli.py add "Descrição da tarefa"
```
Adiciona uma nova tarefa com o status inicial `todo`.

Exemplo:

```bash
python task_cli.py add "Buy groceries"
```

### Atualizar uma tarefa

Atualiza a descrição da tarefa e o horário da última atualização (`updatedAt`).

```bash
python task_cli.py update 1 "Nova descrição da tarefa"
```

### Deletar uma tarefa

Exclui uma tarefa do arquivo `tasks.json`.

```bash
python task_cli.py delete 1
```


### Marcar uma tarefa como `in-progress`

Marca uma tarefa como `in-progress` e atualiza o horário da última atualização (`updatedAt`).

```bash
python task_cli.py mark-in-progress 1
```

### Marcar uma tarefa como `done`

Marca uma tarefa como `done` e atualiza o horário da última atualização (`updatedAt`).

```bash
python task_cli.py mark-done 1
```

### Listar as tarefas existentes

Lista todas as tarefas existentes no arquivo `tasks.json`, mostrando o ID, a descrição e o status de cada tarefa.

```bash
python task_cli.py list
```

### Listar tarefas por status

Lista somente as tarefas que têm o status correspondente ao informado na chamada do comando

```bash
python task_cli.py list done
python task_cli.py list todo
python task_cli.py list in-progress
```

## Estrutura da tarefa

Cada tarefa possui as seguintes propriedades:

- `id`: um identificador do tipo `INT` que não se repete em outras tarefas
- `description`: uma descrição que é uma `STRING`
- `status`: um status que é uma `STRING` e só pode ser `done`, `todo` ou `in-progress`
- `createdAt`: uma data que é uma `STRING` e deve estar no padrão ISO
- `updatedAt`: uma data que é uma `STRING` e deve estar no padrão ISO

## Armazenamento

As tarefas são armazenadas no arquivo `tasks.json`, que se encontra no diretório atual do projeto.

Caso o arquivo não exista, ele será criado quando uma tarefa for adicionada.

## Tratamento de erros

O programa trata os erros decorrentes das seguintes situações:

- arquivo JSON inexistente;
- arquivo json inválido ou corrompido;
- dados com formato incorreto;
- ID inválido;
- tarefa inexistente;
- status inválido;
- descrição vazia.