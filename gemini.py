from typing import List, Dict, Any
import json
from models import BatchFormattedDefinitions
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
