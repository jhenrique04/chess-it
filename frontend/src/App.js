import React, { useState, useEffect } from "react";

function App() {
    const [boardImage, setBoardImage] = useState("");
    const [videoStream, setVideoStream] = useState("");

    useEffect(() => {
        const updateBoard = () => {
            const timestamp = new Date().getTime();
            setBoardImage(`http://192.168.1.13:5000/board?timestamp=${timestamp}`);
        };

        updateBoard();
        const interval = setInterval(updateBoard, 1000);
        return () => clearInterval(interval);
    }, []);

    useEffect(() => {
        setVideoStream("http://192.168.1.13:5000/video");
    }, []);

    return (
        <div className="app">
            <div className="split left">
                <div className="container-left">
                    <img src={videoStream} alt="Camera Feed" className="camera-feed" />
                </div>
            </div>
            <div className="split right">
                <div className="div-board">
                    <img src={boardImage} alt="Board" className="board" />
                </div>
            </div>
        </div>
    );
}

export default App;
