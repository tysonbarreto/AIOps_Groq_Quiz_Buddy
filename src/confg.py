import os
from pydantic_settings import BaseSettings
from langchain_groq.chat_models import ChatGroq

class Settings(BaseSettings):
    groq_api_key:str
    
    class Config:
        env_file=".env"

class Parameters:
    MODEL_NAME = "llama-3.1-8b-instant"
    TEMPERATURE = 0.9
    MAX_RETRIES = 3
     
class GroqConfig:
    @classmethod
    def groq_client(cls)->ChatGroq:
        settings = Settings()
        return ChatGroq(
            api_key=settings.groq_api_key,
            model=Parameters.MODEL_NAME,
            temperature=Parameters.TEMPERATURE,
            max_retries=3
        )
if __name__=="__main__":
    __all__=["Parameters","GroqConfig"]

