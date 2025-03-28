import { useEffect, useState } from "react";

import io from "socket.io-client";
import styles from "./RemoteController.module.css";

// const host = "http://192.168.1.200:5125";
// const socket = io("ws://192.168.1.200:5125");

// const host = "http://192.168.1.200:5125";
const socket = io();

const RemoteController = () => {
  const [text, setText] = useState("");
  // const [localIp, setLocalIp] = useState("");

  const sendAction = async (endpoint, action) => {
    try {
      const response = await fetch(`/api${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ action }),
      });
    } catch (error) {
      console.error("Error:", error);
    }
  };

  const sendText = async (text) => {
    try {
      await fetch(`/api/send_text`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
      });
    } catch (error) {
      console.error("Error sending key:", error);
    }
  };

  const handleKeyDown = async (event) => {
    if (event.key === "Enter") {
      await sendText(text);
      setText("");
    }
  };

  const handleTouch = async (event, route) => {
    event.preventDefault();
    const touch = event.touches[0];
    const x = touch.clientX;
    const y = touch.clientY;
    socket.emit(route, { x, y });
  };

  return (
    <div className={styles.container}>
      <div className={styles.inputContainer}>
        <label htmlFor="text-input"></label>
        <input
          id="text-input"
          type="text"
          placeholder="Enter text"
          value={text}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={handleKeyDown}
          className={styles.inputField}
        />
        <button
          className={styles.button}
          onClick={() => {
            sendText("backspace");
          }}
        >
          <img src="./left_arrow.svg" alt="bsp" className={styles.icon} />
        </button>
      </div>

      <div className={styles.volumeButtons}>
        <button
          className={styles.button}
          onClick={() => sendAction("/volume", "increase")}
        >
          +
        </button>
        <button
          className={styles.button}
          onClick={() => sendAction("/volume", "decrease")}
        >
          –
        </button>
      </div>

      <div className={styles.mouseButtons}>
        <button
          className={styles.button}
          onClick={() => sendAction("/mouse_click", "left")}
        >
          L
        </button>
        <button
          className={styles.button}
          onClick={() => sendAction("/mouse_click", "right")}
        >
          R
        </button>
      </div>
      <div
        id="touch-area"
        className={styles.touchArea}
        onTouchStart={(e) => handleTouch(e, "mouse_start")}
        onTouchMove={(e) => handleTouch(e, "mouse_move")}
      ></div>
    </div>
  );
};

export default RemoteController;
