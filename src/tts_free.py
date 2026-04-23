import logging
import queue
import threading
import time
from typing import Optional
import pyttsx3

from config_voice import (
    ANNOUNCEMENT_COOLDOWN_SECONDS,
    GESTURE_TO_TEXT,
    TTS_MAX_LATENCY_SECONDS,
    TTS_REPEAT_COOLDOWN_SECONDS,
)

logger = logging.getLogger(__name__)

_last_spoken_text: Optional[str] = None
_last_spoken_at: Optional[float] = None
_last_enqueued_text: Optional[str] = None
_last_enqueued_at: Optional[float] = None
_state_lock = threading.Lock()
_tts_queue: "queue.Queue[tuple[str, float]]" = queue.Queue()
_worker_started = False


def speak_gesture(gesture: str) -> tuple[bool, str]:
    global _last_enqueued_text, _last_enqueued_at

    text = GESTURE_TO_TEXT.get(gesture)
    if not text:
        logger.debug("Gesture '%s' not mapped to text; skipping TTS.", gesture)
        return False, "gesture_not_mapped"

    _start_worker_if_needed()

    now = time.monotonic()
    with _state_lock:
        if _last_spoken_at is not None:
            cooldown_elapsed = now - _last_spoken_at
            if cooldown_elapsed < ANNOUNCEMENT_COOLDOWN_SECONDS:
                return False, "announcement_cooldown"

        if _last_spoken_text == text and _last_spoken_at is not None:
            if now - _last_spoken_at < TTS_REPEAT_COOLDOWN_SECONDS:
                return False, "repeat_cooldown_spoken"
        if _last_enqueued_text == text and _last_enqueued_at is not None:
            if now - _last_enqueued_at < TTS_REPEAT_COOLDOWN_SECONDS:
                return False, "repeat_cooldown_enqueued"
        _last_enqueued_text = text
        _last_enqueued_at = now
        _clear_pending_queue()
    _tts_queue.put((text, now))
    return True, "accepted"


def _worker_loop():
    global _last_spoken_text, _last_spoken_at
    while True:
        text, enqueued_at = _tts_queue.get()
        try:
            if time.monotonic() - enqueued_at > TTS_MAX_LATENCY_SECONDS:
                logger.warning("Skipping late TTS playback for '%s'.", text)
                continue

            # Use PowerShell SAPI for zero-latency, deadlock-free TTS on Windows
            import subprocess
            # CREATE_NO_WINDOW = 0x08000000 ensures no console pops up
            subprocess.run(
                ["powershell", "-c", f"(New-Object -ComObject SAPI.SpVoice).Speak('{text}')"],
                creationflags=0x08000000
            )

            with _state_lock:
                _last_spoken_text = text
                _last_spoken_at = time.monotonic()
        except Exception as exc:
            logger.error("TTS failed for '%s': %s", text, exc)


def _clear_pending_queue() -> None:
    try:
        while True:
            _tts_queue.get_nowait()
    except queue.Empty:
        return


def _start_worker_if_needed():
    global _worker_started
    if _worker_started:
        return
    worker = threading.Thread(target=_worker_loop, daemon=True)
    worker.start()
    _worker_started = True
