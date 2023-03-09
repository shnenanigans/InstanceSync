import os
from tkinter import messagebox

#makes the multi path a global variable cause I suck at coding
def find_multimc(path):
    global multi
    multi=path

#finds all your multimc instances in case they are not grouped
def find_instances():
    mylist = os.listdir("".join(multi) + "\\instances")
    try:
        mylist.remove("instgroups.json")
        mylist.remove("_LAUNCHER_TEMP")
    except:
        pass
    mylist.sort()
    return mylist

#find instance names from the .json by searching between two apostrophes
def find_between(s):
    start = s.index("\"") + len("\"")
    end = s.index("\"", start)
    return s[start:end]

#finds your multimc instances groups and returns them in a list
def find_groups():
    try:
        f_groups = open("".join(multi) + "\\instances\\instgroups.json", "r")
    except FileNotFoundError or OSError:
        return []
    group_lines = f_groups.readlines()
    groups = []
    i=0
    for line in group_lines:
        if line.find("instances") != -1:
            group = group_lines[i-2]
            group = find_between(group)
            groups.append(group)
        i += 1
    f_groups.close()
    return groups

#finds which instances are in a particular group and sorts them alphabetically (thanks specnr)
def find_instances_from_groups(group):
    f_groups = open("".join(multi) + "\\instances\\instgroups.json", "r")
    group_lines = f_groups.readlines()
    insts = []
    for line in group_lines:
        if line.find(group) != -1:
            i=group_lines.index(line) + 3
            while group_lines[i].find("]") == -1:
                inst = find_between(group_lines[i])
                insts.append(inst)
                i += 1
    f_groups.close()
    if len(insts)<=1:
        messagebox.showerror(title=None, message="Please make sure your multimc group has multiple instances in it")
    insts.sort()
    return insts