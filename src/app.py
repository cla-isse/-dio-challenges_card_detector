import streamlit as st
from services.blob_service import upload_blob
from services.card_service import card_analyzer

def configure_interface():
    st.title('Project Card Detector - Azure Document Intelligence')
    uploaded_file = st.file_uploader("Faça upload do seu arquivo", type=["png", "jpg", "jpeg"])

    if uploaded_file:
        file_name = uploaded_file.name

        # Envio para o Azure Blob Storage
        blob_url = upload_blob(uploaded_file, file_name)

        if blob_url:
            st.write(f'O arquivo {file_name} foi enviado com sucesso para o Azure Blob Storage')
            card_info = card_analyzer(blob_url) # Chama a função card_analyzer em card_service
            show_image_and_validation(blob_url, card_info)
            
        else:
            st.write(f'Não foi possível enviar {file_name} para o Azure Blob Storage')


def show_image_and_validation (blob_url, card_info):
    st.image(blob_url, caption = 'Imagem enviada')
    if isinstance(card_info, dict) and "error" not in card_info:
        card_name = card_info.get("card_name")
        
        if card_name:
            st.markdown("<h1 style='color: green;'>Cartão Válido</h1>", unsafe_allow_html=True)
            st.write("Informações de cartão de crédito encontradas:")
            st.write(f"Nome do Titular: {card_name}")
            st.write(f"Número do Cartão: {card_info.get('CardNumber')}")
            st.write(f"Banco Emissor: {card_info.get('bank_name')}")
            st.write(f"Data de Validade: {card_info.get('expiry_date')}")
        else:
            st.markdown("<h1 style='color: red;'>Cartão Inválido</h1>", unsafe_allow_html=True)
    
    else:
        st.error(f"Erro ao validar o cartão: {card_info.get('error', 'Desconhecido')}")

if __name__ == '__main__':
    configure_interface()
