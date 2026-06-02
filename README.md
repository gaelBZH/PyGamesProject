# King of the Ocean in Python 💻
This repository was developed by Gaël KERNINON and Clément GOMEZ in 2026. It contains a project from the Course *Python Programming* during an Erasmus+ semester at *Cracow University of Technology* (**Poland**).
<img src="https://upload.wikimedia.org/wikipedia/en/thumb/1/12/Flag_of_Poland.svg/330px-Flag_of_Poland.svg.png" width="20px"></img>

## Languages 🌍
The main language of this repository is **Python**, utilizing the Pygame library to build a functional 2D arcade game.

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/250px-Python-logo-notext.svg.png" width="100px" style="padding: 5px 10px"></img>

## Architecture ⚙️
```text
KingOfTheOcean
├─── Game.py
├─── README.md
├─── Sea1.jpg
├─── Sea2.png
├─── Sea3.png
├─── Ship2.png
├─── SubmarineA.png
├─── Torpilla.png
├─── gameover.png
├─── music.mp3
└─── sonar.mp3
```

This repository contains a centralized Python script (`Game.py`) that executes the main game loop, as well as a collection of multimedia image and audio assets.  Clone this Repository 📦

## Clone this Repository 📦
⚠️ Prerequisites : `Python 3.x` and the `pygame` library must be installed on your system.  
```bash
pip install pygame
```

##### Windows 11 (Powershell)
```bash
python .\Game.py
```

##### Linux / macOS
```bash
python3 Game.py
```

## Controls 🎮
##### 🕹️ Navigation
- `Left / Right Arrow Keys`: Steer and move your ship horizontally across the surface.

##### ⚔️ Combat
- `Left Mouse Click`: Launch a torpedo from the left cannon of the ship.

- `Right Mouse Click`: Launch a torpedo from the right cannon of the ship.

##### ⚙️ Game Over Screen
- `P` Key: Restart the game loop to play again.

- `Q` Key: Safely exit and close the game application.