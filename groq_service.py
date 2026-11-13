"""groq_service.py - talks to the Groq API. The API key never leaves the server."""
import os
import time

import groq
from dotenv import load_dotenv
from groq import Groq

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"), override=True)

DEFAULT_MODEL = "llama-3.3-70b-versatile"


class GroqServiceError(Exception):
    """Error with a safe, user-friendly message (never contains secrets)."""


def generate_message(prompt):
    api_key = os.getenv("GROQ_API_KEY", "").strip()
    model = os.getenv("GROQ_MODEL", "").strip() or DEFAULT_MODEL

    

    if not api_key or api_key in ("your_actual_api_key_here", "replace_with_your_key"):
        raise GroqServiceError("API key is missing. Add GROQ_API_KEY to your .env file and restart the app.")

    client = Groq(api_key=api_key)
    attempts = 0

    # While loop: retry once on a temporary connection problem
    while attempts < 2:
        attempts += 1
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system",
                     "content": "You are a helpful professional email and message writing assistant."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
            )
            text = (response.choices[0].message.content or "").strip()
            if not text:
                raise GroqServiceError("The AI returned an empty response. Please try again.")
            return text

        except groq.APIConnectionError:
            if attempts < 2:
                time.sleep(1)
                continue
            raise GroqServiceError("Unable to connect to the AI service. Check your internet connection.")
        except groq.AuthenticationError:
            raise GroqServiceError("The Groq API key is invalid. Check GROQ_API_KEY in your .env file.")
        except groq.RateLimitError:
            raise GroqServiceError("Too many requests. Please wait a moment and try again.")
        except groq.NotFoundError:
            raise GroqServiceError("The selected AI model is not available. Update GROQ_MODEL in your .env file.")
        except groq.BadRequestError:
            raise GroqServiceError("The AI model could not accept this request. Check GROQ_MODEL in your .env file.")
        except GroqServiceError:
            raise
        except Exception:
            raise GroqServiceError("Something went wrong. Please try again.")
