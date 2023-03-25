from settings import *
from sync import *
from tkinter import *
from tkinter import filedialog
from os import path
import groups
from random import uniform

#create root window
root = Tk()
root.geometry("700x500")
root.config(background="#FFE2FF")

#sets the multimc path given and opens other widget options when user inputs multimc path manually
def use_mc_manual():
    global multipath 
    multipath = findmc.get()
    if path.exists("".join(findmc.get()) + "\\instances"):
        f = open("mcpath.txt", "w")
        f.write(findmc.get())
        f.close()
        try:
            usebutton_browse.config(state="disabled")
            mc_label.config(text=findmc.get())
        except:
            pass
        usebutton_manual.config(state="disabled")
        browsemc.config(state="disabled")
        groups.find_multimc(multipath)
        create_group_widget()
        create_radio_buttons()
        create_check_buttons()
        create_sync()
        create_colon3()
    else:
        messagebox.showerror(title=None, message="Please make sure your MultiMC path is set correctly.")

#sets multimc path and opens other widgets when user browses for multimc folder
def use_mc_browse():
    global multipath
    multipath = directory
    check = "".join(directory) + "\\instances"
    if path.exists(check):
        f = open("mcpath.txt", "w")
        f.write(directory)
        f.close()
        usebutton_browse.config(state="disabled")
        usebutton_manual.config(state="disabled")
        browsemc.config(state="disabled")
        groups.find_multimc(multipath)
        create_group_widget()
        create_radio_buttons()
        create_check_buttons()
        create_sync()
        create_colon3()
    else:
        messagebox.showerror(title=None, message="Please make sure your MultiMC path is set correctly.")

#opens the file browser when user presses browse button to search for multimc path
def browse_folder():
    global directory
    global usebutton_browse
    global mc_label
    directory = filedialog.askdirectory()
    mc_label = Label(root, text=directory, width=60, anchor="w", background="#FFE2FF")
    usebutton_browse = Button(root, background="#FFA9FF", text="use", command=use_mc_browse)
    mc_label.place(relx=0.02, rely=0.11, anchor=W)
    usebutton_browse.place(relx=0.6, rely=0.11, anchor=CENTER)
        
#create the sync button which will activate the program
def create_sync():
    sync_button = Button(root, background="#FFA9FF", text='sync', height="2", width="8", command=lambda: [find_instances(method.get())])
    sync_button.place(relx=0.8, rely=0.45, anchor=CENTER)


#creates the list of multimc groups for the user to choose from in a dropdown menu
def create_group_widget():
    frame = Frame(root)
    frame.place(relx=0.6, rely=0.3, anchor=N)
    frame.config(background="#FFE2FF")
    try:
        destroy_groupings()
    except:
        pass #if there is an error, the widgets dont exist at all and dont need to be destroyed.
    global groupings
    global groupwidget_label
    ahh = groups.find_groups()
    groupings = Listbox(frame, selectmode = "single")

    #make sure it cant go off screen
    if len(ahh)>15:
        groupings.config(height=15)
    else:
        groupings.config(height=len(ahh))

    for each_item in range(len(ahh)):
        groupings.insert(END, ahh[each_item])
        groupings.itemconfig(each_item)
    
    global find_first_instance
    find_first_instance = Button(root, text="What is my\nfirst instance?", background="#ffa9ff", command=show_first_inst)
    find_first_instance.place(relx=0.8, rely=0.65, anchor=CENTER)
        
    #packing the listbox into the frame automatically makes it scrollable
    groupings.pack()
    groupwidget_label = Label(root, text="Select which group you would like to sync.\nThey will sync to the first instance in that group", background="#FFE2FF")
    groupwidget_label.place(relx=0.6, rely=0.2, anchor=N)

#creates the list of instances for the user to choose from
def create_instance_widget():
    frame = Frame(root)
    frame.place(relx=0.6, rely=0.3, anchor=N)
    frame.config(background="#FFE2FF")
    try:
        destroy_instances()
    except:
        pass #if there is an error, the widgets dont exist at all and dont need to be destroyed.
    global instances
    global instwidget_label
    ahh = groups.find_instances()
    instances = Listbox(frame, selectmode = "multiple")

    #make sure it cant go off screen
    if len(ahh)>15:
        instances.config(height=15)
    else:
        instances.config(height=len(ahh))
        
    for each_item in range(len(ahh)):
        instances.insert(END, ahh[each_item])
        instances.itemconfig(each_item)

    #packing the listbox into the frame automatically makes it scrollable
    instances.pack()
    instwidget_label = Label(root, text="Select which instances to sync.\nThey will sync to the whichever is highest in the list,\n NOT the one you click first.", background="#FFE2FF")
    instwidget_label.place(relx=0.6, rely=0.2, anchor=N)


#if you press the radiobuttons again they create these widgets again so instead i am going to delete the old ones and replace them
def destroy_groupings():
    groupings.destroy()
    groupwidget_label.destroy()
    find_first_instance.destroy()
def destroy_instances():
    instances.destroy()
    instwidget_label.destroy()

#creates the buttons which allow user to choose between groups and instances
def create_radio_buttons():
    global method
    radio_label = Label(root, text="Select groups if you have a multimc group\nfor the instances you want to sync", background="#FFE2FF")
    method= IntVar()
    bygroups = Radiobutton(root, background="#FFE2FF", text="groups", variable=method, value=0, command=lambda: [instwidget_label.destroy(), instances.destroy(), create_group_widget()])
    byinst = Radiobutton(root, background="#FFE2FF", text="instances", variable=method, value=1, command=lambda: [groupings.destroy(), find_first_instance.destroy(), create_instance_widget()])
    bygroups.place(relx=0.02, rely=0.3, anchor=W)
    byinst.place(relx=0.02, rely=0.35, anchor=W)
    radio_label.place(relx=0.02, rely=0.2, anchor=NW)

#creates the options for the user to choose which folders to sync
def create_check_buttons():
    global config
    global mods
    global resourcepacks
    global speedrunigt
    check_label = Label(root, text="Select which folders you would like to sync", background="#FFE2FF")
    config =IntVar()
    mods=IntVar()
    resourcepacks=IntVar()
    speedrunigt=IntVar()
    configbtn = Checkbutton(root, background="#FFE2FF", text='config', variable=config, onvalue=1, offvalue=0, command=check_config)
    modsbtn = Checkbutton(root, background="#FFE2FF", text='mods', variable=mods, onvalue=1, offvalue=0, command=check_mods)
    packsbtn = Checkbutton(root, background="#FFE2FF", text='resourcepacks', variable=resourcepacks, onvalue=1, offvalue=0, command=check_packs)
    igtbtn = Checkbutton(root, background="#FFE2FF", text='speedrunigt', variable=speedrunigt, onvalue=1, offvalue=0, command=check_igt)
    configbtn.place(relx=0.02, rely=0.5, anchor=W)
    modsbtn.place(relx=0.02, rely=0.55, anchor=W)
    packsbtn.place(relx=0.02, rely=0.6, anchor=W)
    igtbtn.place(relx=0.02, rely=0.65, anchor=W)
    check_label.place(relx=0.02, rely=0.45, anchor=W)

#finds which folders the user has chosen and puts them into the settings module
def check_config():
    add_config(config.get())
def check_mods():
    add_mods(mods.get())
def check_packs():
    add_resourcepacks(resourcepacks.get())
def check_igt():
    add_speedrunigt(speedrunigt.get())

#tells the user which instance in that group is the first one, which all other instances will sync to
def show_first_inst():
    selected = groupings.curselection()
    if len(selected)==0:
        messagebox.showerror(title=None, message="Please select a group to check")
    for i in selected:
        group = groupings.get(i)
    insts = groups.find_instances_from_groups(group)
    messagebox.showinfo(title=None, message=f"your first instance is {insts[0]}. All other instances in this group will sync to this one.")

#figure out if inst or groups is selected, and then get which instances to sync from the dropdown menues
def find_instances(radio):

    #check that user has chosen at least one folder
    if config.get()==0 and mods.get()==0 and resourcepacks.get()==0 and speedrunigt.get()==0:
        messagebox.showwarning(title=None, message="You have no folders selected")
    
    #if groups is selected
    if radio==0:
        selected = groupings.curselection()
        if len(selected)==0:
            messagebox.showerror(title=None, message="Please select a group to sync")
        for i in selected:
            group = groupings.get(i)
        insts = groups.find_instances_from_groups(group)
        del_and_replace(insts, multipath)

    #if instances is selected
    if radio==1:
        selected = instances.curselection()
        if len(selected)==0:
            messagebox.showerror(title=None, message="Please select instances to sync")
        if len(selected)==1:
            messagebox.showerror(title=None, message="Please select more than one instance to sync")
        insts = []
        for i in selected:
            inst = instances.get(i)
            insts.append(inst)
        del_and_replace(insts, multipath)


#silly little mini game
def create_colon3():
    global colon3
    colon3 = Button(root, height=2, width=4, background="#CCE5FF", text=":3", command=movebutton)
    colon3.place(relx=0.9, rely=0.9, anchor=CENTER)
def movebutton():
    x=uniform(0.1,0.9)
    y=uniform(0.1,0.9)
    colon3.place(relx=x, rely=y)
    colon3.lift()

#create the initial buttons/labels on the gui
browsemc = Button(root, background="#FFA9FF", text="browse folders", command=browse_folder)
path_label = Label(root, text="or enter your MultiMC path manually:", background="#FFE2FF")
findmc = Entry(root, width=50) #enter multimc path
usebutton_manual = Button(root, background="#FFA9FF", text="use", command=use_mc_manual) #press use or it doesnt work
quit_button = Button(root, background="#FFA9FF", text='quit', height="2", width="7", command=root.destroy)

#save mcpath for reuse
try:
    #create mcpath.txt when the user runs program for the first time
    f = open("mcpath.txt", "x")
    f.close()
except:
    #opens the rest of the program to the user, as if they had pressed a "use" button
    f = open("mcpath.txt", "r+")
    multipath = f.read()
    check = "".join(multipath) + "\\instances"
    if path.exists(check):
        usebutton_manual.config(state="disabled")
        browsemc.config(state="disabled")
        groups.find_multimc(multipath)
        create_group_widget()
        create_radio_buttons()
        create_check_buttons()
        create_sync()
        create_colon3()
        mc_label = Label(root, text=f.read(), width=60, anchor="w", background="#FFE2FF")
        f.close()

#place the initial buttons/labels on the gui
browsemc.place(relx=0.09, rely=0.05, anchor=CENTER)
path_label.place(relx=0.3, rely=0.05, anchor=CENTER)
findmc.place(relx=0.67, rely=0.05, anchor=CENTER)
usebutton_manual.place(relx=0.92, rely=0.05, anchor=CENTER)
quit_button.place(relx=0.02, rely=0.98, anchor=SW)

root.title('instanceSync')
root.mainloop()
