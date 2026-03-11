import streamlit as st
import google.generativeai as genai

# Configuração da página para uso em mobile pelos supervisores
st.set_page_config(page_title="Revisor de Mensagens", page_icon="🛡️", layout="centered")

st.title("🛡️ Revisor de Mensagens")
st.markdown("Evite passivos laborais. A IA analisará o risco e sugerirá uma versão profissional e segura da sua mensagem antes do envio pelo WhatsApp.")

# Resgate seguro da Chave API (invisível no código)
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except KeyError:
    st.error("Erro de configuração: Chave de API não encontrada nos Secrets.")
    st.stop()

st.markdown("---")
st.subheader("Como deseja enviar o relato?")

# Abas para separar a digitação da gravação de áudio (interface mais limpa no celular)
tab1, tab2 = st.tabs(["🎙️ Gravar Áudio", "✍️ Digitar Texto"])

with tab1:
    st.info("Clique no microfone para relatar o que aconteceu. A IA vai ouvir, transcrever e corrigir.")
    audio_gravado = st.audio_input("Gravar relato")

with tab2:
    draft = st.text_area(
        "Digite o texto aqui:", 
        height=120, 
        placeholder="Ex: Ó João, tens de vir aqui limpar a unidade a correr senão dou-te uma advertência e corto-te o dia...",
        label_visibility="collapsed"
    )

st.markdown("---")

# Processamento
if st.button("Rever Mensagem ✨", type="primary", use_container_width=True):
    
    # Verifica se tem áudio ou texto
    if audio_gravado is None and not draft.strip():
        st.warning("⚠️ Por favor, grave um áudio ou digite um texto para análise.")
        st.stop()
        
    with st.spinner("A processar a sua mensagem com o departamento jurídico virtual..."):
        
        # Instruções de Sistema atualizadas para lidar com áudio e texto
        system_instruction = """Você é um Advogado Trabalhista Especialista em empresas de prestação de serviços e gestão de contratos públicos. 
        O utilizador é um supervisor de campo que está enviando um relato (por texto ou áudio) sobre uma situação com um funcionário.
        
        Sua tarefa:
        1. Se for um áudio, comece apresentando a TRANSCRIÇÃO EXATA do que o supervisor falou.
        2. Definir o Nível de Risco Trabalhista (Alto, Médio, Baixo) do relato original.
        3. Apontar de forma direta e concisa o erro na abordagem do supervisor.
        4. Fornecer uma sugestão de reescrita profissional, polida, assertiva e juridicamente segura para ele copiar e colar no WhatsApp do funcionário.
        
        Formate a resposta em Markdown claro, destacando a mensagem sugerida para cópia rápida."""
        
        try:
            # Inicializa o modelo Gemini
            model = genai.GenerativeModel('gemini-2.5-flash', system_instruction=system_instruction)
            
            # Se o supervisor gravou um áudio, enviamos o pacote de áudio
            if audio_gravado is not None:
                pacote_audio = {
                    "mime_type": "audio/wav",
                    "data": audio_gravado.getvalue()
                }
                response = model.generate_content(["Analise este relato em áudio:", pacote_audio])
            
            # Se não tem áudio, enviamos o texto digitado
            else:
                response = model.generate_content(f"Analise este rascunho: '{draft}'")
            
            # Exibe o resultado
            st.success("Análise concluída!")
            st.markdown("### Parecer e Mensagem Sugerida")
            st.info(response.text)
            
        except Exception as e:
            st.error(f"Ocorreu um erro na comunicação com a IA: {e}")
