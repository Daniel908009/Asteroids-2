# Asteroids-2

## What is it?

This project is a classic *Asteroids* style game written in Python using Pygame.  
It recreates the core mechanics of the original arcade game while adding several new features, such as a player shield and configurable settings for fullscreen mode, invincibility, and more.

## Why did I do it?

Those paying attention probably noticed that this repository is called Asteroids-**2**. This is because I already have an older project repository named *Asteroids*.

I originally made an Asteroids style game about two years ago, and while it worked, it does not represent my current skill level. Compared to my more recent work, the original version looks, plays, and is structured quite poorly, not just in terms of visuals and gameplay, but also in code quality.

The first version was a single file Python project with only a few classes, making it difficult to maintain or extend. This project is a complete rewrite, built with a class structure and cleaner architecture, and is meant to serve as a more accurate and presentable showcase of my Python and Pygame skills.

## How to play

Simply start the game and try to destroy as many asteroids and UFOs as possible.  
When the game ends, you will be prompted to enter your name so your score can be saved and later viewed in the High Scores menu.

### Game controls

- **W, D** for up and down in the menu
- **Enter, Space** for selecting in the menu
- **Backspace** return
- **Escape** Close game<br/>
The rest of the controls are in the game itself (Manual in the main menu)

## Features

- All core mechanics from the original *Asteroids*, including a controllable spaceship, asteroids, and UFOs
- Rechargeable player shield
- Main menu system
- Extensive in-game settings (fullscreen, invincibility, spawn rates, and more)

## Screenshots
### !Important: Each screenshot has a description below it so you can understand what you are seeing.
<img width="2256" height="1504" alt="Main menu" src="https://github.com/user-attachments/assets/3a5f21dc-0a6c-4454-872e-c6191c5791a1" /> <br/>
This is the main menu.

<img width="2256" height="1504" alt="image" src="https://github.com/user-attachments/assets/3c1d2872-d37e-4b5a-b493-85e6a310c16b" /> <br/>
This is the actual game.

<img width="2256" height="1504" alt="image" src="https://github.com/user-attachments/assets/a4f6f3b4-434f-44c3-9935-dce286378ebc" /> <br/>
This is how the settings are displayed.

<img width="2256" height="1504" alt="image" src="https://github.com/user-attachments/assets/6c3bd52b-b27b-4161-bf65-2521b3597b40" /> <br/>
This is how changing of value in the settings looks.

## How to download and run locally
(Python 3.10+ recommended)
1. From source code
Steps:
   1. Download this repository as a .zip file
   2. Put it in the folder where you want your game to be and extract it
   3. Install Python if you dont have it
   4. Open a command prompt and run these two commands
   ```bash
   pip install -r requirements.txt
   python3 main.py
   ```
2. Using .exe file
   1. Simply download the .exe file from the latest release. It should be on the right side of the repository webpage
   2. Run the executable
