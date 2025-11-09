from pydantic import BaseModel, Field
from typing import List, Dict, Any


class HskEntry(BaseModel):
    index: int = Field(
        ..., 
        description="The HSK vocabulary list index number (e.g., 1, 2, 3...)."
    )
    characters: str = Field(
        ..., 
        description="The word in Simplified Chinese characters (e.g., 爱 or 爸爸)."
    )
    pinyin: str = Field(
        ..., 
        description="The Hanyu Pinyin pronunciation with tone marks (e.g., ài or bàba)."
    )
    definition: str = Field(
        ..., 
        description="The definition or translation of the word."
    )
    
class BatchFormattedDefinitions(BaseModel):
    formatted_results: List[HskEntry] = Field(
        ..., 
        description="A list of hsk definitions, one for each input item, in the same order."
    )