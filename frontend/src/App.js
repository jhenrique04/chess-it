import React, { useState, useEffect, useRef } from "react";

function App() {
    const [boardImage, setBoardImage] = useState("/images/board.png");
    const videoRef = useRef(null);

    useEffect(() => {
        const updateBoard = () => {
            const timestamp = new Date().getTime();
            setBoardImage(`http://192.168.1.13:5000/board?timestamp=${timestamp}`);
        };

        const interval = setInterval(updateBoard, 1000);

        return () => clearInterval(interval);
    }, []);

    useEffect(() => {
        navigator.mediaDevices.getUserMedia({ video: true })
            .then((stream) => {
                if (videoRef.current) {
                    videoRef.current.srcObject = stream;
                }
            })
            .catch((err) => {
                console.error("Erro ao acessar a câmera: ", err);
            });

        return () => {
            if (videoRef.current && videoRef.current.srcObject) {
                videoRef.current.srcObject.getTracks().forEach(track => track.stop());
            }
        };
    }, []);

    return (
        <div className="app">
            <div className="split left">
                <div className="container-left">
                    <video ref={videoRef} autoPlay playsInline className="camera-feed" />
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
