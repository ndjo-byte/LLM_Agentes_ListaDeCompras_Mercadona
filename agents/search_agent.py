from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq 
import os
from dotenv import load_dotenv
import pandas as pd 
from classify_agent import ClassifyAgent
import re 

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

prompt = ChatPromptTemplate.from_messages([
        ("system", "Eres un asistente que busca productos en la lista de productos de Mercadona."),
        ("user", "Necesito saber qué productos disponibles en Mercadona son los que necesito, según la lista de productos."),
        ("user", "{user_input}")
    ])


class SearchAgent:
    def __init__(self, product_data, product_list):
        self.product_data = product_data # From CSV
        self.product_list = [product.lower() for product in product_list] # From ClassifyAgent
        self.chain = prompt | llm 

    def get_available_products(self) -> str:
        """
        Get the available products from the product_data.
        """

        available_products = []
        for product in self.product_list:
            matches = self.product_data[
                self.product_data['display_name'].str.lower().str.contains(rf"\b{re.escape(product)}\b", na=False)].head(10) # case insensitive, partial matching with REGEX
            if not matches.empty:
                available_products.append(matches)
        
        available_products_df = pd.concat(available_products)
        catalog_text = available_products_df.to_string(index=False)
        return catalog_text
    

    def search(self) -> str:
        """
        Use the LLM to match products from the ClassifyAgentproduct list products available in Mercadona product_data.
        """
        available_products = self.get_available_products()

        # Format the full user input with both the product list and available catalog
        user_input = f"""
        Esta es la lista de productos que necesito: {', '.join(self.product_list)}

        Esta es la lista de productos disponibles en Mercadona:
        {available_products}

        Devuélveme solo los productos de mi lista que están disponibles, con su nombre, formato y precio. Elige solo 1 producto por cada producto de la lista, el más barato.
        """

        return self.chain.invoke({"user_input": user_input})
        

if __name__ == "__main__":
    agent = SearchAgent(simple_products, ["leche entera", "pan", "queso"])
    result = agent.search()
    print(result.content)