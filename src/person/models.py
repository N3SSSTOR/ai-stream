from pydantic import BaseModel


class PersonModel(BaseModel):
    prompt: str 
    voice: str 
    words_correction: dict | None = None 
    talking_scene_path: str | None = None 