
from pathlib import Path

import streamlit as st
import hashlib

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
    const frame = parentElement.querySelector("#exolve-frame");

    const crossword = data.crossword;
    frame.src =
        `/app/static/exolve/exolve-embedder.html?crossword=${encodeURIComponent(crossword)}&v=${data.version}`;
    console.log("Assigned iframe URL:", frame.src);
    if (command) {
        frame.contentWindow.postMessage(
            command,
            window.location.origin
        );
    }

    

    
    
    function handleMessage(event) {
        console.log("Component received message:", event.data);
        console.log("Full message data:", event.data);
        if (event.data?.type === "EXOLVE_LOADED") {
            console.log("Exolve is ready");

            frame.contentWindow.postMessage(
                command,
                window.location.origin
            );
        }
        if (event.origin !== window.location.origin) {
            return;
        }

        if (event.source !== frame.contentWindow) {
            return;
        }

        if (event.data?.type !== "TEST_RESPONSE") {
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
    st.write("JavaScript version:", version)
    st.write("Component result:", repr(result))

    return result
