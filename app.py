import streamlit as st
import google.generativeai as genai

# Configuração da página para uso em mobile pelos supervisores
st.set_page_config(page_title="Revisor de Mensagens", page_icon="🛡️", layout="centered")

st.title("Prática: Revisor de Mensagens")
st.markdown("Evite passivos laborais. A IA analisará o risco e sugerirá uma versão profissional e segura da sua mensagem antes do envio pelo WhatsApp.")

# Resgate seguro da Chave API (invisível no código)
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except KeyError:
    st.error("Erro de configuração: Chave de API não encontrada nos Secrets.")
    st.stop()

# Área de Entrada
st.subheader("O seu rascunho de mensagem:")
draft = st.text_area(
    "Digite o texto aqui:", 
    height=120, 
    placeholder="Ex: Ó João, tens de vir aqui limpar a unidade a correr senão dou-te uma advertência e corto-te o dia...",
    label_visibility="collapsed"
)

# Processamento
if st.button("Rever Mensagem ✨", type="primary", use_container_width=True):
    if not draft.strip():
        st.warning("Por favor, insira um texto para análise.")
    else:
        with st.spinner("A analisar riscos jurídicos..."):
            
            # Instruções de Sistema (O seu 'Advogado Trabalhista')
            system_instruction = """Você é um Advogado Trabalhista Especialista em empresas de prestação de serviços e gestão de contratos. 
            O utilizador é um supervisor que escreveu um rascunho de mensagem de WhatsApp para um funcionário da operação.
            
            Sua tarefa:
            1. Definir o Nível de Risco Trabalhista (Alto, Médio, Baixo).
            2. Apontar de forma direta e concisa o erro na mensagem.
            3. Fornecer uma sugestão de reescrita profissional, polida, assertiva e juridicamente segura.
            
            Formate a resposta em Markdown claro, destacando a mensagem sugerida para cópia rápida."""
            
            try:
                # Inicializa o modelo Gemini mais rápido e eficiente para esta tarefa
                model = genai.GenerativeModel('gemini-2.5-flash', system_instruction=system_instruction)
                
                # Executa a chamada
                response = model.generate_content(f"Analise este rascunho: '{draft}'")
                
                # Exibe o resultado
                st.success("Análise concluída!")
                st.markdown("### Parecer e Sugestão")
                st.info(response.text)
                
            except Exception as e:
                st.error(f"Ocorreu um erro na comunicação com a IA: {e}")
