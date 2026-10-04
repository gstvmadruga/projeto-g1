import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(
    page_title="Análise de Redes Sociais no Brasil",
    page_icon="📊",
    layout="wide"
)

# Título do dashboard
st.title("📊 Análise de Redes Sociais no Brasil")

st.write(
    "Análise de dados de redes sociais brasileiras, "
    "comparando plataformas, perfis, categorias e tipos de conteúdo."
)

# Informações do projeto
st.markdown("""
**Disciplina:** Linguagem de Programação — Análise e Visualização de Dados com Python  
**Professor:** Alexandre Neves Louzada  
**Aluno:** Gustavo de Madruga Maciel
""")


# Carregamento dos dados pelo banco SQLite
from sqlalchemy import create_engine

engine = create_engine("sqlite:///database/redes_sociais.db")

df = pd.read_sql("SELECT * FROM publicacoes", engine)


# Filtros
st.subheader("🔎 Filtros")

col1, col2, col3 = st.columns(3)

with col1:
    plataforma = st.selectbox(
        "Plataforma",
        ["Todas"] + sorted(df["plataforma"].unique().tolist())
    )

with col2:
    perfil = st.selectbox(
        "Perfil",
        ["Todos"] + sorted(df["perfil"].unique().tolist())
    )

with col3:
    categoria = st.selectbox(
        "Categoria",
        ["Todas"] + sorted(df["categoria"].unique().tolist())
    )


# Aplicação dos filtros
df_filtrado = df.copy()

if plataforma != "Todas":
    df_filtrado = df_filtrado[df_filtrado["plataforma"] == plataforma]

if perfil != "Todos":
    df_filtrado = df_filtrado[df_filtrado["perfil"] == perfil]

if categoria != "Todas":
    df_filtrado = df_filtrado[df_filtrado["categoria"] == categoria]


# KPIs principais
st.subheader("📌 Indicadores Principais")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Publicações", len(df_filtrado))
col2.metric("Seguidores", f"{df_filtrado['seguidores'].sum():,.0f}")
col3.metric("Visualizações", f"{df_filtrado['visualizacoes'].sum():,.0f}")
col4.metric("Engajamento médio", f"{df_filtrado['taxa_engajamento'].mean():.2f}%")


# Gráfico de engajamento por plataforma
st.subheader("📊 Taxa Média de Engajamento por Plataforma")

engajamento_plataforma = (
    df_filtrado.groupby("plataforma")["taxa_engajamento"]
    .mean()
    .sort_values(ascending=False)
)

st.bar_chart(engajamento_plataforma)

# Gráfico de evolução do engajamento
st.subheader("📈 Evolução da Taxa Média de Engajamento")

engajamento_ano = (
    df_filtrado.groupby("ano")["taxa_engajamento"]
    .mean()
)

st.line_chart(engajamento_ano)

# Gráfico de relação entre seguidores e engajamento
st.subheader("🔵 Relação entre Seguidores e Taxa de Engajamento")

st.scatter_chart(
    df_filtrado,
    x="seguidores",
    y="taxa_engajamento"
)


# Tabela de dados
st.subheader("📋 Dados das publicações")

st.dataframe(
    df_filtrado,
    use_container_width=True
)

# Interpretação dos resultados
st.subheader("📝 Interpretação dos resultados")

st.write(
    "Os resultados apresentados permitem comparar o desempenho das publicações "
    "de acordo com os filtros selecionados. A taxa de engajamento possibilita "
    "avaliar o desempenho das diferentes plataformas, enquanto a análise ao "
    "longo dos anos permite observar mudanças no comportamento das publicações. "
    "A relação entre seguidores e engajamento também auxilia na identificação "
    "de padrões nos dados."
)

# Conclusão executiva
st.subheader("🎯 Conclusão")

st.write(
    "A análise dos dados demonstra a importância do acompanhamento das métricas "
    "de desempenho das redes sociais. Os filtros, indicadores e visualizações "
    "permitem comparar diferentes plataformas, perfis e categorias de conteúdo, "
    "facilitando a identificação de padrões de engajamento. Dessa forma, o "
    "dashboard oferece uma visão geral dos resultados e auxilia na interpretação "
    "dos dados para apoiar decisões relacionadas às publicações."
)