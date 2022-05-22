import webbrowser
import os
import weather
import json
import random
qwords = ["кто","что","какой","чей","который","сколько","когда","где","куда",
        "как","откуда","почему","зачем?"]


with open("qa.json", "r", encoding="utf-8") as read_file:
    qa = json.load(read_file)
    
def execute_command(commands, command): 
    command = command.lower()
    if not command:
        return [0,0]
    if any(command == i[0].lower() for i in commands.items()):
        return [fopen(commands, command),0]
    if (command.find("выполни") != -1) or command.find("выполнить") != -1:
        return [fcomplexcommand(commands, command),0]
    if (command.find("открой") != -1) or command.find("открыть") != -1:
        return [fopen(commands, command),0]
    if (command.find("поиск") != -1) or (command.find("найди") != -1) or (command.find("найти") != -1):
        return [fsearch(command),0]
    if (command.find("погод") != -1 and (command.find("скажи") != -1 or
        command.find("какая")!= -1 or command.find("cейчас")!= -1)) or (command == ("погода")):
        mes = weather.get_weather()
        if mes:
            message = f"<b>{mes['temperature']}</b><br>{mes['status']}<br>{mes['wind']}"
        else:
            message = "<b>Извините</b><br>не могу узнать" 
        return([message,1])

    if command in qa:
        return([random.choice(qa[command]),0])
    else:
        if command.split(" ")[0] in qwords:
            search_string = "https://www.google.com/search?q=" + command
            webbrowser.open_new_tab(search_string)
            return(["сейчас найдем",0])
        return([random.choice(qa["0"]),0])

    
    
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
def main():
    command = input()
    # запретить редактировать
    with open("commands.json", "r", encoding="utf-8") as read_file:
        commands = json.load(read_file)
    success = execute_command(commands, command)
    

if __name__ == "__main__":
    main()
