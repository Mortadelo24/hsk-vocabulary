from typing import List, Dict, Any
import json
from models import BatchFormattedDefinitions, BatchSpanishDefinitions
from google import genai
from google.genai import types
import pandas as pd


def fix_missing_characters(definitions: List[Dict[Any, Any]]):
    client = genai.Client()

    prompt = f"""
    You will be given a JSON list of mandarin vocabulary definitions.
    Your task is to replace the placeholders of character '(cid:n)' where n is an arbitrary integer with the correct character based on the other fields of the definition.
    Return *only* the JSON object matching the required schema.
    Use Simplified Chinese (简体中文).
    Ensure all characters are standard Unicode.
    The context is HSK 2 level vocabulary.
    
    Definitions:
    {json.dumps(definitions)}
    """
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(
                thinking_budget=0),
            response_mime_type='application/json',
            response_json_schema=BatchFormattedDefinitions.model_json_schema()
        ),

    )

    if not response.text:
        raise ValueError("No response from gemini")

    return BatchFormattedDefinitions.model_validate_json(response.text.strip()).model_dump()['formatted_results']


def translate_definitions_spanish(definitions: List[Dict[Any, Any]]):
    client = genai.Client()

    prompt = f"""
    You will be given a JSON list of mandarin vocabulary definitions.
    Your task is to make the definition more friendly for spanish native speakers that wants to study mandarin.
    You are to translate and modify the definitions in order that it is easy to understand for a Latin-american Spanish native speaker.
    You must add at the end of the definition the classifiers if there is any for that word.
    The definition does not have to be a direct translation from the english version, it should be oriented to spanish speakers.
    Return *only* the JSON object matching the required schema.

    Use Simplified Chinese (简体中文) for the characters.
    The context is HSK 2 level vocabulary.
    Don't make modifications to other fields that are not the definition field.

    Definitions:
    {json.dumps(definitions)}
    """

    response = client.models.generate_content(
        model='gemini-2.5-pro',
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type='application/json',
            response_json_schema=BatchSpanishDefinitions.model_json_schema()
        ),


    )

    if not response.text:
        raise ValueError("No response from gemini")

    return BatchSpanishDefinitions.model_validate_json(response.text.strip()).model_dump()['result']
