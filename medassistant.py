# i still need to add styles

import threading
import subprocess
import logging
import sys
import tkinter as tk
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
        def checkCommand(text):
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


# half-baked gui, god i hope it works
class medGui:
    def __init__(self):  # uhhhhhhhhhh
        self._root = tk.Tk()
        self._root.title = "Medical Assistant"
        self._topFrame = ttk.Frame(self._root, padding="10, 10, 12, 12")
        self._assistant = medicalAssistant()
        self._input = tk.StringVar()

    def makeWidgets(self):
        # i don't really have a need for this function except cleanliness
        heading_font = ("Arial", 20)
        ttk.Label(self._topFrame, text="Medical Assistant").grid(column=1, row=1, sticky=(tk.W, tk.E))
        ttk.Button(self._topFrame, text="Activate", command=self._assistant.buttonPressed()).grid(column=1, row=2, sticky=(tk.W))
        ttk.Button(self._topFrame, text="Refresh", command=self._assistant.refreshIndex()).grid(column=1, row=3, sticky=(tk.W))

        input = ttk.Entry(self._topFrame, width=10).grid(column=1, row=4, sticky=(tk.W))
        input.focus()
        self._root.bind("<Return>",
                        lambda event, var=input:
                            self._assistant.textInput(var))

    def start(self):
        self.makeWidgets()
        self._assistant.startAssistant()
        self._root.mainloop()


def main():
    logging.basicConfig(level=logging.INFO)
    gui = medGui()
    gui.start()


if __name__ == "__main__":
    main()
