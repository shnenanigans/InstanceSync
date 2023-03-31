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

#find group names from instgroups.json file
def find_groups():
    groups = []
    try:
        f = open("".join(multi) + "\\instances\\instgroups.json", "r")
        data = json.load(f)
    except FileNotFoundError or OSError:
        return groups
    finally:
        f.close()
    for k, v in data.items():
        if k=="groups":
            for k, v in v.items():
                groups.append(k)
    return groups

#find instances in a particular group from instgroups.json file
def find_instances_from_groups(group):
    instances = []
    try:
        f = open("".join(multi) + "\\instances\\instgroups.json", "r")
        data = json.load(f)
    except FileNotFoundError or OSError:
        return instances
    finally:
        f.close()
    for k, v in data.items():
        if k=="groups":
            for k, v in v.items():
                if k==group:
                    instances = v["instances"]
    if len(instances)<=1:
        messagebox.showerror(title=None, message="Please make sure your multimc group has multiple instances in it")
    instances.sort()
    return instances
