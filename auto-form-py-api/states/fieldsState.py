import logging
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain.schema.runnable import RunnablePassthrough

from utils.llmfactory import LLMFactory
from pds.QuestionDS import QuestionDS
from pds.RequestDS import RequestDS
from pds.ResponseDS import ResponseDS
from prompts.templates import *
import dotenv

class FieldsState:
    def __init__(self, llm_type="openai", model_name="gpt-4o-mini", temperature=0.7):
        dotenv.load_dotenv()
        self.llm_factory = LLMFactory()
        self.llm = self.llm_factory.create_llm(
            llm_type=llm_type,
            model_name=model_name,
            temperature=temperature
        )
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)



    def ask(self, input):
        self.logger.info("Starting the question chain")
        
        parser = JsonOutputParser(pydantic_object=QuestionDS)

        format_instructions = parser.get_format_instructions()

        prompt = PromptTemplate(template=questioner_prompt, input_variables=["request"], partial_variables={"format_instructions":format_instructions})

        request = input

        chain = ({"request" : RunnablePassthrough()} 
                 | prompt 
                 | self.llm 
                 | parser
                 )
        

        response = chain.invoke({"request":request})
        self.logger.info(f"Received response: {response}")

        # parsed_response = parser.parse(response)
        # self.logger.info(f"Parsed response: {parsed_response}")
        
        return response.get("question","")

    def process(self, answer_object: RequestDS):
        self.logger.info("Starting the answer chain")
        
        parser = JsonOutputParser(pydantic_object=ResponseDS)

        format_instructions = parser.get_format_instructions()

        prompt = PromptTemplate(template=field_prompt, input_variables=["request"], partial_variables={"format_instructions":format_instructions})

        chain = ({"request" : RunnablePassthrough()} 
                 | prompt 
                 | self.llm 
                 | parser
                 )
        

        response = chain.invoke({"request":repr(answer_object)})
        self.logger.info(f"Received response: {response}")

        # parsed_response = parser.parse(response)
        # self.logger.info(f"Parsed response: {parsed_response}")
        
        
        
        return self._validate(repr(answer_object)+f', field_value={response.get("field_value","")}')
    
    def _validate(self, input):
        self.logger.info("Starting the validation chain")
        
        parser = JsonOutputParser(pydantic_object=ResponseDS)

        format_instructions = parser.get_format_instructions()

        prompt = PromptTemplate(template=validation_prompt, input_variables=["request"], partial_variables={"format_instructions":format_instructions})

        request = input

        chain = ({"request" : RunnablePassthrough()} 
                 | prompt 
                 | self.llm 
                 | parser
                 )
        

        response = chain.invoke({"request":request})
        self.logger.info(f"Received response: {response}")

        # parsed_response = parser.parse(response)
        # self.logger.info(f"Parsed response: {parsed_response}")
        
        return response.get("field_value","")
        
