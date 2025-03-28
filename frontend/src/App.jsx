import React, { useState } from "react";

import "./App.css";
import RemoteController from "./RemoteController";

function App() {
  // const [deviceIp, setDeviceIp] = useState("192.168.1.200");
  // const [deviceName, setDeviceName] = useState("y0oo");

  return (
    <div className="App">
      <RemoteController />
    </div>
  );
}

export default App;
