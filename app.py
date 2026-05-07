import streamlit as st
import pandas as pd
from datetime import date

# Configuração da Página com sua Identidade Visual
st.set_page_config(page_title="Meu Treino Bike", layout="centered")

# CSS para aplicar as cores: Preto, Azul Escuro e Dourado
st.markdown("""
    <style>
    .main { background-color: #000000; color: #ffffff; }
    .stButton>button { background-color: #D4AF37; color: #000000; font-weight: bold; width: 100%; border-radius: 8px; }
    .stCheckbox { color: #ffffff; margin-bottom: 0px; }
    .ex-desc { color: #999999; font-size: 0.85rem; font-style: italic; margin-bottom: 18px; margin-left: 28px; line-height: 1.2; }
    h1, h2, h3 { color: #002366; font-family: 'Arial Black', sans-serif; } /* Azul Escuro */
    .stExpander { border: 1px solid #002366; border-radius: 8px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚲 Treino Luiz")
st.write(f"Registro de: **{date.today().strftime('%d/%m/%Y')}**")

# Dicionário Completo baseado na sua Planilha
exercicios = {
    "🚀 Aquecimento (Pré-Pedal)": {
        "Rotação de Pescoço": "Gire a cabeça lentamente 5 vezes para cada lado.",
        "Círculos com os Ombros": "Gire os ombros para trás e para baixo 10 vezes.",
        "Rotação de Quadril": "Com as mãos na cintura, faça círculos grandes com o quadril (5x cada lado).",
        "Balanço de Pernas": "Apoie em algo e balance uma perna para frente e para trás (10x cada perna).",
        "Rotação de Tornozelos": "Gire cada pé 10 vezes para cada lado."
    },
    "💪 Fortalecimento (Motor das Pernas)": {
        "Agachamento": "Pés na largura dos ombros, desça o quadril como se fosse sentar em uma cadeira invisível. Peso nos calcanhares.",
        "Afundo (Passada)": "Dê um passo largo à frente e desça o joelho de trás em direção ao chão (90 graus). Alterne os lados.",
        "Prancha Abdominal": "Apoie antebraços e pontas dos pés. Mantenha o corpo alinhado sem subir ou descer o quadril.",
        "Elevação de Gêmeos": "Fique na ponta dos pés e desça lentamente. Use um degrau para maior amplitude.",
        "Ponte (Elevação Pélvica)": "Deitado de costas, dobre os joelhos e suba o quadril contraindo bem os glúteos no topo."
    },
    "🧘 Alívio (Pós-Pedal)": {
        "Psoas (Quadril)": "Ajoelhe em um pé só e projete o quadril para frente, alongando a frente da coxa.",
        "Posteriores": "Tente tocar as pontas dos pés com as pernas esticadas. Segure por 30 segundos.",
        "Peitoral no Portal": "Apoie o antebraço no batente da porta e gire o corpo para o lado oposto.",
        "Cervical Lateral": "Puxe a cabeça levemente para o ombro, mantendo o braço oposto relaxado.",
        "Recolhimento de Queixo": "Puxe o queixo para trás (fazendo 'papada') por 3 segundos para alinhar a coluna.",
        "Giro de Tornozelo": "Gire os pés em círculos para soltar a articulação após a pressão do pedal."
    }
}

# Interface de Progresso
st.subheader("O que concluímos hoje?")
progresso_hoje = []

for categoria, lista_ex in exercicios.items():
    with st.expander(categoria):
        for ex, desc in lista_ex.items():
            if st.checkbox(ex, key=f"{categoria}_{ex}"):
                progresso_hoje.append({"Data": date.today(), "Exercicio": ex, "Status": "Concluído"})
            st.markdown(f'<div class="ex-desc">{desc}</div>', unsafe_allow_html=True)

# Lógica para Salvar
if st.button("SALVAR TREINO DE HOJE"):
    if progresso_hoje:
        df_novo = pd.DataFrame(progresso_hoje)
        try:
            df_antigo = pd.read_csv("historico_treino.csv")
            df_final = pd.concat([df_antigo, df_novo], ignore_index=True)
        except FileNotFoundError:
            df_final = df_novo
        
        df_final.to_csv("historico_treino.csv", index=False)
        st.success("✅ Tudo pronto! Histórico atualizado.")
    else:
        st.warning("⚠️ Selecione os exercícios feitos antes de salvar.")

# Gráfico simples de consistência
if st.checkbox("Mostrar meu Histórico"):
    try:
        hist = pd.read_csv("historico_treino.csv")
        st.dataframe(hist.tail(15), use_container_width=True)
    except:
        st.info("O seu histórico começará a aparecer aqui após o primeiro salvamento.")