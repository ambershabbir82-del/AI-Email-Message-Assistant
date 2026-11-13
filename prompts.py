"""prompts.py - category/tone options and the reusable prompt builder."""

# Dictionary: key -> extra guidance for the AI (Python concept: dictionaries)
MESSAGE_TYPES = {
    "Professional Email": "a professional email. Include a subject line, greeting and closing.",
    "Student Message": "a message a student would send to a teacher or classmate. Keep it clear and respectful.",
    "Leave Application": "a leave application. Include a subject line, greeting, the request and a closing.",
    "Formal Request": "a formal request letter or email. Include a subject line, greeting and closing.",
}

TONES = {
    "Professional": "formal, confident and businesslike",
    "Polite": "courteous, respectful and gentle",
    "Friendly": "warm, relaxed and approachable, while still clear",
}

# Lists derived from the dictionaries (Python concept: lists)
MESSAGE_TYPE_LIST = list(MESSAGE_TYPES.keys())
TONE_LIST = list(TONES.keys())


def build_prompt(message, message_type, tone):
    """Build the instruction prompt sent to the AI model."""
    type_hint = MESSAGE_TYPES[message_type]
    tone_hint = TONES[tone]

    return f"""You are a professional AI writing assistant.
Your task is to improve the user's rough message.

Message Type: {message_type} - write {type_hint}
Writing Tone: {tone} - the tone must be {tone_hint}

Original Message:
{message}

Instructions:
1. Correct spelling and grammar.
2. Improve clarity and sentence structure.
3. Preserve the original meaning.
4. Follow the selected writing tone.
5. Use the selected message type.
6. Do not invent names, dates, facts or details. If a name is unknown, use a neutral greeting such as "Dear Sir/Madam".
7. Add a subject line only when the message type is an email, leave application or formal request.
8. Return only the improved message, with no explanations, notes or quotation marks.
"""
