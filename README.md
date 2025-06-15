
# 🧠 Mercadona API - GenAI Shopping List Assistant

A modular NLP pipeline built with LangChain and Groq LLMs for classifying user shopping intentions, searching product data, and calculating a final receipt. Designed for MVP-level performance using simple pandas filtering and streamlined prompt engineering — no embeddings or vector stores required.

## 🎥 Demo Video
https://youtu.be/vF19gx2CZaU

---

## 📌 Methodology  

This project is based on three agent classes working in sequence:  

### 1. ✔️ **ClassifyAgent**   
- Classifies user intentions and extracts relevant products and quantities from free-form input.  
- Returns a dictionary:  
  ```python  
  {
    "intentions": ["cocina", "limpieza"],  
    "products": {
        "lechuga": "1",
        "queso feta": "1 bloque",
        ...
    }
  }
```

- Uses a simple ChatPromptTemplate, and has performed exceptionally even without FewShotPrompt examples.  
- Provides:  
    classify() – Returns full classification dict.  
    get_products() – Extracts only the list of product names (used by the SearchAgent).  
    get_product_quantities() - Extracts the product and quantity for each classification result. For use with the CalculateAgent.  

Note: get_products() depends on classify() being run first. May need to cache classify_result() in the future.  

### 2. 🕵🏻‍♂️ **SearchAgent**  
-Performs lightweight RAG using a local .csv version of Mercadona product catalog.  
- Uses pandas DataFrame filtering instead of a vector store:  
    REGEX with word boundaries to increase accuracy.  
    Limited to top 10 matches per product to avoid LLM token limit errors.    
- Returns a summarized availability list and basic product data (name, price, unit).  
- Input: List of products from ClassifyAgent.get_products().  
- A future version will use Chroma for Vectorise Store of the Mercadona API data, and OpenAIEmbeddings. This will provide for more accurate searches.  


### 3. ➕ **CalculateAgent**   
- Takes classified product quantities and matched search results.  
- Formats a receipt, including:  
    Product names  
    Prices  
    Units  
    Availability  
    Total cost  
- Returns a final receipt using a Groq LLM prompt.  
-  Output ready to present in UI or Streamlit.  

### 🔄 Pipeline Integration  
To encapsulate agent logic, a Pipeline class has been implemented to handle:  

    pipeline = ProductPipeline(user_input)  
    pipeline.run()  
    pipeline.save_to_text()  
    
Benefits:   
- Keeps logic out of app.py  
- Improves readability  
- Centralizes the agent flow  

### 🧪 Testing & Performance  

- ClassifyAgent performs semantic parsing better than expected, although a future model which implements LangGraph, Chroma and OpenAIEmbedding will be more powerful.
- SearchAgent yields high precision with pandas filters and REGEX.  
- LLM size token limits handled via manual row filtering (top 10 matches).  
- CalculateAgent outputs accurate receipts.  
- Pipeline end-to-end tested.  
- Streamlit demo app working with .env config and CSV absolute path handling.  

## 📁 Project Structure  

product-assistant/  
│  
├── agents/  
│   ├── classify_agent.py  
│   ├── search_agent.py  
│   ├── calculate_agent.py  
│   └── __init__.py  
│  
├── product_pipeline.py  
├── app.py  
├── main.py  
├── .env  
├── requirements.txt  
└── csv_files/  
    └── simple_products.csv  


## ⚙️ Setup  

**Clone the repo:**  
git clone https://github.com/ndjo-byte/LLM_Agentes_ListaDeCompras_Mercadona.git  
cd product-assistant  
**Install dependencies:**  
pip install -r requirements.txt  
**Set your environment variables in .env:**  
GROQ_API_KEY=your_api_key  
CSV_PATH=/absolute/path/to/simple_products.csv  
**Run the app or pipeline:**  
python main.py  
**Optional: Launch Streamlit demo**  
streamlit run app.py  

