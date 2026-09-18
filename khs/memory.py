from collections import defaultdict

MEMORY = defaultdict(list)
MAX_HISTORY = 10

def add_message(user, role, content):
    MEMORY[user].append({"role": role, "content": content})
    if len(MEMORY[user]) > MAX_HISTORY:
        MEMORY[user] = MEMORY[user][-MAX_HISTORY:]

def get_memory(user):
    return MEMORY[user]
