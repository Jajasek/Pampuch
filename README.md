# Pampuch
This is one of many versions of the popular game Pacman, possibly the best. 
It was originally created by ZONER Software for Windows XP, this is the 
reimplementation for Windows 10; it should work basically on every platform
that supports pygame (see https://www.pygame.org/wiki/about).

## Instalation
* Install python 3.7.1 or newer (see https://www.python.org/downloads/)
* Install all the requirements listed in requirements.txt. These are:
    - pygame - the low-level GUI library that is used to handle graphics. 
      To install it, on most systems run `python3 -m pip install -U pygame --user`.
      For further information see
      https://www.pygame.org/wiki/GettingStarted#Pygame%20Installation.
    - pygame_widgets - the object-oriented abstraction on pygame. See the instruction 
      on https://github.com/Jajasek/pygame_widgets/blob/master/README.md.
    - Pillow - library used to process animated gifs. See the instruction on
      https://pillow.readthedocs.io/en/stable/installation.html.
    - MyLib - my personal library of useful bits of code. Download the content of the repository https://github.com/Jajasek/MyLib and save it to the folder `<your installation of python>/Lib/site-packages/MyLib`.
* Copy the entire content of this repository in a folder named `Pampuch` anywhere
  on your computer.
 
## Run
To run the game, run the file `main.py`. This can be done using command
```
python <your path to Pampuch>/Pampuch/main.py
```
On Windows you can double-click to the script `run.bat` instead.

There are some screenshots:

![Screenshot 0](https://github.com/Jajasek/Pampuch/blob/master/Screenshots/0.png)

![Screenshot 3](https://github.com/Jajasek/Pampuch/blob/master/Screenshots/3.png)

![Screenshot 4](https://github.com/Jajasek/Pampuch/blob/master/Screenshots/4.png)

![Screenshot 5](https://github.com/Jajasek/Pampuch/blob/master/Screenshots/5.png)

![Screenshot 6](https://github.com/Jajasek/Pampuch/blob/master/Screenshots/6.png)

Note: the `Options` button in main menu and pause menu works (probably) only on Windows. 
To change options on other systems, edit the file `constants.py`.

## Contact
In case the steps described in sections Install and Run fail, please contact me 
through github (https://github.com/Jajasek/Pampuch/issues) or mail
jachym.mierva@gmail.com.
