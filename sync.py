import settings
import os
import shutil


#turn the instance naming convention into a list which will be appended later
inst_list = list(settings.inst_setup)

#names of instances put in a list, which will be used to say which folders have been synced successfully or unsuccessfully.
ordered_insts = []
if len(settings.custom_paths) == 0:
    for i in range(settings.inst_number):
        item = inst_list
        item = [w.replace('*', str(i)) for w in settings.inst_setup]
        item = "".join(item)
        ordered_insts.append(item)
else:
    ordered_insts = settings.custom_paths

#update inst_number in case of a custom list of instances
if len(settings.custom_paths) == 0:
    inst_number = settings.inst_number
else:
    inst_number = len(settings.custom_paths)

#determine if there is a custom instance list
Custom = False
if len(settings.custom_paths) != 0:
    Custom = True

#get the path to all custom instances and list them in order
def get_custom_instances():
    global inst_paths
    inst_paths = []

    i=0
    while i< inst_number:
        inst_path = settings.mc_path + "\\instances\\" + "".join(settings.custom_paths[i]) + "\\.minecraft"
        inst_paths.append(inst_path)
        i += 1
    
    return inst_paths

#get the config paths for all instances and list them in order
def get_configs():
    global config_paths
    config_paths = [] 

    if Custom:
        i=0
        while i< inst_number:
            config_path = "".join(inst_paths[i]) + "\\config"
            config_paths.append(config_path)
            i += 1

        return config_paths

    else:
        i=1
        while i<= inst_number:
            new_list = inst_list
            new_list = [w.replace('*', str(i)) for w in inst_list]
            config_path = settings.mc_path + "\\instances\\" + "".join(new_list) + "\\.minecraft\\config"
            config_paths.append(config_path)
            i += 1

        return config_paths

#get the mods paths for all instances and list them in order
def get_mods():
    global mods_paths
    mods_paths = []

    if Custom:
        i=0
        while i< inst_number:
            mods_path = "".join(inst_paths[i]) + "\\mods"
            mods_paths.append(mods_path)
            i += 1

        return mods_paths

    else:
        i=1
        while i<= inst_number:
            new_list = inst_list
            new_list = [w.replace('*', str(i)) for w in inst_list]
            mods_path = settings.mc_path + "\\instances\\" + "".join(new_list) + "\\.minecraft\\mods"
            mods_paths.append(mods_path)
            i += 1

        return mods_paths

#get the resourcepacks paths for all instances and list them in order
def get_packs():
    global packs_paths
    packs_paths = []

    if Custom:
        i=0
        while i< inst_number:
            packs_path = "".join(inst_paths[i]) + "\\resourcepacks"
            packs_paths.append(packs_path)
            i += 1

        return packs_paths

    else:
        i=1
        while i<= inst_number:
            new_list = inst_list
            new_list = [w.replace('*', str(i)) for w in inst_list]
            packs_path = settings.mc_path + "\\instances\\" + "".join(new_list) + "\\.minecraft\\resourcepacks"
            packs_paths.append(packs_path)
            i += 1

        return packs_paths

#get the speedrunigt paths for all instances and list them in order
def get_igt():
    global igt_paths
    igt_paths = []

    if Custom:
        i=0
        while i< inst_number:
            igt_path = "".join(inst_paths[i]) + "\\speedrunigt"
            igt_paths.append(igt_path)
            i += 1

        return igt_paths

    else:
        i=1
        while i<= inst_number:
            new_list = inst_list
            new_list = [w.replace('*', str(i)) for w in inst_list]
            igt_path = settings.mc_path + "\\instances\\" + "".join(new_list) + "\\.minecraft\\speedrunigt"
            igt_paths.append(igt_path)
            i += 1

        return igt_paths

#delete the config, mod, packs, and speedrunigt folders for all but the first instance
def delete_folders():
    i = 1
    while i< inst_number:

        #if the folder does not exist, ignore the error and continue because it has already been deleted.
        if settings.config:
            try:
                shutil.rmtree(config_paths[i])
            except FileNotFoundError:
                pass
            except:
                input(f"{ordered_insts[i+1]} config folde failed to delete. Press enter to continue.")
                pass

        if settings.mods:
            try:
                shutil.rmtree(mods_paths[i])
            except FileNotFoundError:
                pass
            except:
                input(f"{ordered_insts[i+1]} mods folder failed to delete. Press enter to continue.")
                pass
        
        if settings.resourcepacks:
            try:
                shutil.rmtree(packs_paths[i])
            except FileNotFoundError:
                pass
            except:
                input(f"{ordered_insts[i+1]} resourcepacks folder failed to delete. Press enter to continue.")
                pass

        if settings.speedrunigt:
            try:
                shutil.rmtree(igt_paths[i])
            except FileNotFoundError:
                pass
            except:
                print(f"{ordered_insts[i+1]} speedrunigt folder failed to delete. Press enter to continue.")
                pass

        i += 1

#copy the config, mod, packs, and speedrunigt folders from first instance and put it in the others
def replace_folders():
    i=1
    while i< inst_number:

        #if syncing is unsuccessful, continue and let the user know which instances failed.
        if settings.config:
            try:
                shutil.copytree(config_paths[0], config_paths[i])
            except FileNotFoundError:
                input("Please make sure your instances/multimc path are named correctly. Press enter to exit")
                exit()
            except:
                input(f"{ordered_insts[i]} config folder failed to sync. Press enter to continue.")
                pass
            print(f"{ordered_insts[i]} config folder sync successful")

        if settings.mods:
            try:
                shutil.copytree(mods_paths[0], mods_paths[i])
            except FileNotFoundError:
                input("Please make sure your instances/mutlimc path are named correctly. Press enter to exit")
                exit()
            except:
                input(f"{ordered_insts[i]} mods folder failed to sync. Press enter to continue.")
                pass
            print(f"{ordered_insts[i]} mods folder sync successful")

        if settings.resourcepacks:
            try:
                shutil.copytree(packs_paths[0], packs_paths[i])
            except FileNotFoundError:
                input("Please make sure your instances/mulitmc path are named correctly. Press enter to exit")
                exit()
            except:
                input(f"{ordered_insts[i]} resourcepacks folder failed to sync. Press enter to continue.")
                pass
            print(f"{ordered_insts[i]} resourcepacks folder sync successful")

        if settings.speedrunigt:
            try:
                shutil.copytree(igt_paths[0], igt_paths[i])
            except FileNotFoundError:
                input("Please make sure your instances/mutlimc path are named correctly. Press enter to exit")
                exit()
            except:
                input(f"{ordered_insts[i]} speedrunigt folder failed to sync. Press enter to continue.")
                pass
            print(f"{ordered_insts[i]} speedrunigt folder sync successful")

        i += 1

if Custom:
    get_custom_instances()

get_configs()
get_mods()
get_packs()
get_igt()

delete_folders()
replace_folders()

input("\nSyncing complete. Press enter to exit.\n")