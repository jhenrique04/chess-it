from flask import Flask, send_file
import os

app = Flask(__name__)

script_dir = os.path.dirname(os.path.abspath(__file__))
board_svg_path = os.path.join(script_dir, "current_board.svg")

@app.route("/board")
def get_board():
    """ Return the current board SVG image. """
    if os.path.exists(board_svg_path):
        return send_file(board_svg_path, mimetype="image/svg+xml")
    return "Board not found", 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
