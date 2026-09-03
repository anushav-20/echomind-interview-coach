"""
Analyzes a transcribed interview answer for delivery quality: filler word
frequency, speaking pace, and basic confidence signals derived from sentence
structure -- the kind of feedback a human interview coach would give.
"""
import re

FILLER_WORDS = ["um", "uh", "like", "you know", "sort of", "kind of", "actually", "basically", "literally"]

HEDGE_PHRASES = ["i think", "i guess", "maybe", "probably", "i'm not sure", "i suppose"]


def count_fillers(text: str) -> dict:
    text_lower = text.lower()
    counts = {}
    for filler in FILLER_WORDS:
        matches = len(re.findall(r'\b' + re.escape(filler) + r'\b', text_lower))
        if matches:
            counts[filler] = matches
    return counts


def count_hedges(text: str) -> int:
    text_lower = text.lower()
    return sum(len(re.findall(re.escape(phrase), text_lower)) for phrase in HEDGE_PHRASES)


def speaking_pace(word_count: int, duration_seconds: float) -> float:
    if duration_seconds <= 0:
        return 0.0
    return round(word_count / (duration_seconds / 60), 1)


def analyze_answer(transcript: str, duration_seconds: float) -> dict:
    words = transcript.split()
    word_count = len(words)
    fillers = count_fillers(transcript)
    filler_total = sum(fillers.values())
    hedge_count = count_hedges(transcript)
    wpm = speaking_pace(word_count, duration_seconds)

    filler_rate = round(filler_total / word_count * 100, 1) if word_count else 0

    feedback = []
    if filler_rate > 4:
        feedback.append("High filler word usage -- practice pausing silently instead of saying 'um' or 'like'.")
    if wpm > 0 and wpm < 110:
        feedback.append("Speaking pace is slower than typical conversational pace (110-150 wpm) -- consider a slightly brisker delivery.")
    elif wpm > 170:
        feedback.append("Speaking pace is quite fast -- slowing down slightly can improve clarity.")
    if hedge_count > 2:
        feedback.append("Frequent hedging language ('I think', 'maybe') may undercut perceived confidence.")
    if word_count < 30:
        feedback.append("Answer is quite short -- consider adding a specific example (STAR method: Situation, Task, Action, Result).")
    if not feedback:
        feedback.append("Solid delivery -- clear pacing and minimal filler words.")

    confidence_score = max(0, 100 - filler_rate * 5 - hedge_count * 5 - (10 if word_count < 30 else 0))

    return {
        "word_count": word_count,
        "duration_seconds": duration_seconds,
        "speaking_pace_wpm": wpm,
        "filler_words": fillers,
        "filler_rate_pct": filler_rate,
        "hedge_phrase_count": hedge_count,
        "confidence_score": round(confidence_score, 1),
        "feedback": feedback,
    }
