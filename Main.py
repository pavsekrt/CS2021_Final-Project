
# from kivy.uix.floatlayout import FloatLayout
# from kivy.base import runTouchApp
# from kivy.uix.button import Button
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

assignmentList = []
tempName, tempLabel, tempDescription = '', '', ''
tempDueYear, tempDueMonth, tempDueDay, tempDueHour, tempDueMin = 0, 0, 0, 0, 0


def printAssignmentList():
    global assignmentList
    print(assignmentList)
    for i in assignmentList:
        print(i.getName(),i.getDueDate())


class Assignment(object):
    # def __init__(self, name, dueYear, dueMonth, dueDay, dueHour=24, dueMin=0, label='None', description='No Description'):
    #     self.name = name
    #     self.dueDate = datetime.datetime(year=dueYear, month=dueMonth, day=dueDay, hour=dueHour, minute=dueMin)
    #     self.label = label
    #     self.description = description
    def __init__(self, name, dueYear, dueMonth, dueDay, dueHour=24, dueMin=0, label='', description=''):
        self.name = name
        self.dueDate = datetime.datetime(year=dueYear, month=dueMonth, day=dueDay, hour=dueHour, minute=dueMin)
        self.label = label
        self.description = description
    # def __init__(self, name, date, label='None', description='No Description'):
    #     self.name = name
    #     self.dueDate = date
    #     self.label = label
    #     self.description = description
    def setName(self, name):
        self.name = name
    def getName(self):
        return self.name
    def setDueDate(self, dueDate):
        self.dueDate = dueDate
    def getDueDate(self):
        return self.dueDate
    def setLabel(self, label):
        self.label = label
    def getLabel(self):
        return self.label
    def setDescription(self, description):
        self.description = description
    def getDescription(self):
        return self.description
    __gt__ = lambda self, other: other.getDueDate() > self.getDueDate()
    __lt__ = lambda self, other: other.getDueDate() < self.getDueDate()
    __eq__ = lambda self, other: other.getDueDate() == self.getDueDate()



def saveToFile(lst):
    saveString = ''
    try:
        os.remove('savedAssignments.txt')
    except :
        pass
    for i in lst:
        saveString += i.getName() + '\t' + i.getDueDate().strftime('%Y %m %d %H %M') + '\t' + i.getLabel() + '\t' + i.getDescription()
    save(saveString, 'savedAssignments.txt')

def loadFromFile():
    lst = []
    try :
        with open('savedAssignments.txt') as f:
            for line in f:
                nam, dat, lab, des = line.split('\t')
                d = datetime.datetime.strptime(dat, '%Y %m %d %H %M')
                lst.append(Assignment(nam, d.year, d.month, d.day, d.hour, d.minute, lab, des))
        print("save file loaded")
    except :
        print("no previous save file")
    return lst

def removeAssignment(a):
    try:
        j = 0
        for i in assignmentList:
            if str(a[0]) == str(i.getName()):
                if str(a[1]) == str(i.getDueDate()):
                    if str(a[2]) == str(i.getLabel()):
                        if str(a[3]) == str(i.getDescription()):
                            assignmentList.pop(j)
                            saveToFile(assignmentList)
            j+=1

    except:
        pass

def start():
    try:
        global assignmentList
        assignmentList = loadFromFile()
        assignmentList.sort()
        printAssignmentList()
    except:
        print("no previous save file")


class Application(tk.Frame):
    def __init__(self, master):
        #1: Create a builder
        self.builder = builder = pygubu.Builder()

        #2: Load an ui file
        builder.add_from_file('main.ui')

        #3: Create the widget using a master as parent
        self.Frame_main = builder.get_object('Frame_main', master)
        self.Button_new = builder.get_object('Button_new', master)
        self.treeview = builder.get_object('treeview', master)
        # self.column_del = builder.get_object('column_del', master)
        self.column_name = builder.get_object('column_name', master)
        self.column_date = builder.get_object('column_date', master)
        self.column_label = builder.get_object('column_label', master)
        self.column_description = builder.get_object('column_description', master)
        # self.Button_new = ttk.Button.(text="TEST")
        # self.treeview.insert("" , 0,    text="X", values=("1A","1b"))
        builder.connect_callbacks(self)

    def refreshList(self):
        global assignmentList
        assignmentList.sort()
        self.treeview.delete(*self.treeview.get_children())
        for i in assignmentList:
            self.treeview.insert("" , 0,    text=i.getName(), values=(i.getName(), i.getDueDate(), i.getLabel(), i.getDescription()))

    def delete(self):
        # try:
        print('Delete')
        selected_item = self.treeview.selection()[0] ## get selected item
        # t = self.treeview.item(self.treeview.focus()).values
        t = self.treeview.item(self.treeview.selection())["values"]
        removeAssignment(t)
        self.treeview.delete(selected_item)
        self.refreshList()
        # except:
        #     print('No Selection')

    def on_treecolumn_click(self):
        return True

    def on_newbutton(self):
        print("New Button Press")
        global assignmentList
        try:
            # print('N: ', tempName, ' Y: ', tempDueYear, ' M: ', tempDueMonth, ' D: ', tempDueDay, ' H: ', tempDueHour, ' M: ', tempDueMin, ' L: ', tempLabel, ' D: ', tempDescription)
            assignmentList.append(Assignment(tempName, tempDueYear, tempDueMonth, tempDueDay, tempDueHour, tempDueMin, tempLabel, tempDescription))
            assignmentList.sort()
            # printAssignmentList()
            saveToFile(assignmentList)
            self.refreshList()
        except :
            messagebox.showinfo('Error', 'Invalid Assignment')


    def setTempName(self, P):
        print('Setting tempName')
        global tempName
        tempName = P
        print(tempName)
        return True
    def setTempLabel(self, P):
        print('Setting tempLabel')
        global tempLabel
        tempLabel = P
        print(tempLabel)
        return True
    def setTempDescription(self, P):
        print('Setting tempDescription')
        global tempDescription
        tempDescription = P
        print(tempDescription)
        return True
    def setTempDueDay(self, P):
        print('Setting tempDueDay')
        global tempDueDay
        try:
            tempDueDay = int(P)
            print(tempDueDay)
        except :
            pass
        return True
    def setTempDueMonth(self, P):
        print('Setting tempDueMonth')
        global tempDueMonth
        D = 0
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
    def setTempDueYear(self, P):
        print('Setting tempDueYear')
        global tempDueYear
        try:
            tempDueYear = int(P)
            print(tempDueYear)
        except :
            pass
        return True
    def setTempDueHour(self, P):
        print('Setting tempDueHour')
        global tempDueHour
        try:
            tempDueHour = int(P)
            print(tempDueHour)
        except :
            pass
        return True
    def setTempDueMin(self, P):
        print('Setting tempDueMin')
        global tempDueMin
        try:
            tempDueMin = int(P)
            print(tempDueMin)
        except :
            pass
        return True


if __name__ == '__main__':
    start()
    # refreshList()
    root = tk.Tk()
    root.title("Assignment Manager")
    app = Application(root)
    app.refreshList()
    root.mainloop()
