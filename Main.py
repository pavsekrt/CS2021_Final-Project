
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
    __gt__ = lambda self, other: other.getDueDate() < self.getDueDate()
    __lt__ = lambda self, other: other.getDueDate() > self.getDueDate()
    __eq__ = lambda self, other: other.getDueDate() == self.getDueDate()



def saveToFile(lst):
    saveString = ''
    try:
        os.remove('savedAssignments.txt')
    except :
        pass
    for i in lst:
        saveString += i.getName() + '\t' + i.getDueDate().strftime('%Y %m %d %H %M') + '\t' + i.getLabel() + '\t' + i.getDescription() + '\n'
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


def start():
    try:
        global assignmentList
        assignmentList = loadFromFile()
        assignmentList.sort()
        printAssignmentList()
    except:
        print("no previous save file")



###START###

# def timeDiff(t):
#     t = datetime.datetime.now().date()
#
#
# a = Assignment('A1', 2032, 6, 9, 1, 1, 'b', 'c')
# b = Assignment('B1', 1980, 7, 19)
# c = Assignment('C1', 2016, 11, 29)
# d = Assignment('D1', 2000, 12, 1)
# print(a.getName())
# print(a.getDueDate())
# print(a.getLabel())
# print(a.getDescription())
# print(a.getTags())
# lst = [Assignment('A1', 1994, 6, 9),Assignment('B1', 1980, 7, 19),Assignment('C1', 2016, 11, 29),Assignment('D1', 2000, 12, 1)]

# # saveToFile(lst)
# a = loadFromFile()
# print(a)
# for i in lst:
#     print(i.getName(),i.getDueDate())
# print(sorted(lst))
# lst.sort()
# for i in lst:
#     print(i.getName(), i.getDueDate())


# today = datetime.datetime.now().date()
# d = datetime.datetime(year=1994, month=6, day=9, hour=12, minute=30)
# # datetime.timedelta(t, t2)
# print("Today is {}".format(d))
# print("Today is {}".format(datetime.timedelta(t, d)))

class Application(tk.Frame):
    def __init__(self, master):
        #1: Create a builder
        self.builder = builder = pygubu.Builder()

        #2: Load an ui file
        builder.add_from_file('main.ui')

        #3: Create the widget using a master as parent
        self.Frame_main = builder.get_object('Frame_main', master)
        self.Button_new = builder.get_object('Button_new', master)
        # self.Button_new = ttk.Button.(text="TEST")
        builder.connect_callbacks(self)





    def on_newbutton(self):
        print("New Button Press")
        global assignmentList
        try:
            # print('N: ', tempName, ' Y: ', tempDueYear, ' M: ', tempDueMonth, ' D: ', tempDueDay, ' H: ', tempDueHour, ' M: ', tempDueMin, ' L: ', tempLabel, ' D: ', tempDescription)
            assignmentList.append(Assignment(tempName, tempDueYear, tempDueMonth, tempDueDay, tempDueHour, tempDueMin, tempLabel, tempDescription))
            assignmentList.sort()
            # printAssignmentList()
            saveToFile(assignmentList)
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
    root = tk.Tk()
    root.title("Assignment Manager")
    app = Application(root)
    root.mainloop()
