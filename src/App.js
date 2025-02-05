function App() {
    return (
        <div className="app">
            <img src="/images/Navbar.png" alt="Navbar" className="navbar-image" />
            <div className="split left">
                <img src="/images/image 1.svg" alt="Icon" className="image-left" />
                <div className="container-left"></div>
                <img src="/images/Cute Avatar.svg" alt="Cute Avatar" className="image-1" />
                <img src="/images/x.svg" alt="X Icon" className="image-2" />
                <img src="/images/Preview.svg" alt="Preview Icon" className="image-3" />
            </div>
            <div className="split right">
                <div className="div-board">
                    <img src="/images/board.png" alt="Board" className="board" />
                </div>
                <img src="/images/image 2.png" alt="Piece" className="piece-right-image" />
            </div>
        </div>
    );
}

export default App;
