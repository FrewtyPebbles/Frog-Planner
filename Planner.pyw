import inspect
import subprocess
from tkinter import *
from datetime import date
import threading
import time
import schedule
from tkinter import messagebox
import playsound
from pystray import MenuItem as item
import pystray
from PIL import Image
from re import sub
from ast import literal_eval as make_tuple


root = Tk()

root.resizable(False, False)

root.title(" Planner ")

root.iconbitmap('planner.ico')

dataVar = ""

plannerData = "PlannerData.tsks"

today = date.today()

# Notification vvvvv

alive = True

def formatDate(_date):
	dmyDate = str(_date)
	if '/' in dmyDate:
		dmyDate = dmyDate.split('/')
		return f"{dmyDate[0].zfill(4)}-{dmyDate[1].zfill(2)}-{dmyDate[2].zfill(2)}"
	elif '-' in dmyDate:
		dmyDate = dmyDate.split('-')
		return f"{dmyDate[0].zfill(4)}-{dmyDate[1].zfill(2)}-{dmyDate[2].zfill(2)}"
	elif '\\' in dmyDate:
		dmyDate = dmyDate.split('\\')
		return f"{dmyDate[0].zfill(4)}-{dmyDate[1].zfill(2)}-{dmyDate[2].zfill(2)}"
	elif '`' in dmyDate:
		dmyDate = dmyDate.split('`')
		return f"{dmyDate[0].zfill(4)}-{dmyDate[1].zfill(2)}-{dmyDate[2].zfill(2)}"
	elif '~' in dmyDate:
		dmyDate = dmyDate.split('~')
		return f"{dmyDate[0].zfill(4)}-{dmyDate[1].zfill(2)}-{dmyDate[2].zfill(2)}"
	elif ',' in dmyDate:
		dmyDate = dmyDate.split(',')
		return f"{dmyDate[0].zfill(4)}-{dmyDate[1].zfill(2)}-{dmyDate[2].zfill(2)}"
	elif '.' in dmyDate:
		dmyDate = dmyDate.split('.')
		return f"{dmyDate[0].zfill(4)}-{dmyDate[1].zfill(2)}-{dmyDate[2].zfill(2)}"
	elif ':' in dmyDate:
		dmyDate = dmyDate.split(':')
		return f"{dmyDate[0].zfill(4)}-{dmyDate[1].zfill(2)}-{dmyDate[2].zfill(2)}"
	else:
		return ""

def rgb_hack(rgb):
	return "#%02x%02x%02x" % rgb

def remindMe(Message, rTime, _date):
	if str(_date) == str(date.today()):
		playsound.playsound('sound/Notif.mp3')
		messagebox.showwarning(f" {rTime} - REMINDER ", f" {Message} ")
		return schedule.CancelJob

def addReminder(Message, rTime, _date):
	theTime = rTime
	if " " in rTime:
		rTimeSplit = rTime.split()
		if rTimeSplit[1] == "pm":
			rTimeSplitTwo = rTimeSplit[0].split(":")
			theTime = f"{int(rTimeSplitTwo[0])+12}:{rTimeSplitTwo[1].zfill(2)}"
		elif rTimeSplit[1] == "am":
			rTimeSplitTwo = rTimeSplit[0].split(":")
			if int(rTimeSplitTwo[0]) == 12:
				theTime = f"00:{rTimeSplitTwo[1]}"
			else:
				theTime = f"{rTimeSplitTwo[0].zfill(2)}:{rTimeSplitTwo[1].zfill(2)}"
	try:
		if _date == "":
			schedule.every().day.at(theTime).do(remindMe, Message, rTime, date.today())
		else:
			schedule.every().day.at(theTime).do(remindMe, Message, rTime, _date)
	except:
		return

def schedulerThread():
	global alive
	while alive:
		schedule.run_pending()
		time.sleep(1)

t1 = threading.Thread(target=schedulerThread, name='t1', daemon=True)
t1.start()

# Notification ^^^^^

def handleData(_today, process):
	global dataVar
	datafile = open(plannerData)

	data = datafile.read()

	datafile.close()
	result = subprocess.check_output(['JIT/luajit', '-l', 'main', '-e', f'{inspect.currentframe().f_code.co_name}("{data.encode()}","{_today}","{process}")'])

	if process == "init":
		if "~missingtoday" in str(result.decode("utf-8")):
			data = open(plannerData,"a")

			data.write(sub("~missingtoday",'',str(result.decode("utf-8"))))

			data.close()
		else:
			tupleData = make_tuple(str(result.decode("utf-8")))
			for i in range(0,len(tupleData)):
				addReminder(tupleData[i][1], tupleData[i][0], date.today())
	else:
		dataVar = result.decode("utf-8")
		dataDisplay.delete("1.0","end")
		dataDisplay.insert(END, dataVar)

def appendData(_date, time, task, process):
	global dataVar
	if process != "remove task" and task == "":
		return
	if process != "remove task" and time == "":
		return
	datafile = open(plannerData)

	data = datafile.read()

	datafile.close()
	result = ""
	if _date == "":
		result = subprocess.check_output(['JIT/luajit', '-l', 'main', '-e', f'{inspect.currentframe().f_code.co_name}("{data.encode()}","{date.today()}","{time}","{task}","{process}")'])
	else:
		if process == "remove task" and time == "" and task == "":
			result = subprocess.check_output(['JIT/luajit', '-l', 'main', '-e', f'{inspect.currentframe().f_code.co_name}("{data.encode()}","{_date}","{time}","{task}","{process}Date")'])
		else:
			result = subprocess.check_output(['JIT/luajit', '-l', 'main', '-e', f'{inspect.currentframe().f_code.co_name}("{data.encode()}","{_date}","{time}","{task}","{process}")'])
	data = open(plannerData,"w")

	data.write(result.decode("utf-8"))

	data.close()
	handleData( date.today(), "show important")

#schedule today's notifications:

handleData(today,"init")

#####

buttons = Frame(root)
displays = Frame(root)
Dates = Frame(root)
buttons2 = Frame(root)

buttons.grid()
displays.grid()
Dates.grid()
buttons2.grid()

background_image= PhotoImage(r"frogs.gif")
background_label = Label(root, i=background_image)

dataDisplay = Text(displays, bg=rgb_hack((179, 216, 242)), fg=rgb_hack((90, 3, 0)), height = 20, width = 40)
displayDayData = Button(buttons, bg=rgb_hack((85, 114, 133)), fg=rgb_hack((255, 255, 255)), text=" Today's task(s) ", command=lambda:handleData( formatDate(date.today()), "show today"))
displayImportantData = Button(buttons, bg=rgb_hack((85, 114, 133)), fg=rgb_hack((255, 255, 255)), text=" All task(s) ", command=lambda:handleData( formatDate(date.today()), "show important"))
DateText = Text(Dates,relief=RIDGE, bg=rgb_hack((255, 192, 150)), fg=rgb_hack((0, 32, 69)), height = 1, width = 13)
TimeText = Text(buttons2, bg=rgb_hack((242, 233, 203)), height = 1, width = 9)
TaskText = Text(buttons2, bg=rgb_hack((242, 233, 203)), height = 2, width = 28)
appendTaskData = Button(buttons2, bg=rgb_hack((90, 122, 173)), fg=rgb_hack((255, 255, 255)), text="Add task", command=lambda:[appendData( formatDate(DateText.get(1.0, "end-1c")), TimeText.get(1.0, "end-1c"), TaskText.get(1.0, "end-1c"), "append task"), addReminder(TaskText.get(1.0, "end-1c"), TimeText.get(1.0, "end-1c"), formatDate(DateText.get(1.0, "end-1c")))])
deleteTaskData = Button(buttons2, bg=rgb_hack((90, 122, 173)), fg=rgb_hack((255, 255, 255)), text="Remove task", command=lambda:[appendData( formatDate(DateText.get(1.0, "end-1c")), TimeText.get(1.0, "end-1c"), TaskText.get(1.0, "end-1c"), "remove task")])

root.config(bg=rgb_hack((77, 191, 143)))
buttons2.config(bg=rgb_hack((77, 191, 143)))
Dates.config(bg=rgb_hack((77, 191, 143)))

dataDisplay.grid()
displayDayData.grid(row=0,column=0)
displayImportantData.grid(row=0,column=1)
DateText.grid(row=0,column=0,pady=( 5, 5 ))
TimeText.grid(row=0,column=0,rowspan=2, padx=( 0, 0 ))
TaskText.grid(row=0,column=1,rowspan=2, sticky='ns')
appendTaskData.grid(row=0,column=2, sticky='nesw')
deleteTaskData.grid(row=1,column=2, sticky='nesw')

##############

# Define a function for quit the window
def quit_window(icon):
	icon.stop()
	root.destroy()

# Define a function to show the window again
def show_window(icon):
	icon.stop()
	root.after(0,root.deiconify())
	root.lift()
	root.attributes('-topmost',1)
	root.after_idle(root.attributes,'-topmost',0)

# Hide the window and show on the system taskbar
def hide_window():
	root.withdraw()
	image=Image.open("planner.ico")
	menu=(item('Open Planner', show_window, default=True), item('Quit', quit_window))
	icon=pystray.Icon("name", image, "Planner", menu)
	icon.run()

root.protocol('WM_DELETE_WINDOW', hide_window)

##############

root.mainloop()