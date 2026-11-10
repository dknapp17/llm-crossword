
import hashlib
from pathlib import Path

import streamlit as st

HTML = """
<iframe
    id="exolve-frame"
    title="Interactive crossword"
    width="100%"
    height="800"
    style="border: none;"
></iframe>
"""


JS = """
export default function(component) {
    const { parentElement, data, setStateValue } = component;
    console.log("Component data:", data);
    const command = data.command;
    console.log("Command received by component:", command);
    const frame = parentElement.querySelector("#exolve-frame");

    if (command) {
        frame.contentWindow.postMessage(
            command,
            window.location.origin
        );
    }

    const crossword = data.crossword;
    const crosswordUrl =
        `/app/static/exolve/exolve-embedder.html?crossword=${encodeURIComponent(crossword)}&v=${data.version}`;

    if (frame.src !== new URL(crosswordUrl, window.location.origin).href) {
        frame.src = crosswordUrl;
        console.log("Assigned iframe URL:", frame.src);
    }
    

    

    
    
    function handleMessage(event) {
        console.log("Component received message:", event.data);
        console.log("Full message data:", event.data);
        if (event.data?.type === "EXOLVE_LOADED" && command) {
            console.log("Exolve is ready");
            console.log("Sending command to iframe:", command);
        }
        if (event.origin !== window.location.origin) {
            return;
        }

        if (event.source !== frame.contentWindow) {
            return;
        }

        if (event.data?.type !== "EXOLVE_CLUE") {
            return;
        }

        setStateValue("clue", event.data);
        console.log("Sent TEST_RESPONSE to Streamlit:", event.data);
    }

    window.addEventListener("message", handleMessage);

    return () => {
        window.removeEventListener("message", handleMessage);
    };
}
"""


_component = st.components.v2.component(
    "exolve_ui_bridge",
    html=HTML,
    js=JS,
)


def exolve_component(
    crossword: str,
) -> dict | None:
    exolve_js = (
        Path(__file__).resolve().parents[2]
        / "app"
        / "static"
        / "exolve"
        / "exolve-embedder.js"
    )

    version = hashlib.md5(exolve_js.read_bytes()).hexdigest()
    result = _component(
        data={
            "crossword": crossword,
            "version": version,
            "command": {"type": "TEST"},
        },
    )

    st.write("Component result:", result)

    return result
