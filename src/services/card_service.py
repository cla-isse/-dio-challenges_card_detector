import streamlit as st
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient 
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest

from utils.config import Config

def card_analyzer(card_url):
    try:
        st.write(f"A URL foi recebida para análise")

        # Inicializa Client
        credential = AzureKeyCredential(Config.KEY_DOC)
        if not credential.key:
            st.write("Erro: A chave de autenticação do Azure está vazia ou inválida.")
        
        document_Client = DocumentIntelligenceClient(Config.ENDPOINT_DOC, credential)
        st.write("Cliente Azure Document Intelligence inicializado com sucesso.")

        try:
            # Chama a API
            card_info = document_Client.begin_analyze_document(
                "prebuilt-creditCard", AnalyzeDocumentRequest(url_source=card_url))
            st.write("Solicitação enviada para o Azure, aguardando resposta...")
        except Exception as ex:
            st.write(f"Erro ao enviar a solicitação para o Azure: {str(ex)}")

        # Espera a conclusão da análise
        result = card_info.result()

        if not result:
            st.write(st.write("Erro: Não foi possível obter uma resposta válida da API."))

        # Verifica documentos retornados
        if not result.documents:
            raise ValueError("Nenhum documento analisado.")
        
        fields = result.documents[0].fields

        def get_field_content(field):
            return field.content if field else None
        
        return {
            "card_name": get_field_content(fields.get("CardHolderName")),
            "card_number": get_field_content(fields.get("CardNumber")),
            "expiry_date": get_field_content(fields.get("ExpirationDate")),
            "bank_name": get_field_content(fields.get("IssuingBank")),
        }
    
    except Exception as ex:
        st.write(f"Erro ao validar o cartão: {ex}")
        return {"error": str(ex)}