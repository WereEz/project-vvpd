import webbrowser
import os
import weather

def execute_command(commands, command):
    command = command.lower()
    if any(command == i[0].lower() for i in commands.items()):
        return fopen(commands, command)
    if command.find("открой") != -1 or command.find("открыть") != -1:
        return fopen(commands, command)
    if command.find("поиск") != -1 or command.find("найди") != -1 or command.find("найти") != -1:
        return fsearch(command)
    if (command.find("погод") != -1 and (command.find("скажи") != -1 or
        command.find("какая")!= -1 or command.find("cейчас")!= -1)) or (command == ("погодa")):
        mes = weather.get_weather()
        message = f"<b>{mes['temperature']}</b><br>{mes['status']}<br>{mes['wind']}"
        return(message)
    
def fopen(commands, command):
    for user_command in commands.items():
        if command == user_command[0].lower():
            sites, folders = map(lambda x: list(
                x.values())[0], user_command[1])
            for i in sites:
                webbrowser.open_new_tab(i)
            for j in folders:
                if os.path.exists(j):
                    os.system(f'start "" "{(j)}"')
            return 1
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
