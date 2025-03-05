import chess
import chess.svg
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
import numpy as np

yolo_to_fen = {
    0: 'P', 1: 'N', 2: 'B', 3: 'R', 4: 'Q', 5: 'K',
    6: 'p', 7: 'n', 8: 'b', 9: 'r', 10: 'q', 11: 'k'
}


def map_to_fen(boxes, frame_size, board_size=(8, 8)):
    board_grid = np.full(board_size, '1', dtype=str)
    height, width = frame_size

    cell_height = height / 8
    cell_width = width / 8

    for box in boxes:
        x, y, w, h, cls = box
        cls = int(cls)
        center_x = x + w / 2
        center_y = y + h / 2

        row = min(max(int(center_y // cell_height), 0), 7)
        col = min(max(int(center_x // cell_width), 0), 7)

        if board_grid[row, col] == '1':
            board_grid[row, col] = yolo_to_fen.get(cls, '?')

    fen_rows = []
    for row in board_grid:
        fen_row = ''
        empty_count = 0
        for cell in row:
            if cell == '1':
                empty_count += 1
            else:
                if empty_count > 0:
                    fen_row += str(empty_count)
                    empty_count = 0
                fen_row += cell
        if empty_count > 0:
            fen_row += str(empty_count)
        fen_rows.append(fen_row)

    return "/".join(fen_rows) + " w KQkq - 0 1"


def fen_to_image(fen, output_path="current_board.png"):
    board = chess.Board(fen)
    svg_board = chess.svg.board(board=board)

    with open("current_board.svg", "w") as svg_file:
        svg_file.write(svg_board)

    drawing = svg2rlg("current_board.svg")
    renderPM.drawToFile(drawing, output_path, fmt="PNG")

    return output_path
