import json
import os

MEMORY_FILE = "command_memory.json"


def load_memory():

    if not os.path.exists(MEMORY_FILE):
        return {}

    with open(MEMORY_FILE, "r") as f:
        return json.load(f)


def save_memory(memory):

    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=4)


def get_command(query):

    memory = load_memory()

    return memory.get(query.lower())


def learn_command(query, command):

    memory = load_memory()

    memory[query.lower()] = command

    save_memory(memory)


def suggest(prefix):

    memory = load_memory()

    suggestions = []

    for key in memory.keys():
        if key.startswith(prefix.lower()):
            suggestions.append(key)

    return suggestions[:3]