import json
import sys, termios
import datetime
from time import sleep
from os import system

clearInputBuffer = lambda: termios.tcflush(sys.stdin, termios.TCIOFLUSH)

def getConfig():
    config = None
    current = None

    with open("config.json", "r") as file:
        config = json.load(file)
    with open("current.json", "r") as file:
        current = json.load(file)

    return [config, current]

def dumpCurrent(data):
    with open("current.json", "w") as file:
        json.dump(data, file, indent=4)

def addLog(data):
    fileData = None
    with open("data.json", "r") as file:
        fileData = json.load(file)
    with open("data.json", "w") as file:
        fileData.append(data)
        json.dump(fileData, file, indent=4)

def handleMiscCmds(code):
    if code.startswith("SYSCMD-"):
        system(code[7:])
        input()
    elif code == "SYSPWR":
        system("sudo reboot")
    elif code == "SYSDTA":
        print("\033[0m")
        with open('data.json', 'r') as file:
            print(json.dumps(json.load(file), indent=4))
        input("Scan to continue ")
    elif code == "SYSCLR":
        with open("current.json", "w") as file:
            json.dump({}, file, indent=4)
    elif code == "SYSPULLGH":
        print("\033[0m")
        system("kill $BASHPID -9")
        input()
    else: return -1
    return 0

def printCurrent():
    print("")
    if any([v[0] == "OUT" for v in current.values()]):
        print("\033[0m  Currently signed out items:")
    for item in current:
        if current[item][0] == "OUT":
            correctName = None
            try:
                correctName = config["users"][current[item][1]]
            except:
                correctName = config["groups"][current[item][1]]
            if item == "837013207139": item = "TACHOMETER" # TEMP
            print("\033[95m            * " + item + " signed out by: \033[93m" + correctName + "\033[0m")
    print("")

def clearScreen():
    system("clear")
    clearInputBuffer()

configs = getConfig()
config = configs[0]
current = configs[1]

system("clear")
clearInputBuffer()

try:
    while True:
        current = getConfig()[1]
        printCurrent()

        name = input("\033[96m  NAME/SUBGROUP: \033[90m").upper()
        
        cmds = handleMiscCmds(name)

        if cmds == 0:
            clearScreen()
            continue

        if name in config["items"] and name in current.keys() and current[name][0] == "OUT" and cmds == -1:
            current[name] = ["IN", "UNKNOWN"]
            print("\033[92m  Signed " + name + " IN\033[0m")
            dumpCurrent(current)
            addLog({
                "timestamp": datetime.datetime.now().isoformat(),
                "item": name,
                "user": "UNKNOWN",
                "action": "IN"
            })
            sleep(0.4)
            clearScreen()
            continue

        if name not in config["users"] and name not in config["groups"] and cmds == -1:
            system("clear")
            print("\033[91m  Invalid name, try again \033[90m(read " + name +")\033[0m")
            continue

        system("clear")
        printCurrent()

        if name in config["groups"]:
            print("\033[96m  SUBGROUP: \033[93m" + config["groups"][name] +"\033[0m\n")
        else:
            print("\033[96m  NAME: \033[93m" + config["users"][name] +"\033[0m\n")

        while True:
            code = input("\033[96m  SCAN ITEM: \033[93m").upper()
            print("\033[0m")
        
            if code in config["users"] or code in config["groups"]: break

            handleMiscCmds(code)

            if code not in config["items"]:
                print("\033[91m  Invalid code, try again\033[0m")
                continue
            break

        if code in config["users"] or code in config["groups"]:
            clearScreen()
            continue

        if not code in current.keys() or current[code][0] == "IN":
            current[code] = ["OUT", name]
            addLog({
                "timestamp": datetime.datetime.now().isoformat(),
                "item": code,
                "user": name,
                "action": "OUT"
            })
        elif current[code][0] == "OUT":
            current[code] = ["IN", name]
            addLog({
                "timestamp": datetime.datetime.now().isoformat(),
                "item": code,
                "user": name,
                "action": "IN"
            })
        
        print("\033[92m  Signed " + code + " " + current[code][0] + "\033[0m")

        dumpCurrent(current)
        sleep(0.4)
        clearScreen()
except KeyboardInterrupt:
    print("")
    pass