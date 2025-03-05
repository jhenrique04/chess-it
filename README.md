# Chess-it
This project aims to recognize chessboards using a YOLOv8 model trained to identify pieces and their positions. The goal is to process the board's image and make the results available through a web interface for users. The project is divided into three main components:

1. **backend** - Scripts responsible for image processing and running the recognition model.
2. **frontend** - A React-based frontend application to display the processed information.
3. **yolo** - The trained YOLOv8 model for piece detection on the board.

## Project Structure
```
├── backend
│   ├── cv_chess.py  # Main recognition script
│   ├── cv_chess_functions.py  # Helper functions for image processing
│   ├── api.py  # Flask API for communication with the frontend
│
├── frontend
│   ├── src/  # Frontend source code in React
│   ├── public/
│   ├── package.json  # Frontend dependencies
│
├── yolo
│   ├── datasets/  # Dataset directory
│   ├── models/  # Model file
│   ├── runs/  # Training results for the model
│
├── requirements.txt  # Project dependencies for the backend
└── README.md  # This file
```

## Installation and Execution
### Prerequisites
Ensure you have installed:
- Python 3.11.6
- Node.js & npm
- Project dependencies

### Setting Up and Running the Backend (chessCV)
```sh
# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run Flask API
python chessCV/api.py
```

### Setting Up and Running the Frontend
```sh
cd frontend
npm install  # Install dependencies
npm start  # Start the frontend
```

## Usage
1. Start the backend to process images of the chessboard.
2. Open the frontend to visualize the real-time positions of the pieces.
3. The YOLOv8 model is used internally for piece detection and recognition.

## Contribution
If you would like to contribute, feel free to open an issue or submit a pull request.