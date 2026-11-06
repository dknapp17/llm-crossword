
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

    const crossword = data.crossword;

    frame.src =
        `/app/static/exolve/exolve-embedder.html?crossword=${encodeURIComponent(crossword)}&v=3`;

    function handleMessage(event) {
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
    key: str | None = None,
) -> dict | None:
    result = _component(
        data={"crossword": crossword},
        default={"clue": None},
        key=key,
        on_clue_change=lambda: None,
    )

    return result.clue
