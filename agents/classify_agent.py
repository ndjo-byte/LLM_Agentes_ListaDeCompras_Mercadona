from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_groq import ChatGroq 
import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import Dict

# Load Environment Variables 
load_dotenv()


# API Key
api_key = os.getenv("GROQ_API_KEY")

# LLM
llm = ChatGroq(
        model_name="llama3-70b-8192",
        temperature=0.7,
        api_key=api_key
    )

# Output Schema 
class PydanticSchema(BaseModel):
    intent: list[str] = Field(description="La intención del usuario para la compra")
    # Dict[str, str] is a dictionary with string keys and string values. 
    # SearchAgent will search for name matches and return information about the product, including price per 'quantity'
    # CalculateAgent will then use initial quantities to calculate final quantities and prices based on information from SearchAgent.
    products: Dict[str, str] = Field(description="Productos con cantidades específicas como '1 paquete', '500g', etc.")

# Prompt
prompt = ChatPromptTemplate.from_messages([
        ("system", "Eres un asistente que clasifica la intención del usuario y extrae una lista de productos para comprar."),
        ("user", "Necesito comprar cosas para cocinar boloñesa para 2 personas y para limpiar el baño. Clasifica los productos que necesito."),
        ("ai", '{{"intent": ["cocina", "limpieza"], "products": {{"carne picada": "1 bandeja 400g", "salsa de tomate": "1 frasco 250g", "espaguetis": "1 paquete 500g", "ajo": "1", "Don Limpio Limpiador baño": "1 botella 500ml", "estropajo": "1 paquete"}}}}'),
        ("user", "{input}")
    ])

# Parser JSON Based on the Schema 
parser = JsonOutputParser(pydantic_object=PydanticSchema)

# Class for Classify Agent
class ClassifyAgent:
    """
    Class to classify user's shopping intent and extract needed products using a language model.
    """
    def __init__(self, user_input: str):
        self.user_input = user_input
        self.chain = prompt | llm | parser
    
    def classify(self) -> dict:
        """
        Classify the user's shopping intent and extract needed products.
        """
        return self.chain.invoke({"input": self.user_input})


# Example Use with __name__ == "__main__" so that only runs when the file is executed directly
if __name__ == "__main__":
    agent = ClassifyAgent("Voy a preparar una ensalada griega y necesito limpiar la cocina.")
    result = agent.classify()
    print(result)
