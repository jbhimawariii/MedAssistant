# a test of sanity
import threading
import subprocess
import logging

from google.assistant.library.event import EventType

# This is a deprecated library but Google doesn't even give us any other APIs.
from aiy.voice import tts
from aiy.assistant import auth_helpers
from aiy.board import Board
from aiy.leds import Color, Leds
from os import listdir
from os.path import isfile, join
from aiy.assistant.library import Assistant


# The class implementation could be better. But this isnt being sold so i dont care.
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
                    tts.say("profile not in index, have you tried running \"refresh\" or checking if the filename is correct?")
                    return

            if profile.endswith('.pdf'):
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

# STOP MAKING SO MANY ASSISTANT AUTH CALLS PLEASSSEEEE
    def runTask(self):
        credentials = auth_helpers.get_assistant_credentials()  # get credentials, self explanatory
        with Assistant(credentials) as assistant:
            self._medAssistant = assistant
            for event in assistant.start():
                self.checkEvent(event)

# implement a "button press = shut up" feature pls
    def buttonPressed(self):
        if self._startConvo:
            self._medAssistant.start_conversation()

    def checkEvent(self, event):
        logging.info(event)
        if event.type == EventType.ON_START_FINISHED:
            self._led.update(Leds.rgb_on(Color.BLACK))
            self._startConvo = True

        elif event.type == EventType.ON_CONVERSATION_TURN_STARTED:
            self._startConvo = False
            self._led.update(Leds.rgb_on(Color.GREEN))

        # process commands
        # need to fix this
        # "Leds.rgb_on(Color.BLACK)) needs to be changed. I could use a better function.
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
    # we need to clean this code
    # IS THERE ANY WAY WE CAN USE SOMETHING CLEANER THAN AN ELIF???
    #
    # remind me to remove the helloWorld functions in the final release
    def checkCommand(self, text):
        if text == "test":
            self._medAssistant.stop_conversation()
            self.helloWorld()

        # remind me to remove this in the final release
        elif "system details" in text:
            self._medAssistant.stop_conversation()
            subprocess.run("neofetch", shell=True)

        elif "shutdown system" == text:
            self._medAssistant.stop_conversation()
            tts.say("Now Shutting Down")
            subprocess.run("sudo shutdown now", shell=True)

        elif "file get" in text:
            self._medAssistant.stop_conversation()
            self.getProfile(text)

        # we need to implement this into the GUI
        elif text == "refresh":
            self._medAssistant.stop_conversation()
            self.refreshIndex()

        # need to fix the exit() function since it doesn't really exit the script.
        elif text == "goodbye":
            self._medAssistant.stop_conversation()
            self._led.update(Leds.rgb_off())
            tts.say("Goodbye")
            exit()


def main():
    logging.basicConfig(level=logging.INFO)
    assist = medicalAssistant()
    assist.startAssistant()


if __name__ == "__main__":
    main()
