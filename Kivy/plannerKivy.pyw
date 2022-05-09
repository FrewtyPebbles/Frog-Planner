from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
import inspect
import subprocess
from datetime import date
import threading
import time
import schedule
import playsound
import plyer
from re import sub
from ast import literal_eval as make_tuple


class PlannerScreen(BoxLayout):
    rootDisplay= ObjectProperty(None)
    rootdate= ObjectProperty(None)
    roottime= ObjectProperty(None)
    roottask= ObjectProperty(None)
    def printMe(self):
        print(self.rootDisplay.text)
    
    plannerData = "PlannerData.tsks"

    today = date.today()

    # Notification vvvvv

    

    def remindMe(self, Message, rTime, _date):
        if str(_date) == str(date.today()):
            playsound.playsound('sound/Notif.mp3')
            #TRIGGER NOTIFICATION
            plyer.notification.notify(title=rTime, message=Message)
            return schedule.CancelJob

    def addReminder(self, Message, rTime, _date):
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
                schedule.every().day.at(theTime).do(self.remindMe, Message, rTime, date.today())
            else:
                schedule.every().day.at(theTime).do(self.remindMe, Message, rTime, _date)
        except:
            return

    def schedulerThread():
        while True:
            schedule.run_pending()
            time.sleep(1)

    t1 = threading.Thread(target=schedulerThread, name='t1', daemon=True)
    t1.start()

    # Notification ^^^^^

    def handleData(self, _today, process):
        global dataVar
        datafile = open(self.plannerData)

        data = datafile.read()

        datafile.close()
        result = subprocess.check_output(['JIT/luajit', '-l', 'main', '-e', f'{inspect.currentframe().f_code.co_name}("{data.encode()}","{_today}","{process}")'])

        if process == "init":
            if "~missingtoday" in str(result.decode("utf-8")):
                data = open(self.plannerData,"a")

                data.write(sub("~missingtoday",'',str(result.decode("utf-8"))))

                data.close()
            else:
                tupleData = make_tuple(str(result.decode("utf-8")))
                for i in range(0,len(tupleData)):
                    self.addReminder(tupleData[i][1], tupleData[i][0], date.today())
        else:
            dataVar = result.decode("utf-8")
            self.rootDisplay.text = dataVar
            

    def appendData(self, _date, time, task, process):
        datafile = open(self.plannerData)

        data = datafile.read()

        datafile.close()
        result = ""
        if _date == "":
            result = subprocess.check_output(['JIT/luajit', '-l', 'main', '-e', f'{inspect.currentframe().f_code.co_name}("{data.encode()}","{date.today()}","{time}","{task}","{process}")'])
        else:
            result = subprocess.check_output(['JIT/luajit', '-l', 'main', '-e', f'{inspect.currentframe().f_code.co_name}("{data.encode()}","{_date}","{time}","{task}","{process}")'])
        data = open(self.plannerData,"w")

        data.write(result.decode("utf-8"))

        data.close()

class PlannerApp(App):
    def build(self):
        PlannerScreen().handleData(date.today(),"init")
        return PlannerScreen()
PlannerApp().run()