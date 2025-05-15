# 🧱 Pygame Tetris

A modern take on the classic Tetris game 
built with Python and Pygame. 
Includes a leaderboard, 
pause/resume functionality, 
restart button, and game logging.

## 📸 Screenshot


> ![Game Screenshot](resources/images/screenshot.png)

## 🎮 Features

- 7 types of falling blocks with rotation
- Line elimination and score system
- Game pause/resume (`P` key or button)
- Restart button after Game Over
- Game result logging with timestamp (`log.txt`)
- Leaderboard with top 5 scores (`scores.txt`)
- Preview of the next block

## 🧰 Technologies Used

- Python 3.12
- Pygame 2.6.1

## 🗂️ Project Structure
├── main.py # Main game loop and UI  
├── block.py # Block logic (movement, rotation, collision, stopping)
├── brick.py # Single unit brick drawing  
├── globals.py # Global constants and state  
├── scores.txt # Leaderboard data (auto-created)  
├── log.txt # Game history logs (auto-created)  
├── resources/  
│ ├── fonts/MONACO.TTF  
│ └── images/game_over.jpg  


## ⚙️ Installation & Running

1. 安装依赖：

```bash
pip install pygame
```

2. 运行游戏：

```bash
python main.py
```

##  🎮 Controls
| Key / Button     | Action                  |
| ---------------- | ----------------------- |
| ⬅ / ⬆ / ⬇ / ➡    | Move / Rotate / Drop    |
| P or Pause Btn   | Pause/Resume            |
| R or Restart Btn | Restart after Game Over |


##  📈 Leaderboard & Logging
👉 All scores are automatically recorded in scores.txt.  
👉 The top 5 highest scores are displayed on the Game Over screen.
👉 Each game result is logged with a timestamp in log.txt.

##  📄 License
This project is developed for educational purposes (COMP9001 Assignment). Not intended for commercial use.

##  👤 Author
Jiamu Cheng
University of Sydney
Course: COMP9001 Final Project
Email: [3386799661@qq.com]

##  ‼️ TIPS!!!!!
you must use English input method！！！！！