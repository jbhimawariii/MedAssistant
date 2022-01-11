# MedAssistant
The scripts used for Jairus' Group research Project.

Version 0.9.4 Marisa (GUI Build)

## Purpose
This program was made for the research title "Raspberry Pi based Virtual Assistant in Helping Doctors in Pulling Patient Profiles" at Pedro Guevara Memorial National Highschool in the section 9-J.BANZON Year 2021-2022.

## Things To Do
- Fix Bugs
- Change commands to ones that work for the enclosure setup of the Raspberry Pi
- Recode the Google Assistant Library for Python and make an API for Python 3.10

## Credits

[**Kalinaw Lukas Aom Conde-Bebis / krlm0**](https://github.com/krlm0)
 - Lead Programmer
 - Co-Manager

[**Jairus Azarael C. Bona / JairusBGit**](https://github.com/JairusBGit)
 - Co-Programmer
 - Lead Debugger
 - Co-Documentor
 - Tester

**Noel Nasalig Sabio II**
 - Documentor
 - Tester

## Hardware
This program runs on a modified build of the Google AIY Voice Kit V2.

- The included Raspberry Pi Zero B was replaced with Raspberry Pi 3B.

## Open Source Programs Used
- [Python 3.7](https://www.python.org/)
- [Zathura](https://github.com/pwmt/zathura)
- [LibreOffice](https://github.com/LibreOffice)
- [Unoconv](https://github.com/unoconv/unoconv)
- [Google Assistant Library API for Python](https://github.com/googlesamples/assistant-sdk-python)  note that google-assistant-library requires the 1.0.0 version

This program runs on the Raspbian OS based on Debian Linux

## Installation
Step 1: Clone this repo running `git clone https://github.com/JairusBGit/MedAssistant.git && cd MedAssistant` in a terminal.

Step 2: Install the [AIY Voice Kit](https://github.com/google/aiyprojects-raspbian/releases) Debian package.

Step 3: Authorize your kit by following instructions [here](https://aiyprojects.withgoogle.com/voice/#assembly-guide).
  * Note: The OAuth credentials may expire so if you encounter that bug, run `rm -rf ~/.cache/voice-recognizer` and then re-run the authorization steps.

Step 4: Install the dependencies with `sudo apt-get install python3.7 zathura zathura-pdf-poppler libreoffice unoconv && pip install google-assistant-library==1.0.0`.

Step 5: Install your documentations in the profiles directory with the patient name as the filename.
  * Note: Adding new patient profiles requires the use of the voice command `OK Google, "Refresh"`
  * Extra Note: You could also add patient profiles via interacting with the GUI once running the script. By clicking the "+" button you are prompted to open the file of the patient's profile and input the patient's name, there is no need to "refresh" with this method.

Step 6: Run the script and enjoy, activate it by pressing the button or saying "OK Google" or by use of the GUI.
  * Note: This program only properly runs on Python 3.7 with ***VERSION 1.0 OF THE GOOGLE ASSISTANT API***

## License
This Program is licensed under the [Apache v2 License](http://www.apache.org/licenses).
