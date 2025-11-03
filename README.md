# 🎮 AI Chess Game

A fully-featured chess game built with Python and Pygame, featuring an unbeatable AI opponent powered by Stockfish engine. Play against a master-level chess AI with a professional, intuitive graphical interface.

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Pygame](https://img.shields.io/badge/Pygame-2.6+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

### 🎯 **Advanced AI Opponent**
- **Unbeatable Stockfish Engine** - Plays at maximum difficulty (Skill Level 20)
- **Deep Analysis** - Searches 20 moves ahead with 5 seconds thinking time
- **Optimized Performance** - Uses 512MB hash table and multi-threading
- **Master-Level Play** - Extremely challenging opponent for all skill levels

### 🎨 **Professional UI/UX**
- **Visual Move Indicators**
  - 🟡 Yellow highlight for selected pieces
  - 🟢 Green circles show valid move destinations
  - 🔴 Red rings highlight capture opportunities
- **Dynamic Board Orientation** - Your pieces always appear at the bottom
- **Move History Panel** - Track all moves in real-time
- **Status Bar** - Displays piece information on hover
- **Game Over Overlay** - Clear win/loss/draw announcements
- **"AI Thinking" Indicator** - Visual feedback during AI calculations

### ♟️ **Complete Chess Rules**
- Full legal move validation
- Automatic pawn promotion to Queen
- Checkmate and stalemate detection
- En passant, castling, and all special moves supported
- Standard chess notation (UCI format)

## 📋 Requirements

- Python 3.11 or higher
- Pygame 2.6.1 or higher
- python-chess library
- Stockfish chess engine executable

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/JeetInTech/AI-CHESS.git
cd AI-CHESS
```

### 2. Set Up Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Download Stockfish Engine
Download the Stockfish chess engine for your operating system:
- **Windows**: [Stockfish for Windows](https://stockfishchess.org/download/)
- **macOS**: [Stockfish for macOS](https://stockfishchess.org/download/)
- **Linux**: [Stockfish for Linux](https://stockfishchess.org/download/)

Place the `stockfish.exe` (or `stockfish` on Unix) in the project root directory.

## 🎮 How to Play

### Starting the Game
```bash
# Activate virtual environment first (if using)
venv\Scripts\activate

# Run the game
python chessai.py
```

### Gameplay Instructions

1. **Choose Your Side**
   - When prompted, type `white` or `black`
   - Your pieces will automatically appear at the bottom of the board

2. **Making Moves**
   - **Select a piece**: Click on any of your pieces
   - **View available moves**: Green circles appear on valid destination squares
   - **Capture pieces**: Red rings indicate enemy pieces you can capture
   - **Move the piece**: Click on a highlighted square to move
   - **Change selection**: Click on another piece to switch selection
   - **Deselect**: Click on an invalid square to deselect

3. **Special Features**
   - **Hover info**: Hover over your pieces to see their names
   - **AI thinking**: Watch the "AI thinking..." indicator during opponent's turn
   - **Move history**: Track all moves in the panel on the right
   - **Automatic promotion**: Pawns automatically promote to Queens

4. **Game Over**
   - The game displays a clear message when checkmate or draw occurs
   - Press any key or close the window to exit

## 🎯 Game Controls

| Action | Method |
|--------|--------|
| Select Piece | Left Click on your piece |
| Move Piece | Left Click on highlighted square |
| Change Selection | Left Click on another piece |
| Deselect | Left Click on invalid square |
| View Piece Info | Hover mouse over piece |
| Quit Game | Close window or press ESC |

## 📁 Project Structure

```
AI-CHESS/
│
├── chessai.py              # Main game file
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
├── .gitignore            # Git ignore rules
│
├── pieces/               # Chess piece images
│   ├── white-pawn.png
│   ├── white-knight.png
│   ├── white-bishop.png
│   ├── white-rook.png
│   ├── white-queen.png
│   ├── white-king.png
│   ├── black-pawn.png
│   ├── black-knight.png
│   ├── black-bishop.png
│   ├── black-rook.png
│   ├── black-queen.png
│   └── black-king.png
│
└── venv/                 # Virtual environment (not tracked)
```

## 🛠️ Technical Details

### Technologies Used
- **Python**: Core programming language
- **Pygame**: Graphics and game loop
- **python-chess**: Chess logic and move validation
- **Stockfish**: AI chess engine

### AI Configuration
```python
Skill Level: 20 (Maximum)
Search Depth: 20 moves
Thinking Time: 5000ms (5 seconds)
Hash Table: 512MB
Threads: 4
```

### Display Configuration
- **Window Size**: 1100 x 850 pixels
  - Chessboard: 800 x 800 pixels
  - Move History Panel: 300 x 850 pixels
  - Status Bar: 800 x 50 pixels
- **Square Size**: 100 x 100 pixels
- **Frame Rate**: 60 FPS

### Color Scheme
- **Light Squares**: Wheat (245, 222, 179)
- **Dark Squares**: Saddle Brown (139, 69, 19)
- **Selected Highlight**: Yellow with transparency
- **Valid Moves**: Green with transparency
- **Capture Moves**: Red with transparency

## 🎓 Tips for Playing

1. **Take Your Time**: The AI is very strong, so plan your moves carefully
2. **Watch for Tactics**: Pay attention to capture indicators (red rings)
3. **Control the Center**: Try to control the center squares early
4. **Protect Your King**: Always consider king safety
5. **Learn from Losses**: The AI plays optimal moves - study them!

## 🐛 Troubleshooting

### Game Won't Start
- Ensure `stockfish.exe` is in the project directory
- Check that all dependencies are installed: `pip install -r requirements.txt`
- Verify Python version: `python --version` (should be 3.11+)

### Board Not Displaying Correctly
- Make sure all piece images are in the `pieces/` folder
- Check that the `pieces/` directory contains all 12 PNG files

### AI Not Moving
- Verify Stockfish engine is properly installed and accessible
- Check terminal for error messages
- Ensure Stockfish has executable permissions (Unix systems)

### Performance Issues
- Close other resource-intensive applications
- Lower AI thinking time in code (change `movetime` parameter)
- Reduce search depth (change `depth` parameter)

## 🤝 Contributing

Contributions are welcome! Here are some ideas for improvements:

- [ ] Add difficulty level selection
- [ ] Implement save/load game functionality
- [ ] Add time controls (clock/timer)
- [ ] Create promotion piece selection UI
- [ ] Add sound effects
- [ ] Implement game analysis features
- [ ] Add multiplayer over network
- [ ] Create opening book integration

### How to Contribute
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see below for details:

```
MIT License

Copyright (c) 2025 JeetInTech

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 👨‍💻 Author

**JeetInTech**
- GitHub: [@JeetInTech](https://github.com/JeetInTech)
- Repository: [AI-CHESS](https://github.com/JeetInTech/AI-CHESS)

## 🙏 Acknowledgments

- **Stockfish Team** - For the incredible chess engine
- **python-chess Library** - For comprehensive chess logic
- **Pygame Community** - For the game development framework
- **Chess.com & Lichess** - For UI/UX inspiration

## 📚 Resources

- [Stockfish Official Website](https://stockfishchess.org/)
- [python-chess Documentation](https://python-chess.readthedocs.io/)
- [Pygame Documentation](https://www.pygame.org/docs/)
- [Chess Programming Wiki](https://www.chessprogramming.org/)

## 🔄 Version History

### v1.0.0 (Current)
- ✅ Initial release with full chess gameplay
- ✅ Maximum difficulty AI opponent
- ✅ Professional UI with move highlighting
- ✅ Dynamic board orientation
- ✅ Move history tracking
- ✅ Complete chess rules implementation

---

**Enjoy the game and good luck defeating the AI! ♟️**

*If you enjoyed this project, please consider giving it a ⭐ on GitHub!*
