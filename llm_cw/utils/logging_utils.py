from pathlib import Path

log_file = Path("solver_log.txt")


def initialize_log() -> None:
    log_file.write_text("")


def log_message(message: str) -> None:
    with log_file.open("a", encoding="utf-8") as f:
        f.write(message + "\n")