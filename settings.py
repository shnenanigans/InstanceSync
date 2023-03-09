
#must be set to false here or you get attributeerror when user doesnt press one of the buttons cause tkinter stupid
config = False
mods = False
resourcepacks = False
speedrunigt = False

#changes folders to true or false depending on which ones the user wants to sync
def add_config(var):
    global config
    if var==1:
        config = True
    else:
        config = False
def add_mods(var):
    global mods
    if var==1:
        mods = True
    else:
        mods = False
def add_resourcepacks(var):
    global resourcepacks
    if var==1:
        resourcepacks = True
    else:
        resourcepacks = False
def add_speedrunigt(var):
    global speedrunigt
    if var==1:
        speedrunigt = True
    else:
        speedrunigt = False

