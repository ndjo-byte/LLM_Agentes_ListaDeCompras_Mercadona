from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_groq import ChatGroq 
import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field

# Cargar variables de entorno
load_dotenv()

# Obtener la clave API
api_key = os.getenv("GROQ_API_KEY")

# LLM
llm = ChatGroq(
    model_name="llama3-70b-8192",
    temperature=0.7,
    api_key=api_key
)

# Esquema de salida
class PydanticSchema(BaseModel):
    intent: list[str] = Field(description="La intención del usuario para la compra")
    products: list[str] = Field(description="La lista de productos que el usuario necesita comprar")

# Prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "Eres un asistente que clasifica la intención del usuario y extrae una lista de productos para comprar."),
    ("user", "Necesito comprar cosas para cocinar boloñesa y para limpiar el baño. Clasifica los productos que necesito."),
    ("ai", '{{"intent": ["cocina", "limpieza"], "products": ["carne picada", "salsa de tomate", "espaguetis", "ajo", "limpiador de inodoro", "esponja"]}}'),
    ("user", "{input}")
])

# Parser JSON basado en el schema
parser = JsonOutputParser(pydantic_object=PydanticSchema)

# Pipeline
chain = prompt | llm | parser

# Entrada del usuario
user_input = "Voy a preparar una ensalada griega y necesito limpiar la cocina. ¿Qué cosas necesito comprar?"

# Invocar la cadena
print(chain.invoke({"input": user_input}))
