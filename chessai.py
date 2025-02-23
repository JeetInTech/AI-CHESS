import pygame
import chess
import subprocess
import time

# Initialize Pygame
pygame.init()


# Window dimensions (chessboard + move history)
CHESSBOARD_WIDTH = 800
MOVE_HISTORY_WIDTH = 300
WINDOW_HEIGHT = 850
screen = pygame.display.set_mode((CHESSBOARD_WIDTH + MOVE_HISTORY_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Chess: Human vs AI ")

# Colors
LIGHT_BROWN = (245, 222, 179)  # Light square color
DARK_BROWN = (139, 69, 19)     # Dark square color
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)         # For status bar background

# Chessboard setup
SQUARE_SIZE =  CHESSBOARD_WIDTH // 8
piece_images = {}
piece_types = ['pawn', 'knight', 'bishop', 'rook', 'queen', 'king']  # Match your filenames

# Map chess symbols to your image filenames (e.g., 'P' -> 'pawn')
piece_filename_map = {
    'P': 'pawn', 'p': 'pawn',
    'N': 'knight', 'n': 'knight',
    'B': 'bishop', 'b': 'bishop',
    'R': 'rook',  'r': 'rook',
    'Q': 'queen', 'q': 'queen',
    'K': 'king',  'k': 'king'
}

# Map chess symbols to custom names (e.g., 1 -> 'Pawn')
piece_names = {
    1: 'Pawn',
    2: 'Knight',
    3: 'Bishop',
    4: 'Rook',
    5: 'Queen',
    6: 'King'
}

# Load piece images (matching your filenames like white-pawn.png, black-knight.png)
for color in ['white', 'black']:  # Match your filenames
    for piece in piece_types:
        piece_images[f"{color}-{piece}.png"] = pygame.transform.scale(
            pygame.image.load(f'pieces/{color}-{piece}.png'), (SQUARE_SIZE, SQUARE_SIZE)
        )

# Initialize Stockfish engine (Windows version; use filename since it's in the same directory)
stockfish = subprocess.Popen('stockfish.exe',
                            stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, bufsize=1)

# Initialize Stockfish UCI mode
stockfish.stdin.write("uci\n")
stockfish.stdin.flush()
while True:
    line = stockfish.stdout.readline().strip()
    if line == "uciok":
        break

def get_stockfish_move(board, depth=15):
    """Get the best move from Stockfish for the current board position."""
    stockfish.stdin.write(f"position fen {board.fen()}\n")
    stockfish.stdin.write(f"go depth {depth}\n")
    stockfish.stdin.flush()
    
    while True:
        line = stockfish.stdout.readline().strip()
        if "bestmove" in line:
            parts = line.split()
            if parts[1] == "(none)":
                return None  # No legal moves (checkmate or stalemate)
            best_move = parts[1]  # Extract the move (e.g., "e2e4")
            return chess.Move.from_uci(best_move)

def draw_board(board):
    """Draw the chessboard, pieces, and status bar."""
    for row in range(8):
        for col in range(8):
            color = LIGHT_BROWN if (row + col) % 2 == 0 else DARK_BROWN
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    
    # Draw pieces
    for square, piece in board.piece_map().items():
        row, col = divmod(square, 8)
        piece_symbol = piece.symbol().upper()  # e.g. 'r' -> 'R'
        filename = f"{'white' if piece.color else 'black'}-{piece_filename_map[piece_symbol]}.png"
        screen.blit(piece_images[filename], (col * SQUARE_SIZE, row * SQUARE_SIZE))

    # Draw status bar (for piece name)
    pygame.draw.rect(screen, GRAY, (0, 800, CHESSBOARD_WIDTH, 50))
    font = pygame.font.Font(None, 36)
    status_text = font.render(piece_name, True, WHITE)
    screen.blit(status_text, (10, 810))

def draw_move_history(move_history):
    """Draw move history on the right panel of the window."""
    # Clear the move history area
    pygame.draw.rect(screen, BLACK, (CHESSBOARD_WIDTH, 0, MOVE_HISTORY_WIDTH, WINDOW_HEIGHT))
    
    font = pygame.font.Font(None, 24)
    y_offset = 10
    for i, move in enumerate(move_history):
        text = f"{i + 1}. {move}"
        move_text = font.render(text, True, WHITE)
        screen.blit(move_text, (CHESSBOARD_WIDTH + 10, y_offset))
        y_offset += 30

def get_square_from_mouse(pos):
    """Only process clicks in the chessboard area (left 800px)."""
    x, y = pos
    if x > CHESSBOARD_WIDTH:  # Ignore clicks in the move history panel
        return None
    col = x // SQUARE_SIZE
    row = y // SQUARE_SIZE
    if 0 <= col < 8 and 0 <= row < 8:
        return chess.square(col, row)
    return None

def get_piece_name(piece):
    """Convert a chess piece to the custom name format (e.g., 'White-Knight')."""
    if piece is None:
        return ""
    color = "White" if piece.color else "Black"
    piece_type = piece_names[piece.piece_type]
    return f"{color}-{piece_type}"

def main():
    # Ask player to choose their side
    while True:
        side = input("Choose your side: White or Black (default White if invalid): ").lower().strip()
        if side in ['white', 'black']:
            break
        print("Invalid input. Defaulting to White.")
        side = 'white'

    human_color = chess.WHITE if side == 'white' else chess.BLACK
    ai_color = chess.BLACK if side == 'white' else chess.WHITE

    board = chess.Board()
    clock = pygame.time.Clock()
    selected_square = None
    valid_moves = []
    global piece_name
    piece_name = ""
    move_history = []

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and (board.turn == (human_color == chess.WHITE)):
                # Only human moves when it's their turn
                pos = pygame.mouse.get_pos()
                square = get_square_from_mouse(pos)
                if square is None:
                    continue

                if selected_square is None:
                    if square in board.piece_map() and board.piece_at(square).color == human_color:
                        selected_square = square
                        valid_moves = [move for move in board.legal_moves if move.from_square == selected_square]
                        piece = board.piece_at(selected_square)
                        piece_name = get_piece_name(piece)
                else:
                    # Check if the clicked square is a valid move
                    move = None
                    for m in valid_moves:
                        if m.to_square == square:
                            move = m
                            break
                    if move is not None:
                        # Handle pawn promotion automatically to queen
                        if board.piece_at(move.from_square).piece_type == chess.PAWN and (
                            chess.square_rank(move.to_square) == 7 or chess.square_rank(move.to_square) == 0
                        ):
                            move = chess.Move(move.from_square, move.to_square, promotion=chess.QUEEN)
                        board.push(move)
                        move_history.append(f"Human: {move.uci()}")
                        selected_square = None
                        valid_moves = []
                        piece_name = ""
                        # Update display immediately
                        screen.fill(BLACK)
                        draw_board(board)
                        draw_move_history(move_history)
                        pygame.display.flip()
                        time.sleep(0.3)  # Show human's move before AI responds

            # Update piece name on hover
            if selected_square is None and (board.turn == (human_color == chess.WHITE)):
                pos = pygame.mouse.get_pos()
                square = get_square_from_mouse(pos)
                if square is not None and square in board.piece_map():
                    piece = board.piece_at(square)
                    piece_name = get_piece_name(piece)
                else:
                    piece_name = ""

        # AI's turn
        if not board.is_game_over() and (board.turn == (ai_color == chess.WHITE)):
            ai_move = get_stockfish_move(board)
            if ai_move is not None:
                board.push(ai_move)
                move_history.append(f"AI: {ai_move.uci()}")
                time.sleep(0.5)  # Delay for AI move visibility
                piece_name = ""
                draw_move_history(move_history)
                pygame.display.flip()

        # Draw the board
        screen.fill(BLACK)
        draw_board(board)
        draw_move_history(move_history)
        pygame.display.flip()
        clock.tick(60)

        # Check game over
        if board.is_game_over():
            result = board.result()
            print(f"Game Over! Result: {result}")
            if result == "1-0":
                if human_color == chess.WHITE:
                    print("White wins (You won!)")
                else:
                    print("Black wins (AI won!)")
            elif result == "0-1":
                if human_color == chess.BLACK:
                    print("Black wins (You won!)")
                else:
                    print("White wins (AI won!)")
            else:
                print("Draw!")
            running = False

    pygame.quit()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Game interrupted by user.")
    finally:
        try:
            stockfish.stdin.write("quit\n")
            stockfish.stdin.flush()
            stockfish.terminate()
        except OSError:
            pass  # Ignore if the process is already terminated