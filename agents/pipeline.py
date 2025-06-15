from .classify_agent import ClassifyAgent
from .search_agent import SearchAgent
from .calculate_agent import CalculateAgent
import pandas as pd
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()  # loads environment variables from .env file

csv_path = os.getenv("CSV_PATH")

# Load CSV Data to DataFrame
simple_products = pd.read_csv(csv_path)
    
class ProductPipeline:
    def __init__(self, user_input: str):
        self.user_input = user_input
        self.clfy_agent = ClassifyAgent(user_input)
        self.srch_agent = SearchAgent(simple_products, self.clfy_agent.get_products(self.clfy_agent.classify()))

    def run(self):
        clfy_result = self.clfy_agent.classify()
        srch_result = self.srch_agent.search()
        calc_result = CalculateAgent(srch_result, self.clfy_agent.get_product_quantities(clfy_result))
        self.ticket_text = calc_result.calculate()
        return self.ticket_text
    
    def save_to_txt(self, folder="txt"):
        os.makedirs(folder, exist_ok=True)
        # Create a timestamped filename: ticket_2025-06-15_1427.txt
        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        filename = f"ticket_{timestamp}.txt"
        file_path = os.path.join(folder, filename)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(self.ticket_text)
        return file_path


if __name__ == "__main__":
    pipeline = ProductPipeline("Voy a preparar una ensalada griega y necesito limpiar la cocina.")
    print(pipeline.run())
    pipeline.save_to_txt()