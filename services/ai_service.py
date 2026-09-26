import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()


def analyze_food_image(image_bytes, image_type):
    """
    Identify the main food or dish in a meal image using Gemini.
    """

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY is not configured.")

    client = genai.Client(api_key=api_key)

    image = types.Part.from_bytes(
        data=image_bytes,
        mime_type=image_type
    )

    prompt = """
    You are the food recognition component of NutriSnap.

    Analyze the provided meal image and identify the main food or dish.

    Return your answer in exactly this format:

    Food: <food name>
    Confidence: <Low, Medium, or High>

    Rules:
    - Identify the main visible dish.
    - Use a concise, commonly used food name.
    - Choose a name that would be suitable for searching a nutrition database.
    - Do not estimate calories or nutrition values.
    - Do not provide explanations.
    """

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=[image, prompt]
    )

    return response.text.strip()