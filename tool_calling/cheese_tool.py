import chess
import chess.polyglot
import random
import os, requests, shutil
import lmstudio as lms

# Modeli yükle
model = lms.llm("ibm-granite/granite-3.3-8b-instruct-GGUF")

# Satranç tahtası
board = chess.Board()
ai_pos = 0

# Açılış kitabı indir
RAW_URL   = ("https://raw.githubusercontent.com/"
             "niklasf/python-chess/master/data/polyglot/performance.bin")
DEST_FILE = "performance.bin"

if not os.path.exists(DEST_FILE):
    print("Downloading performance.bin …")
    try:
        with requests.get(RAW_URL, stream=True, timeout=15) as r:
            r.raise_for_status()
            with open(DEST_FILE, "wb") as out:
                shutil.copyfileobj(r.raw, out, 1 << 16) 
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Download failed: {e}")

# --- Yardımcı Fonksiyonlar ---

def legal_moves() -> list[str]:
    return [board.san(move) for move in board.legal_moves]

def possible_captures()-> list[dict]:
    result = []
    for move in board.generate_legal_captures():
        piece = board.piece_at(move.to_square)
        piece_type = piece.symbol().upper() if piece else "?"
        defenders = board.attackers(not board.turn, move.to_square)
        is_hanging = len(defenders) == 0
        result.append({
            "san": board.san(move),
            "captured_piece": piece_type,
            "is_hanging": is_hanging    
        })
    return result

def possible_checks() -> list[dict]:
    result = []
    for move in board.legal_moves:
        if not board.gives_check(move):
            continue
        temp = board.copy()
        temp.push(move)
        can_capture = any(
            temp.is_capture(reply) and reply.to_square == move.to_square
            for reply in temp.legal_moves
        )
        king_sq = temp.king(not board.turn)
        can_escape = any(
            reply.from_square == king_sq for reply in temp.legal_moves
        )
        can_block = any(
            not temp.is_capture(reply)
            and reply.from_square != king_sq
            and not temp.gives_check(reply)
            for reply in temp.legal_moves
        )
        result.append({
            "san": board.san(move),
            "can_be_captured": can_capture,
            "can_be_blocked": can_block,
            "can_escape_by_moving_king": can_escape
        })
    return result

def get_move_history() -> list[str]:
    return [board.san(move) for move in board.move_stack]

def get_book_moves() -> list[str]:
    moves = []
    with chess.polyglot.open_reader("performance.bin") as reader:
        for entry in reader.find_all(board):
            moves.append(board.san(entry.move))
    return moves

def is_ai_turn() -> bool:
    return bool(board.turn) == (ai_pos == 0)

def make_ai_move(move: str) -> None:
    if is_ai_turn():
        try:
            board.push_san(move)
        except ValueError as e:
            raise ValueError(e)
    else:
        raise ValueError("Not AI's turn.")

def make_user_move(move: str) -> None:
    if not is_ai_turn():
        try:
            board.push_san(move)
        except ValueError as e:
            raise ValueError(e)
    else:
        raise ValueError("Not player's turn.")

# Tahta çıktısı: ASCII (terminalde)
def update_board(move=0):
    os.system("cls" if os.name == "nt" else "clear")  # ekran temizle
    print(f"\nBoard after move {move+1}")
    print(board)  # ASCII çıktısı
    print("\nMoves so far:", get_move_history())

# İsteğe bağlı: SVG çıktısını dosyaya kaydet
def save_board_svg(filename="board.svg"):
    import chess.svg
    with open(filename, "w") as f:
        f.write(chess.svg.board(board, size=400))
    print(f"Tahta {filename} dosyasına kaydedildi.")

def get_end_state():
    if board.is_checkmate():
        return "Checkmate!"
    elif board.is_stalemate():
        return "Stalemate!"
    elif board.is_insufficient_material():
        return "Draw by insufficient material!"
    elif board.is_seventyfive_moves():
        return "Draw by 75-move rule!"
    elif board.is_fivefold_repetition():
        return "Draw by fivefold repetition!"
    else:
        return None

# --- LLM rolleri ---
chat_white = lms.Chat("""You are a chess AI, playing for white...""")
chat_black = lms.Chat("""You are a chess AI, playing for black...""")

# Başlangıç
board.reset()
ai_pos = round(random.random())  # 0 = beyaz, 1 = siyah
move = 0
update_board(move)

# --- Oyun Döngüsü ---
userEndGame = False
while True:
    if ai_pos == 0:
        # AI Beyaz
        model.act(
            chat_white,
            [get_move_history, legal_moves, possible_captures, possible_checks, get_book_moves, make_ai_move],
            on_message=print,
            max_prediction_rounds=8,
        )
        if is_ai_turn():
            make_ai_move(legal_moves()[0])  # failsafe
        update_board(move); move += 1
        if (msg := get_end_state()): print(msg); break

        # Kullanıcı Siyah
        while True:
            user_move = input("\nUser (Black): hamleni gir ('help' ya da 'quit'): ")
            if user_move.lower() == 'quit':
                print("Game ended by user."); userEndGame = True; break
            if user_move.lower() == 'help':
                print("Possible moves:", legal_moves()); continue
            try:
                make_user_move(user_move); break
            except ValueError as e:
                print(e)
        if userEndGame: break
        update_board(move); move += 1
        if (msg := get_end_state()): print(msg); break

    else:
        # Kullanıcı Beyaz
        while True:
            user_move = input("\nUser (White): hamleni gir ('help' ya da 'quit'): ")
            if user_move.lower() == 'quit':
                print("Game ended by user."); userEndGame = True; break
            if user_move.lower() == 'help':
                print("Possible moves:", legal_moves()); continue
            try:
                make_user_move(user_move); break
            except ValueError as e:
                print(e)
        if userEndGame: break
        update_board(move); move += 1
        if (msg := get_end_state()): print(msg); break

        # AI Siyah
        model.act(
            chat_black,
            [get_move_history, legal_moves, possible_captures, possible_checks, get_book_moves, make_ai_move],
            max_prediction_rounds=8,
            on_message=print,
        )
        if is_ai_turn():
            make_ai_move(legal_moves()[0])
        update_board(move); move += 1
        if (msg := get_end_state()): print(msg); break
