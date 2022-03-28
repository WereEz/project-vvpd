import webbrowser

def execute_command(commands, command):
    command.lower()
    if command.find("открой") != -1 or command.find("открыть") != -1:
        return fopen(commands, command)

def fopen(commands ,command):
    for i in commands["folders"].items():
        if command.find(i[1]) != -1:
            #открыть папку, путь хранится в i[0]
            return 1
    for i in commands["sites"].items():
        for j in i[1]:
            if command.find(j) != -1:
                webbrowser.open_new_tab(j[0])
                return 1
    return 0