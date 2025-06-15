import pandas as pd
from agents.pipeline import ProductPipeline

if __name__ == "__main__":
    
    user_input = input("¿Qué quieres comprar? Ejemplo: 'Voy a preparar una ensalada griega y necesito limpiar la cocina.'")
    pipeline = ProductPipeline(user_input) # Create pipeline object
    pipeline.run() # Run pipeline
    
    pipeline.save_to_txt(folder="txt") # Save ticket to txt file

