from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq 
import os
from dotenv import load_dotenv
import pandas as pd 
from classify_agent import ClassifyAgent
from search_agent import SearchAgent

# Load CSV Data to DataFrame
simple_products = pd.read_csv("../csv_files/simple_products.csv")

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

# Prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "Eres un asistente que crea un ticket de compra con los precios y cantidades de productos de Mercadona."),
    ("user", """
Crea un ticket de compra con los siguientes productos y sus cantidades necesarias:

Productos disponibles:
{products}

Cantidades necesarias:
{quantities}

Indica si algún producto no está disponible.
Calcula el precio total (solo de los disponibles). El resultado debe ser claro y fácil de leer.
""")
])

class CalculateAgent:
    def __init__(self, srch_result: str, clfy_result_quantities: list[tuple[str, str]]):
        self.srch_result = srch_result  # string (from srch_result.content)
        self.quantities = clfy_result_quantities  # list of (product, quantity)
        self.chain = prompt | llm

    def run(self):
        # Convert list of tuples to string for the prompt
        quantity_str = "\n".join([f"- {product}: {quantity}" for product, quantity in self.quantities])

        response = self.chain.invoke({
            "products": self.srch_result,
            "quantities": quantity_str
        })

        return response.content


if __name__ == "__main__":
    clfy_agent = ClassifyAgent("Voy a preparar una ensalada griega y necesito limpiar la cocina.")
    clfy_result = clfy_agent.classify()
    clfy_result_quantities = clfy_agent.get_product_quantities(clfy_result)

    srch_agent = SearchAgent(simple_products, clfy_agent.get_products(clfy_result))
    srch_result = srch_agent.search()

    calc_agent = CalculateAgent(srch_result, clfy_result_quantities)
    print(calc_agent.run())
