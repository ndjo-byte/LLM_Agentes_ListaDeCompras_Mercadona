from agents.classify_agent import ClassifyAgent 

if __name__ == "__main__":
    user_input = input("¿Qué quieres comprar? Ejemplo: 'Voy a preparar una ensalada griega y necesito limpiar la cocina.'")
    agent = ClassifyAgent(user_input)
    result = agent.classify()
    print(result)   

