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
SELECTED_COLOR = (255, 255, 0, 128)  # Yellow with transparency for selected piece
VALID_MOVE_COLOR = (0, 255, 0, 100)  # Green with transparency for valid moves
CAPTURE_MOVE_COLOR = (255, 0, 0, 128)  # Red with transparency for capture moves
BORDER_COLOR = (255, 255, 0)         # Yellow border for selected square

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

def get_stockfish_move(board, depth=20):
    """Get the best move from Stockfish for the current board position with maximum strength."""
    # Set Stockfish to maximum strength
    stockfish.stdin.write("setoption name Skill Level value 20\n")
    stockfish.stdin.write("setoption name Depth value 20\n")
    stockfish.stdin.write("setoption name Threads value 4\n")
    stockfish.stdin.write("setoption name Hash value 512\n")  # 512MB hash table
    stockfish.stdin.flush()
    
    stockfish.stdin.write(f"position fen {board.fen()}\n")
    stockfish.stdin.write(f"go depth {depth} movetime 5000\n")  # 5 seconds thinking time
    stockfish.stdin.flush()
    
    while True:
        line = stockfish.stdout.readline().strip()
        if "bestmove" in line:
            parts = line.split()
            if parts[1] == "(none)":
                return None  # No legal moves (checkmate or stalemate)
            best_move = parts[1]  # Extract the move (e.g., "e2e4")
            return chess.Move.from_uci(best_move)

def draw_board(board, human_color, selected_square=None, valid_moves=None):
    """Draw the chessboard, pieces, highlights, and status bar."""
    # Draw squares
    for row in range(8):
        for col in range(8):
            # Calculate display coordinates based on human color
            # If human is WHITE, show board normally (rank 0 at bottom)
            # If human is BLACK, flip the board (rank 7 at bottom)
            display_row = 7 - row if human_color == chess.WHITE else row
            display_col = col
            
            # Square color
            color = LIGHT_BROWN if (row + col) % 2 == 0 else DARK_BROWN
            pygame.draw.rect(screen, color, (display_col * SQUARE_SIZE, display_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            
            # Calculate actual square number
            actual_square = chess.square(col, row)
            
            # Highlight selected square
            if selected_square is not None and actual_square == selected_square:
                # Draw yellow border for selected square
                pygame.draw.rect(screen, BORDER_COLOR, 
                               (display_col * SQUARE_SIZE, display_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 4)
                # Draw semi-transparent yellow overlay
                highlight_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                highlight_surface.fill(SELECTED_COLOR)
                screen.blit(highlight_surface, (display_col * SQUARE_SIZE, display_row * SQUARE_SIZE))
            
            # Highlight valid moves
            if valid_moves and actual_square in [move.to_square for move in valid_moves]:
                highlight_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                # Check if it's a capture move
                is_capture = any(board.piece_at(move.to_square) is not None for move in valid_moves if move.to_square == actual_square)
                move_color = CAPTURE_MOVE_COLOR if is_capture else VALID_MOVE_COLOR
                highlight_surface.fill(move_color)
                screen.blit(highlight_surface, (display_col * SQUARE_SIZE, display_row * SQUARE_SIZE))
                
                # Draw a circle in the center for empty squares, ring for captures
                center_x = display_col * SQUARE_SIZE + SQUARE_SIZE // 2
                center_y = display_row * SQUARE_SIZE + SQUARE_SIZE // 2
                if is_capture:
                    pygame.draw.circle(screen, (255, 0, 0), (center_x, center_y), SQUARE_SIZE // 3, 3)
                else:
                    pygame.draw.circle(screen, (0, 255, 0), (center_x, center_y), SQUARE_SIZE // 6)
    
    # Draw pieces
    for square, piece in board.piece_map().items():
        row, col = divmod(square, 8)
        # Calculate display coordinates based on human color
        # If human is WHITE, show board normally (rank 0 at bottom)
        # If human is BLACK, flip the board (rank 7 at bottom)
        display_row = 7 - row if human_color == chess.WHITE else row
        display_col = col
        
        piece_symbol = piece.symbol().upper()  # e.g. 'r' -> 'R'
        filename = f"{'white' if piece.color else 'black'}-{piece_filename_map[piece_symbol]}.png"
        screen.blit(piece_images[filename], (display_col * SQUARE_SIZE, display_row * SQUARE_SIZE))

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

def get_square_from_mouse(pos, human_color):
    """Only process clicks in the chessboard area (left 800px) and convert to proper square based on orientation."""
    x, y = pos
    if x > CHESSBOARD_WIDTH:  # Ignore clicks in the move history panel
        return None
    col = x // SQUARE_SIZE
    row = y // SQUARE_SIZE
    if 0 <= col < 8 and 0 <= row < 8:
        # Convert display coordinates to actual board coordinates
        # If human is WHITE, board is shown normally (rank 0 at bottom, so flip the row)
        # If human is BLACK, board is flipped (rank 7 at bottom, so use row as is)
        actual_row = 7 - row if human_color == chess.WHITE else row
        return chess.square(col, actual_row)
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

    print(f"You are playing as {'White' if human_color == chess.WHITE else 'Black'}")
    print("Your pieces are at the bottom of the board.")
    print("AI is set to maximum difficulty - Good luck!")

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
                square = get_square_from_mouse(pos, human_color)
                if square is None:
                    continue

                if selected_square is None:
                    # Select a piece if it belongs to the human player
                    if square in board.piece_map() and board.piece_at(square).color == human_color:
                        selected_square = square
                        valid_moves = [move for move in board.legal_moves if move.from_square == selected_square]
                        piece = board.piece_at(selected_square)
                        piece_name = get_piece_name(piece)
                else:
                    # Check if clicking on another piece of the same color (reselect)
                    if (square in board.piece_map() and 
                        board.piece_at(square).color == human_color and 
                        square != selected_square):
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
                            # Handle pawn promotion - give options
                            if (board.piece_at(move.from_square).piece_type == chess.PAWN and 
                                (chess.square_rank(move.to_square) == 7 or chess.square_rank(move.to_square) == 0)):
                                # For now, auto-promote to Queen (can be enhanced later with a UI choice)
                                move = chess.Move(move.from_square, move.to_square, promotion=chess.QUEEN)
                            
                            board.push(move)
                            move_history.append(f"Human: {move.uci()}")
                            selected_square = None
                            valid_moves = []
                            piece_name = ""
                            # Update display immediately
                            screen.fill(BLACK)
                            draw_board(board, human_color, selected_square, valid_moves)
                            draw_move_history(move_history)
                            pygame.display.flip()
                            time.sleep(0.3)  # Show human's move before AI responds
                        else:
                            # Deselect if clicking on invalid square
                            selected_square = None
                            valid_moves = []
                            piece_name = ""

            # Update piece name on hover when not selecting a move
            if selected_square is None and (board.turn == (human_color == chess.WHITE)):
                pos = pygame.mouse.get_pos()
                square = get_square_from_mouse(pos, human_color)
                if square is not None and square in board.piece_map():
                    piece = board.piece_at(square)
                    if piece.color == human_color:  # Only show name for player's pieces
                        piece_name = get_piece_name(piece)
                    else:
                        piece_name = ""
                else:
                    piece_name = ""

        # AI's turn - show thinking message
        if not board.is_game_over() and (board.turn == (ai_color == chess.WHITE)):
            # Show "AI thinking..." message
            thinking_font = pygame.font.Font(None, 48)
            thinking_surface = thinking_font.render("AI thinking...", True, WHITE)
            thinking_rect = thinking_surface.get_rect(center=(CHESSBOARD_WIDTH // 2, WINDOW_HEIGHT // 2))
            
            # Draw semi-transparent overlay
            overlay = pygame.Surface((CHESSBOARD_WIDTH, WINDOW_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            screen.blit(overlay, (0, 0))
            screen.blit(thinking_surface, thinking_rect)
            pygame.display.flip()
            
            ai_move = get_stockfish_move(board)
            if ai_move is not None:
                board.push(ai_move)
                move_history.append(f"AI: {ai_move.uci()}")
                piece_name = ""

        # Draw the board
        screen.fill(BLACK)
        draw_board(board, human_color, selected_square, valid_moves)
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
                    print("White wins (AI won!)")
            elif result == "0-1":
                if human_color == chess.BLACK:
                    print("Black wins (You won!)")
                else:
                    print("Black wins (AI won!)")
            else:
                print("Draw!")
            
            # Show game over message on screen
            game_over_font = pygame.font.Font(None, 72)
            if result == "1/2-1/2":
                game_over_text = "DRAW!"
            elif (result == "1-0" and human_color == chess.WHITE) or (result == "0-1" and human_color == chess.BLACK):
                game_over_text = "YOU WIN!"
            else:
                game_over_text = "AI WINS!"
            
            game_over_surface = game_over_font.render(game_over_text, True, WHITE)
            game_over_rect = game_over_surface.get_rect(center=(CHESSBOARD_WIDTH // 2, WINDOW_HEIGHT // 2))
            
            # Draw semi-transparent overlay
            overlay = pygame.Surface((CHESSBOARD_WIDTH + MOVE_HISTORY_WIDTH, WINDOW_HEIGHT))
            overlay.set_alpha(200)
            overlay.fill(BLACK)
            screen.blit(overlay, (0, 0))
            screen.blit(game_over_surface, game_over_rect)
            pygame.display.flip()
            
            # Wait for user to close or press a key
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        waiting = False
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        waiting = False
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