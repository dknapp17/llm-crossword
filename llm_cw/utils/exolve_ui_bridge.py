
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
    const frame = parentElement.querySelector("#exolve-frame");

    function handleMessage(event) {
        if (event.origin !== window.location.origin) {
            return;
        }

        if (event.source !== frame.contentWindow) {
            return;
        }

        const message = event.data;

        if (message?.type === "EXOLVE_LOADED") {
            setStateValue("event", {
                type: "crossword_loaded",
            });
        }

        if (message?.type === "EXOLVE_CLUE") {
            setStateValue("event", {
                type: "clue_selected",
                index: message.index,
                clue_text: message.text,
                answer_length: message.answer_length,
            });
        }
    }

    window.addEventListener("message", handleMessage);

    const crossword = data.crossword;

    frame.src =
        `/app/static/exolve/exolve-embedder.html?crossword=${encodeURIComponent(crossword)}&v=3`;

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
    key: str | None = None,
) -> dict:
    result = _component(
        data={"crossword": crossword},
        default={"event": None},
        key=key,
    )

    return result.event
