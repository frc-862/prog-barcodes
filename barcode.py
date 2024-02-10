import json
import sys, termios
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
    with open("data.json", "rw") as file:
        json.write(json.load(file).append(data), file, indent=4)

def handleMiscCmds(name, code):
    hasName = name != None

    if code == "SYSPWR":
        system("sudo reboot")
        return 0
    elif code == "SYSGETDATA":
        with open('data.json', 'r') as file:
            print(json.load(file))
        input("Scan to continue ")
        return 0
    elif code == "SYSCLR":
        with open("current.json", "w") as file:
            json.dump({}, file, indent=4)
        return 0
    else: return -1

def printCurrent(update = False):
    print("")
    if any([v[0] == "OUT" for v in current.values()]): print("\033[0m  Currently signed out items:")
    for item in current:
        if current[item][0] == "OUT":
            print("\033[95m            * " + item + " signed out by: \033[93m" + config["users"][current[item][1]] + "\033[0m")
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
        
        cmds = handleMiscCmds(None, name)
        if cmds == 0:
            clearScreen()
            continue
        if name not in config["users"] and cmds == -1:
            system("clear")
            print("\033[91m  Invalid name, try again \033[90m(read " + name +")\033[0m")
            continue

        system("clear")
        printCurrent()
        print("\033[96m  NAME: \033[93m" + config["users"][name] +"\033[0m\n")

        while True:
            code = input("\033[96m  SCAN ITEM: \033[93m").upper()
            print("\033[0m")
        
            if code == name: break

            handleMiscCmds(name, code)

            if code not in config["items"]:
                print("\033[91m  Invalid code, try again\033[0m")
                continue
            break
        if code == name:
            clearScreen()
            continue

        if not code in current.keys() or current[code][0] == "IN":
            current[code] = ["OUT", name]
        elif current[code][0] == "OUT":
            current[code] = ["IN", name]
        print("\033[92m  Signed " + code + " " + current[code][0] + "\033[0m")
        dumpCurrent(current)
        sleep(0.4)
        clearScreen()
except KeyboardInterrupt:
    print("")
    pass