import webbrowser
import os
import weather

def execute_command(commands, command):
    command = command.lower()
    if any(command == i[0].lower() for i in commands.items()):
        return fopen(commands, command)
    if command.find("выполни") != -1 or command.find("выполнить") != -1:
        return fcomplexcommand(commands, command)
    if command.find("открой") != -1 or command.find("открыть") != -1:
        return fopen(commands, command)
    if command.find("поиск") != -1 or command.find("найди") != -1 or command.find("найти") != -1:
        return fsearch(command)
    if (command.find("погод") != -1 and (command.find("скажи") != -1 or
        command.find("какая")!= -1 or command.find("cейчас")!= -1)) or (command.find("погодa")):
        mes = weather.get_weather()
        if mes == 0:
            return 0
        message = f"<b>{mes['temperature']}</b><br>{mes['status']}<br>{mes['wind']}"
        return(message)
    
def fopen(commands, command):
    for i in commands["folders"].items():
        if command.find(i[1]) != -1 and os.path.exists(i[0]):
            os.system(f'start "" "{(i[0])}"')
            return 1
    for i in commands["sites"].items():
        for j in i[1]:
            if command.find(j) != -1:
                webbrowser.open_new_tab(i[0])
                return 1
    return 0


def fsearch(command):
    search_string = command.replace("поиск", "", 1)
    search_string = search_string.replace("найди", "", 1)
    search_string = search_string.replace("найти", "", 1)
    search_string = search_string.replace(" ", "+")
    search_string = "https://www.google.com/search?q=" + search_string
    webbrowser.open_new_tab(search_string)

def fcomplexcommand(commands, command):
    for i in commands["complexcommands"].items():
        if command.find(i[0]) != -1:
            for j in i[1]:
                if os.path.exists(j):
                    os.system(f'start "" "{(j)}"')
                else:
                    webbrowser.open_new_tab(j)
            return 1