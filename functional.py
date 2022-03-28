import webbrowser

def execute_command(commands, command):
    command.lower()
    if command.find("открой") != -1 or command.find("открыть") != -1:
        return fopen(commands, command)
    if command.find("поиск") != -1 or command.find("найди") != -1 or command.find("найти") != -1:
        return fsearch(command)

def fopen(commands, command):
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

def fsearch(command):
    search_string = command.repalce("поиск", "", 1)
    search_string = search_string.repalce("найди", "", 1)
    search_string = search_string.repalce("найти", "", 1)
    search_string = search_string.repalce(" ","+")
    search_string = "https://www.google.com/search?q=" + search_string
    webbrowser.open_new_tab(search_string)