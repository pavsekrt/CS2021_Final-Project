##Python project - Ryan Pavsek
from save import save
from datetime import datetime
import datetime
import os
import pygubu
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox

##GLOBAL VARIABLES
assignmentList = [] #main list (gets displayed)
tempName, tempLabel, tempDescription = '', '', ''
tempDueYear, tempDueMonth, tempDueDay, tempDueHour, tempDueMin = 0, 0, 0, 0, 0


def printAssignmentList():#prints assignmentList
    global assignmentList
    print(assignmentList)
    for i in assignmentList:
        print(i.getName(),i.getDueDate())


class Assignment(object):
    def __init__(self, name, dueYear, dueMonth, dueDay, dueHour=24, dueMin=0, label='', description=''):
        self.name = name
        self.dueDate = datetime.datetime(year=dueYear, month=dueMonth, day=dueDay, hour=dueHour, minute=dueMin)
        self.label = label
        self.description = description
    def setName(self, name):# name setter
        self.name = name
    def getName(self):# name getter
        return self.name
    def setDueDate(self, dueDate):# date setter
        self.dueDate = dueDate
    def getDueDate(self): # date getter
        return self.dueDate
    def setLabel(self, label):# label setter
        self.label = label
    def getLabel(self): # label getter
        return self.label
    def setDescription(self, description): #description setter
        self.description = description
    def getDescription(self): #description getter
        return self.description
    #USED FOR SORTING
    __gt__ = lambda self, other: other.getDueDate() > self.getDueDate() # sets greater than
    __lt__ = lambda self, other: other.getDueDate() < self.getDueDate() # sets less than
    __eq__ = lambda self, other: other.getDueDate() == self.getDueDate()# sets equal to



def saveToFile(lst):
    saveString = ''#create empty string
    try:
        os.remove('savedAssignments.txt')#delete old save
    except :
        pass
    for i in lst:# set saveString to assignmentList
        saveString += i.getName() + '\t' + i.getDueDate().strftime('%Y %m %d %H %M') + '\t' + i.getLabel() + '\t' + i.getDescription()
    save(saveString, 'savedAssignments.txt') # using save API set savedAssignments.txt to saveString

def loadFromFile():
    lst = []# create empty list
    try :
        with open('savedAssignments.txt') as f:#open save file
            for line in f:#read save file
                nam, dat, lab, des = line.split('\t')
                d = datetime.datetime.strptime(dat, '%Y %m %d %H %M')
                #write save file entry to lst
                lst.append(Assignment(nam, d.year, d.month, d.day, d.hour, d.minute, lab, des))
        print("save file loaded")
    except :
        print("no previous save file")#no previous save
    return lst

def removeAssignment(a):
    try:
        j = 0 #location in list
        for i in assignmentList:
            if str(a[0]) == str(i.getName()):
                if str(a[1]) == str(i.getDueDate()):
                    if str(a[2]) == str(i.getLabel()):
                        if str(a[3]) == str(i.getDescription()):
                            assignmentList.pop(j)#remove assignment
                            saveToFile(assignmentList)#save to data file
            j+=1#increment location

    except:
        pass

def start():
    try:
        global assignmentList
        assignmentList = loadFromFile()#load old assignments
        assignmentList.sort()#sort assignments
        printAssignmentList()#print in terminal assignments
    except:
        pass


class Application(tk.Frame):
    def __init__(self, master):
        # Create a builder
        self.builder = builder = pygubu.Builder()
        # Load an ui file
        builder.add_from_file('main.ui')

        # Create the widgets using a master as parent
        self.Frame_main = builder.get_object('Frame_main', master)
        self.Button_new = builder.get_object('Button_new', master)
        self.treeview = builder.get_object('treeview', master)
        self.column_name = builder.get_object('column_name', master)
        self.column_date = builder.get_object('column_date', master)
        self.column_label = builder.get_object('column_label', master)
        self.column_description = builder.get_object('column_description', master)
        builder.connect_callbacks(self)

    def refreshList(self):
        global assignmentList
        assignmentList.sort()#sort assignmentList
        self.treeview.delete(*self.treeview.get_children())#delete all items in treeview
        for i in assignmentList:#insert all items in assignmentList into treeview
            self.treeview.insert("" , 0,    text=i.getName(), values=(i.getName(), i.getDueDate(), i.getLabel(), i.getDescription()))

    def delete(self):
        try:
        print('Delete')
            selected_item = self.treeview.selection()[0] ## get selected item
            t = self.treeview.item(self.treeview.selection())["values"] # get information from selection
            removeAssignment(t) #remove item from assignmentList
            self.treeview.delete(selected_item)# remove from treeview
            self.refreshList()
        except:
            print('No Selection')


    def on_newbutton(self):
        print("New Button Press")
        global assignmentList
        try:
            #add new assignment to assignmentList
            assignmentList.append(Assignment(tempName, tempDueYear, tempDueMonth, tempDueDay, tempDueHour, tempDueMin, tempLabel, tempDescription))
            assignmentList.sort()
            saveToFile(assignmentList)##save
            self.refreshList()
        except :
            messagebox.showinfo('Error', 'Invalid Assignment')#if invalid data is passed


    def setTempName(self, P):#sets tempName to current input
        print('Setting tempName')
        global tempName
        tempName = P
        print(tempName)
        return True
    def setTempLabel(self, P):#sets tempLabel to current input
        print('Setting tempLabel')
        global tempLabel
        tempLabel = P
        print(tempLabel)
        return True
    def setTempDescription(self, P):#sets tempDescription to current input
        print('Setting tempDescription')
        global tempDescription
        tempDescription = P
        print(tempDescription)
        return True
    def setTempDueDay(self, P):#sets tempDueDay to current input
        print('Setting tempDueDay')
        global tempDueDay
        try:
            tempDueDay = int(P)#set string to int
            print(tempDueDay)
        except :
            pass
        return True
    def setTempDueMonth(self, P):#sets tempDueMonth to current input
        print('Setting tempDueMonth')
        global tempDueMonth
        D = 0
        #string to int
        if P == "January":
            D = 1
        elif P == "February":
            D = 2
        elif P == "March":
            D = 3
        elif P == "April":
            D = 4
        elif P == "May":
            D = 5
        elif P == "June":
            D = 6
        elif P == "July":
            D = 7
        elif P == "August":
            D = 8
        elif P == "September":
            D = 9
        elif P == "October":
            D = 10
        elif P == "November":
            D = 11
        elif P == "December":
            D = 12
        tempDueMonth = D
        print(tempDueMonth)
        return True
    def setTempDueYear(self, P):#sets tempDueYear to current input
        print('Setting tempDueYear')
        global tempDueYear
        try:
            tempDueYear = int(P)#set string to int
            print(tempDueYear)
        except :
            pass
        return True
    def setTempDueHour(self, P):#sets tempDueHour to current input
        print('Setting tempDueHour')
        global tempDueHour
        try:
            tempDueHour = int(P)#set string to int
            print(tempDueHour)
        except :
            pass
        return True
    def setTempDueMin(self, P):#sets tempDueMin to current input
        print('Setting tempDueMin')
        global tempDueMin
        try:
            tempDueMin = int(P)#set string to int
            print(tempDueMin)
        except :
            pass
        return True


if __name__ == '__main__':
    start()#startup (load)
    root = tk.Tk()# create tkinter object
    root.title("Assignment Manager")# set title
    app = Application(root)#create instance of Application
    app.refreshList()#adds items to treview
    root.mainloop()####MAINLOOP####
