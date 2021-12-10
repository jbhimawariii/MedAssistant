# i still need to add styles

import threading
import subprocess
import logging
import sys
import tkinter as tk
import pyglet
from tkinter import ttk

from google.assistant.library.event import EventType

# This is a deprecated library but Google doesn't even give us any other APIs.
from aiy.voice import tts
from aiy.assistant import auth_helpers
from aiy.board import Board
from aiy.leds import Color, Leds
from os import listdir
from os.path import isfile, join
from aiy.assistant.library import Assistant


# The class implementation could be somewhat better..
class medicalAssistant:
    def __init__(self):
        self._task = threading.Thread(target=self.runTask)
        self._medAssistant = None
        self._startConvo = False
        self._board = Board()
        self._board.button.when_pressed = self.buttonPressed
        self._led = Leds()

    def startAssistant(self):
        self._task.start()

    def getProfile(self, text):
        with open('index', 'r') as index:
            array = index.readlines()

            if len(text) < 11:
                tts.say("syntax error")
                return
            else:
                text = text[9:]
                tts.say("pulling profile for %s" % text)
                text = text.replace(" ", "")

            for x in array:
                if text in x:
                    profile = x
                else:
                    tts.say("""profile not in index, have you tried running \"refresh\"
                            or checking if the filename is correct?""")
                    return

            if profile.endswith(".pdf"):
                command = "zathura profiles/" + profile
                subprocess.run(command, shell=True)
            else:
                # just in case, always use pdf files
                command = "unoconv -f pdf profiles/" + profile
                subprocess.run(command, shell=True, capture_output=True)
                command = "zathura profiles/" + profile
                subprocess.run(command, shell=True)

    def refreshIndex(self):
        # gets a list of all files in a directory, then writes them into a file
        profiles = [f for f in listdir("profiles/") if isfile(join("profiles/", f))]
        with open('index', 'w') as file:
            for i in profiles:
                file.write(i + "\n")

        tts.say("refresh finished")

    def runTask(self):
        credentials = auth_helpers.get_assistant_credentials()  # get credentials, self explanatory
        with Assistant(credentials) as assistant:
            self._medAssistant = assistant
            for event in assistant.start():
                self.checkEvent(event)

    def buttonPressed(self):
        if self._startConvo:
            self._medAssistant.start_conversation()

    # There's some sort of part here that doesn't work on newer versions of the library, too bad!
    def checkEvent(self, event):
        logging.info(event)
        if event.type == EventType.ON_START_FINISHED:
            self._led.update(Leds.rgb_on(Color.BLACK))
            self._startConvo = True

        elif event.type == EventType.ON_CONVERSATION_TURN_STARTED:
            self._startConvo = False
            self._led.update(Leds.rgb_on(Color.GREEN))

        # process commands
        # Leds.rgb_on(Color.BLACK)) needs to be changed. I could use a better function.
        elif event.type == EventType.ON_RECOGNIZING_SPEECH_FINISHED and event.args:
            print("out: ", event.args['text'])
            text = event.args['text'].lower()
            self.checkCommand(text)

        elif (event.type == EventType.ON_CONVERSATION_TURN_FINISHED or
              event.type == EventType.ON_NO_RESPONSE or
              event.type == EventType.ON_CONVERSATION_TURN_TIMEOUT):
            self._led.update(Leds.rgb_on(Color.BLACK))
            self._startConvo = True

    # i dont like this part
    # can i use match cases
    def checkCommand(self, text):
        # TODO remove
        if text == "test":
            self._medAssistant.stop_conversation()
            self.helloWorld()

        elif "shutdown system" == text:
            self._medAssistant.stop_conversation()
            tts.say("Now Shutting Down")
            subprocess.run("sudo shutdown now", shell=True)

        elif "file get" in text:
            self.getProfile(text)

        elif text == "refresh":
            self._medAssistant.stop_conversation()
            self.refreshIndex()

        elif text == "goodbye":
            self._medAssistant.stop_conversation()
            self._led.update(Leds.rgb_off())
            tts.say("Goodbye")
            sys.exit(0)

    def textInput(self, input):
        if self._startConvo:
            self._medAssistant.send_text_query(input)


class medGui:
    def __init__(self):  # ABSOLUTE TRASH
        self._root = tk.Tk()
        self._root.title = "MedAssistant"
        self._root.geometry("400x450")
        self._root.resizable(False, False)
        self._root.configure(background="#141316")

        self._topFrame = ttk.Frame(self._root, padding="20 20 22 22", width=350, height=400)
        self._topFrame.pack()
        self._topFrame.pack_propagate(False)
        self._topFrame.place(relx=.5, rely=.5, anchor="center")

        pyglet.font.add_file("assets/Lato-Regular.ttf")
        self._icon = tk.PhotoImage(file="assets/githubicon.png")

        self._assistant = medicalAssistant()
        self._input = tk.StringVar()

    def openCredits(self):
        # TODO i would improve this function rn but its 1 am
        subprocess.run("chromium https://github.com/JairusBGit/MedAssistant")

    # bruh
    def addStyle(self):
        teststyle = ttk.Style()

        teststyle.configure("TFrame", background="#1b1c1f")
        teststyle.configure("TButton", font=("Lato", 18), borderwidth=0, background="#1b1c1f",
                            foreground="#c9c2bd", activeforeground="#ffffff",
                            activebackground="#1b1c1f")
        teststyle.configure("TSeparator", background="#ffffff")
        teststyle.configure("header.TLabel", font=("Lato", 24), background="#1b1c1f",
                            foreground="#c9c2bd")
        teststyle.configure("normal.TLabel", font=("Lato", 10), background="#1b1c1f",
                            foreground="#c9c2bd")
        teststyle.configure("TEntry", borderwidth=0, fieldbackground="#1b1c1f", foreground="#c9c2bd",
                            relief="flat", justify="center")

    # note to self, avoid writing gui programs
    def makeWidgets(self):
        ttk.Label(self._topFrame, text="MedAssistant", style="header.TLabel").pack(side=tk.TOP,
                                                                                   anchor=tk.NW)
        ttk.Separator(self._topFrame, orient=tk.VERTICAL).pack(side=tk.LEFT, fill="y",
                                                               padx=20)
        # AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        ttk.Button(self._topFrame, text="Activate", command=self._assistant.buttonPressed()).place(x=40, y=100)
        ttk.Button(self._topFrame, text="Refresh", command=self._assistant.refreshIndex()).place(x=40, y=200)

        input = ttk.Entry(self._topFrame, width=10, font=("Lato", 16))  # workaround
        input.place(x=60, y=300)
        input.delete(0, tk.END)
        input.insert(0, "Manual Input")
        input.focus()

        self._root.bind("<Return>",
                        lambda event, var=input:
                            self._assistant.textInput(var))

        ttk.Label(self._topFrame, text="Ver 0.9.1", style="normal.TLabel").place(x=240, y=360)

        ttk.Button(self._topFrame, image=self._icon, command=self.openCredits()).place(x=300, y=350)

    def start(self):
        self.addStyle()
        self.makeWidgets()
        self._root.mainloop()


def main():
    logging.basicConfig(level=logging.INFO)
    gui = medGui()
    gui.start()


if __name__ == "__main__":
    main()