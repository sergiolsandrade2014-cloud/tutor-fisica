import streamlit as st
from groq import Groq

st.set_page_config(page_title="Tutor Virtual de Física", page_icon="⚡", layout="centered")

st.title("⚡ Tutor Virtual de Física")
st.caption("Assistente interativo de Cinemática para o Ensino Médio e EJA")

with st.sidebar:
    st.header("Configuração")
    api_key = st.text_input("Cole sua Chave Groq (começa com gsk_):", type="password")
    
    st.markdown("---")
    st.markdown("### 📌 Como obter a chave grátis:")
    st.markdown("1. Acesse [console.groq.com/keys](https://console.groq.com/keys).")
    st.markdown("2. Clique em **Create API Key**.")
    st.markdown("3. Copie a chave que começa com **gsk_** e cole acima.")

SYSTEM_INSTRUCTION = """
Você é um tutor de Física amigável, paciente e dedicado a estudantes do Ensino Médio e EJA.
Seu foco exclusivo é o ensino de Cinemática (movimento, velocidade, aceleração, deslocamento, tempo).

Diretrizes Pedagógicas:
1. Adote o Método Socrático: NÃO dê respostas diretas ou fórmulas prontas de imediato. Faça perguntas guiadas para ajudar o estudante a construir o raciocínio.
2. Use contextos reais do dia a dia (carros, viagens de ônibus, caminhadas, trânsito).
3. Use linguagem simples, direta e encorajadora.
4. Mantenha respostas curtas e focadas em apenas um passo por vez.
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Digite sua dúvida sobre velocidade ou movimento..."):
    chave_limpa = api_key.strip() if api_key else ""
    
    if not chave_limpa or not chave_limpa.startswith("gsk_"):
        st.error("⚠️ Chave inválida! A chave da Groq deve começar com 'gsk_'. Verifique a barra lateral.")
    else:
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        try:
            client = Groq(api_key=chave_limpa)

            groq_messages = [{"role": "system", "content": SYSTEM_INSTRUCTION}]
            for msg in st.session_state.messages:
                role = "assistant" if msg["role"] == "assistant" else "user"
                groq_messages.append({"role": role, "content": msg["content"]})

            with st.spinner("O Tutor está pensando..."):
                completion = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=groq_messages,
                    temperature=0.7,
                )
                resposta = completion.choices[0].message.content

            st.chat_message("assistant").markdown(resposta)
            st.session_state.messages.append({"role": "assistant", "content": resposta})

        except Exception as e:
            st.error(f"⚠️ Erro ao conectar com a Groq: {e}")
