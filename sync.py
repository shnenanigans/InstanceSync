import settings
import shutil
from tkinter import messagebox

#find path to the .minecraft folder of each instance that will be synced
def get_inst_paths(insts, path):
    inst_number = len(insts)
    inst_paths = []

    i=0
    while i< inst_number:
        inst_path = path + "\\instances\\" + "".join(insts[i]) + "\\.minecraft"
        inst_paths.append(inst_path)
        i += 1
    return inst_paths

#find paths to each folder to be synced, for each instance and return a list of lists of them
def get_paths(insts, path):
    config_paths = [] 
    mods_paths = []
    packs_paths = []
    igt_paths = []
    inst_number = len(insts)
    inst_paths = get_inst_paths(insts, path)

    i=0
    while i< inst_number:
        config_path = "".join(inst_paths[i]) + "\\config"
        config_paths.append(config_path)
        i += 1
    i=0
    while i< inst_number:
        mods_path = "".join(inst_paths[i]) + "\\mods"
        mods_paths.append(mods_path)
        i += 1
    i=0
    while i< inst_number:
        packs_path = "".join(inst_paths[i]) + "\\resourcepacks"
        packs_paths.append(packs_path)
        i += 1
    i=0
    while i< inst_number:
        igt_path = "".join(inst_paths[i]) + "\\speedrunigt"
        igt_paths.append(igt_path)
        i += 1
    
    return [config_paths, mods_paths, packs_paths, igt_paths]

#put the instances which failed to delete in a nice format for the user to understand
def del_errors(error_list):
    error_string = "Some of your folders failed to delete. They must be deleted before they can be copied in.\nThis may happen if your instances are open.\nFolders failed to delete: \n"
    for error in error_list:
        error_string += f"{error[0]} {error[1]} folder\n"
    error_string += "Program will attempt to continue."
    return error_string

#put the instances which failed to sync in a nice format for the user to understand
def get_errors(error_list):
    packs = False
    error_string = "Folders failed to sync: \n"
    for error in error_list:
        error_string += f"{error[0]} {error[1]} folder\n"
        if error[1]=="resourcepacks":
            packs = True
    if packs:
        error_string += "Make sure your instances are closed"
    return error_string

#edits options.txt to activate chosen resource packs
def activate_packs(first_inst, curr_inst, path):
    first_opt_path = path + "\\instances\\" + "".join(first_inst) + "\\.minecraft\\options.txt"
    curr_opt_path = path + "\\instances\\" + "".join(curr_inst) + "\\.minecraft\\options.txt"
    
    with open(first_opt_path, "r") as f:
        lines = f.readlines()
        pack_line = lines[33]
    with open(curr_opt_path, "r") as f:
        lines = f.readlines()
        lines[33] = pack_line
    with open(curr_opt_path, "w") as f:
        f.writelines(lines)



#delete the config, mods, packs, and speedrunigt folders for all but the first instance (otherwise copytree will get mad at you)
def del_and_replace(insts, path):
    inst_number = len(insts)
    paths_list = get_paths(insts, path)

    i = 1
    error_count = 0
    delete_error_list = []
    while i< inst_number:

        #if the folder does not exist, ignore the error and continue because it has already been deleted.
        if settings.config:
            try:
                shutil.rmtree(paths_list[0][i])
            except FileNotFoundError:
                pass
            except:
                delete_error_list.append([insts[i], "config"])
                error_count += 1
                pass
        
        if settings.mods:
            try:
                shutil.rmtree(paths_list[1][i])
            except FileNotFoundError:
                pass
            except:
                delete_error_list.append([insts[i], "mods"])
                error_count += 1
                pass
        
        if settings.resourcepacks:
            try:
                shutil.rmtree(paths_list[2][i])
            except FileNotFoundError:
                pass
            except:
                delete_error_list.append([insts[i], "resourcepacks"])
                error_count += 1
                pass

        if settings.speedrunigt:
            try:
                shutil.rmtree(paths_list[3][i])
            except FileNotFoundError:
                pass
            except:
                delete_error_list.append([insts[i], "speedrunigt"])
                error_count += 1
                pass
        
        i += 1

    if error_count != 0:
        errors=del_errors(delete_error_list)
        messagebox.showwarning(title=None, message=errors)

    i=1
    count=0
    error_list = []
    while i< inst_number:

        #if syncing is unsuccessful, continue and let the user know which instances failed.
        if settings.config:
            try:
                shutil.copytree(paths_list[0][0], paths_list[0][i])
            except:
                count += 1
                error_list.append([insts[i], "config"])
                pass
            
        if settings.mods:
            try:
                shutil.copytree(paths_list[1][0], paths_list[1][i])
            except:
                count += 1
                error_list.append([insts[i], "mods"])
                pass

        if settings.resourcepacks:
            try:
                shutil.copytree(paths_list[2][0], paths_list[2][i])
                activate_packs(insts[0], insts[i], path)
            except:
                count += 1
                error_list.append([insts[i], "resourcepacks"])
                pass

        if settings.speedrunigt:
            try:
                shutil.copytree(paths_list[3][0], paths_list[3][i])
            except:
                count += 1
                error_list.append([insts[i], "speedrunigt"])
                pass

        i += 1

    #ok so if you get the warning that you have no folders chosen it doesnt actually stop the program from running so its just gonna skip the "success" thingy
    if (count==0) and (settings.config or settings.mods or settings.resourcepacks or settings.speedrunigt):
        messagebox.showinfo(title=None, message="Success!")

    #show which folders failed
    elif count!=0:
        errors = get_errors(error_list)
        messagebox.showerror(title=None, message=errors)
