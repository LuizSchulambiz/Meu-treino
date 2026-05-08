import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os

# 1. AJUSTE DE FUSO HORÁRIO (Brasília/Betim)
data_hoje = (datetime.now() - timedelta(hours=3)).date()

st.set_page_config(page_title="Treino Águia Pro", layout="centered")

# Estilização Águia (Preto, Azul Escuro e Dourado)
st.markdown(f"""
    <style>
    .main {{ background-color: #000000; color: #ffffff; }}
    .stButton>button {{ background-color: #D4AF37; color: #000000; font-weight: bold; width: 100%; border-radius: 8px; border: none; height: 3em; }}
    .stCheckbox {{ color: #ffffff; margin-bottom: 0px; }}
    .ex-desc {{ color: #999999; font-size: 0.85rem; font-style: italic; margin-bottom: 20px; margin-left: 28px; line-height: 1.3; }}
    h1, h2, h3 {{ color: #002366; font-family: 'Arial Black', sans-serif; }}
    .stExpander {{ border: 1px solid #002366; border-radius: 8px; background-color: #0a0a0a; margin-bottom: 10px; }}
    </style>
    """, unsafe_allow_html=True)

st.title("🦅 Painel de Treino Águia")
st.write(f"Registro de: **{data_hoje.strftime('%d/%m/%Y')}**")

# 2. BANCO DE DADOS COM AS DESCRIÇÕES COMPLETAS DA PLANILHA
exercicios_dict = {
    "🚀 Aquecimento (Pré-Pedal)": {
        "Rotação de Pescoço": "Gire a cabeça lentamente 5 vezes para cada lado.",
        "Círculos com os Ombros": "Gire os ombros para trás e para baixo 10 vezes.",
        "Rotação de Quadril": "Com as mãos na cintura, faça círculos grandes com o quadril (5x cada lado).",
        "Balanço de Pernas": "Apoie em algo e balance uma perna para frente e para trás (10x cada perna).",
        "Rotação de Tornozelos": "Gire cada pé 10 vezes para cada lado."
    },
    "💪 Fortalecimento (Motor das Pernas)": {
        "Agachamento": "Com os pés na largura dos ombros, desça o quadril como se fosse sentar em uma cadeira invisível. Mantenha as costas retas e o peso nos calcanhares.",
        "Afundo (Passada)": "Dê um passo largo à frente e desça o joelho de trás em direção ao chão, formando um ângulo de 90 graus com ambas as pernas. Alterne os lados.",
        "Prancha Abdominal": "Apoie os antebraços e as pontas dos pés no chão. Mantenha o corpo alinhado (sem subir ou descer o quadril) pelo máximo de tempo que conseguir.",
        "Elevação de Gêmeos": "Fique na ponta dos pés e desça lentamente. Pode ser feito no degrau de uma escada para aumentar a amplitude do movimento.",
        "Ponte (Elevação Pélvica)": "Deitado de costas, dobre os joelhos e suba o quadril em direção ao teto, contraindo bem os glúteos no topo."
    },
    "🧘 Alongamentos de Alívio (Pós-Pedal)": {
        "Psoas (Quadril)": "Ajoelhe-se em um pé só e projete o quadril para frente, sentindo alongar a frente da coxa da perna que está com o joelho no chão.",
        "Posteriores": "Sentado no chão ou em pé, tente tocar as pontas dos pés com as pernas bem esticadas, mantendo a posição por 30 segundos.",
        "Peitoral no Portal": "Apoie o antebraço no batente de uma porta e gire o corpo suavemente para o lado oposto, abrindo bem o tórax.",
        "Cervical Lateral": "Puxe levemente a cabeça em direção ao ombro, mantendo o braço oposto relaxado ou esticado para baixo para aumentar o alívio.",
        "Recolhimento de Queixo": "Puxe o queixo para trás (fazendo 'papada') sem inclinar a cabeça para cima ou para baixo. Segure 3 segundos e relaxe.",
        "Giro de Tornozelo": "Gire os pés em círculos, nos dois sentidos, para soltar a articulação que recebe a pressão do pedal."
    }
}

# 3. CARREGAR HISTÓRICO
def carregar_dados():
    if os.path.exists("historico_treino.csv"):
        try:
            df = pd.read_csv("historico_treino.csv")
            df['Data'] = pd.to_datetime(df['Data']).dt.date
            return df
        except:
            return pd.DataFrame(columns=["Data", "Exercicio", "Status"])
    return pd.DataFrame(columns=["Data", "Exercicio", "Status"])

df_historico = carregar_dados()

# Verificar o que já foi concluído hoje
feitos_hoje = df_historico[(df_historico['Data'] == data_hoje) & (df_historico['Status'] == "Concluído")]['Exercicio'].tolist()

# 4. INTERFACE
st.subheader("O que concluímos hoje?")
progresso_atual = []

for categoria, itens in exercicios_dict.items():
    with st.expander(categoria):
        for ex, desc in itens.items():
            # Checkbox já vem marcado se você já salvou antes no mesmo dia
            foi_feito = ex in feitos_hoje
            check = st.checkbox(ex, value=foi_feito, key=f"chk_{ex}")
            
            # Texto explicativo detalhado
            st.markdown(f'<div class="ex-desc">{desc}</div>', unsafe_allow_html=True)
            
            status = "Concluído" if check else "Pendente"
            progresso_atual.append({"Data": data_hoje, "Exercicio": ex, "Status": status})

# 5. BOTÃO DE SALVAR (Substitui os dados de hoje, sem duplicar)
if st.button("SALVAR PROGRESSO ATUAL"):
    df_novo_hoje = pd.DataFrame(progresso_atual)
    df_sem_hoje = df_historico[df_historico['Data'] != data_hoje]
    df_final = pd.concat([df_sem_hoje, df_novo_hoje], ignore_index=True)
    
    df_final.to_csv("historico_treino.csv", index=False)
    st.success(f"✅ Atualizado com sucesso! (Último registro: {datetime.now().strftime('%H:%M')})")
    st.rerun()

# 6. HISTÓRICO DETALHADO
st.markdown("---")
if st.checkbox("📊 Ver Mapa de Disciplina"):
    if not df_historico.empty:
        st.write("Histórico dos últimos 7 dias de treino:")
        
        # Filtra apenas os exercícios do nosso dicionário
        lista_validos = [ex for cat in exercicios_dict.values() for ex in cat.keys()]
        df_view = df_historico[df_historico['Exercicio'].isin(lista_validos)]
        
        # Cria a tabela cruzada (Data x Exercício)
        pivot_df = df_view.pivot_table(index='Data', columns='Exercicio', values='Status', aggfunc='first')
        
        # Exibe a tabela (você pode arrastar para os lados no celular)
        st.dataframe(pivot_df.tail(7), use_container_width=True)
        
        # Resumo rápido
        concluidos = sum(1 for p in progresso_atual if p['Status'] == 'Concluído')
        st.info(f"Hoje você completou {concluidos} de {len(progresso_atual)} exercícios.")
    else:
        st.info("O histórico aparecerá aqui após o primeiro uso.")