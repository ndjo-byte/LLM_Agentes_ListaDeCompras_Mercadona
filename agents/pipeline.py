from classify_agent import ClassifyAgent
from search_agent import SearchAgent
from calculate_agent import CalculateAgent
import pandas as pd

# Load CSV Data to DataFrame
simple_products = pd.read_csv("../csv_files/simple_products.csv")
    
class ProductPipeline:
    def __init__(self, user_input: str):
        self.user_input = user_input
        self.clfy_agent = ClassifyAgent(user_input)
        self.srch_agent = SearchAgent(simple_products, self.clfy_agent.get_products(self.clfy_agent.classify()))

    def run(self):
        clfy_result = self.clfy_agent.classify()
        srch_result = self.srch_agent.search()
        calc_result = CalculateAgent(srch_result, self.clfy_agent.get_product_quantities(clfy_result))
        return calc_result.calculate()

if __name__ == "__main__":
    pipeline = ProductPipeline("Voy a preparar una ensalada griega y necesito limpiar la cocina.")
    print(pipeline.run())