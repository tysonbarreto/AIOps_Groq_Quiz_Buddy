from typing import Union

from .schema import MCQQuestion, FillBlankQuestion
from .prompts import Prompts
from .logger import get_logger
from .exception import AIException
from .confg import GroqConfig, Parameters

from langchain.output_parsers import PydanticOutputParser
from langchain_groq.chat_models import ChatGroq
from langchain.prompts import PromptTemplate



class QuestionGenerator:
    def __init__(self):
        self.llm:ChatGroq = GroqConfig.groq_client()
        self.logger = get_logger(self.__class__.__name__)
        
    def __retry_and_parse(self, prompt:PromptTemplate, parser:PydanticOutputParser, topic:str, difficulty:str)->Union[MCQQuestion,FillBlankQuestion]:
        for attempt in range(Parameters.MAX_RETRIES):
            try:
                self.logger.info(f"Generating question for topic {topic} with difficulty {difficulty}")
                response = self.llm.invoke(prompt.format(topic=topic, difficulty=difficulty))
                parsed = parser.parse(response.content)
                
                self.logger.info("Successfully parsed the question")
                
                return parsed
            except Exception as e:
                self.logger.error(f"Error : {str(e)}")
                if attempt==Parameters.MAX_RETRIES-1:
                    raise AIException(f"Generation failed after {Parameters.MAX_RETRIES} attempts", e)
    
    def generate_mcq(self, topic:str, difficulty:str='medium')->MCQQuestion:
        try:
            parser = PydanticOutputParser(pydantic_object=MCQQuestion)
            question = self.__retry_and_parse(Prompts.mcq_prompt_template, parser, topic, difficulty)
            
            if len(question.options) != 4 or question.correct_answer not in question.options:
                raise ValueError("Invalid MCQ Structure")
            
            self.logger.info("Generated a valid MCQ Question")
            return question
        
        except Exception as e:
            self.logger.error(f"Failed to generate MCQ : {str(e)}")
            raise AIException("MCQ generation failed" , e)
        
    def generate_fill_blank(self, topic:str, difficulty:str='medium')->FillBlankQuestion:
        try:
            parser = PydanticOutputParser(pydantic_object=MCQQuestion)
            question = self.__retry_and_parse(Prompts.mcq_prompt_template, parser, topic, difficulty)
            
            if "___" not in question.question:
                raise ValueError("Fill in blanks should contain '___'")
            
            self.logger.info("Generated a valid MCQ Question")
            return question
        
        except Exception as e:
            self.logger.error(f"Failed to generate fillups : {str(e)}")
            raise AIException("Fill in blanks generation failed" , e)

if __name__=="__main__":
    __all__=["QuestionGenerator"]