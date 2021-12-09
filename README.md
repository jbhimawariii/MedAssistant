# MedAssistant
The Scripts used for Jairus' Group Research Project.

Version 0.5.1 beta
Codename: PC-98 Reimu

## Purpose
This program was made for the research title "Raspberry Pi based Virtual Assistant in Helping Doctors in Pulling Patient Profiles" at Pedro Guevara Memorial National Highschool in the section 9-J.BANZON Year 2021-2022

## Things To Do
- Program a GUI
- Profile Entry template
- Fix Bugs
- Automation Functions
- Proper LED Implementation
- Fix the 500 API call limit

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

- The included Raspberry Pi Zero B was replaced with Raspberry Pi 3B

## Open Source Programs Used
- [Python 3.7](https://www.python.org/)
- [Zathura](https://github.com/pwmt/zathura)
- [LibreOffice](https://github.com/LibreOffice)
- [Unoconv](https://github.com/unoconv/unoconv)
- [Neofetch](https://github.com/dylanaraps/neofetch)
- [Google Assistant Library API for Python](https://github.com/googlesamples/assistant-sdk-python)

This program was made in [NeoVim](https://github.com/neovim/neovim)

This program runs on the Raspbian OS based on Debian Linux

## Installation
Step 1: Install the [AIY Voice Kit](https://github.com/google/aiyprojects-raspbian/releases) Debian package
Step 2: Authorize your kit by following instructions [here](https://aiyprojects.withgoogle.com/voice/#assembly-guide)
  * Note: The OAuth credentials may expire so if you encounter that bug, run `rm -rf ~/.cache/voice-recognizer` and then re-run the authorization steps.
Step 3: Install the dependencies with `sudo apt-get install python3 zathura libreoffice unoconv`
Step 4: Install your documentations in the profiles directory with the patient name as the filename.
  * Note: Adding new patient profiles requires the use of the voice command `OK Google, "Refresh"`
Step 5: Run the Python script and enjoy.

## License
This Program is licensed under the [Apache v2 License](http://www.apache.org/licenses)
