import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import SyncStream from "./App";

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
    <React.StrictMode>
        <SyncStream />
    </React.StrictMode>
);
