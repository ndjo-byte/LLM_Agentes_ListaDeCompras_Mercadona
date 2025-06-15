import os
import streamlit as st
from agents.pipeline import ProductPipeline

st.title("Lista de Compras")

user_input = st.text_input("¿Qué quieres comprar? Ejemplo: 'Voy a preparar una ensalada griega y necesito limpiar la cocina.'")

if st.button("Generar lista de compras"):
    pipeline = ProductPipeline(user_input)
    pipeline.run()
    filepath = pipeline.save_to_txt(folder="txt")
    st.success("Lista de compras generada correctamente")
    st.text_area("Contenido de la lista", pipeline.ticket_text, height=200)

# List all tickets in the folder
ticket_folder = "txt"
if os.path.exists(ticket_folder):
    ticket_files = sorted(os.listdir(ticket_folder), reverse=True)  # show newest first
    if ticket_files:
        selected_file = st.selectbox("Selecciona un ticket para descargar:", ticket_files)

        # Read selected ticket file content into ticket_content
        full_path = os.path.join(ticket_folder, selected_file)
        with open(full_path, "r", encoding="utf-8") as f:
            ticket_content = f.read()

        st.text_area("Contenido del ticket seleccionado", ticket_content, height=200)

        # Provide download button for the selected ticket
        st.download_button(
            label="Descargar ticket",
            data=ticket_content,
            file_name=selected_file,
            mime="text/plain",
        )
    else:
        st.info("No hay tickets guardados aún.")
else:
    st.info(f"La carpeta '{ticket_folder}' no existe.")

# streamlit run app.py
