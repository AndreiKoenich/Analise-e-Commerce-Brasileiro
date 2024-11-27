import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Carregar dados simulados (substitua com seus próprios dados)
def load_data():
    data = {
        'Produto': ['Produto A', 'Produto B', 'Produto C', 'Produto D', 'Produto E'],
        'Categoria': ['Eletrônicos', 'Roupas', 'Eletrônicos', 'Beleza', 'Roupas'],
        'Vendas': [5000, 3000, 4500, 2000, 4000],
        'Avaliação Média': [4.2, 3.8, 4.5, 4.0, 3.9],
        'Data de Venda': ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04', '2024-01-05']
    }
    return pd.DataFrame(data)

def start_dashboard(engine):
    # Carregar dados
    df = load_data()

    # Título do Dashboard
    st.title("Análise de Tendências no E-commerce Brasileiro")

    # Descrição
    st.write("""
    Este dashboard apresenta algumas análises preliminares de vendas e avaliações de produtos no e-commerce brasileiro.
    Acompanhe o desempenho de vendas por categoria, produtos mais vendidos e análise de avaliações.
    """)

    # Seção 1: Total de Vendas por Categoria
    st.header("Total de Vendas por Categoria")

    # Calcular total de vendas por categoria
    vendas_categoria = df.groupby('Categoria')['Vendas'].sum().reset_index()

    # Exibir gráfico
    fig, ax = plt.subplots()
    sns.barplot(x='Vendas', y='Categoria', data=vendas_categoria, ax=ax, hue='Categoria', palette='viridis', legend=False)
    ax.set_title('Total de Vendas por Categoria')
    ax.set_xlabel('Categoria')
    ax.set_ylabel('Vendas')
    st.pyplot(fig)

    # Seção 2: Produtos Mais Vendidos
    st.header("Produtos Mais Vendidos")

    # Exibir tabela com os produtos mais vendidos
    produtos_mais_vendidos = df.sort_values(by='Vendas', ascending=False).head(5)
    st.write(produtos_mais_vendidos[['Produto', 'Vendas']])

    # Seção 3: Avaliação Média dos Produtos
    st.header("Avaliação Média dos Produtos")

    # Calcular e exibir gráfico de avaliação média
    fig, ax = plt.subplots()
    sns.barplot(x='Avaliação Média', y='Produto', data=df, ax=ax, hue='Produto', palette='Blues', legend=False)
    ax.set_title('Avaliação Média dos Produtos')
    ax.set_xlabel('Produto')
    ax.set_ylabel('Avaliação Média')
    st.pyplot(fig)

    # Seção 4: Tendência de Vendas ao Longo do Tempo
    st.header("Tendência de Vendas ao Longo do Tempo")

    # Converter a coluna "Data de Venda" para datetime
    df['Data de Venda'] = pd.to_datetime(df['Data de Venda'])

    # Calcular total de vendas por data
    vendas_diarias = df.groupby('Data de Venda')['Vendas'].sum().reset_index()

    # Exibir gráfico de vendas diárias
    fig, ax = plt.subplots()
    sns.lineplot(x='Data de Venda', y='Vendas', data=vendas_diarias, ax=ax)
    ax.set_title('Vendas Diárias ao Longo do Tempo')
    ax.set_xlabel('Data')
    ax.set_ylabel('Vendas')
    st.pyplot(fig)

    # Adicionar interatividade para o usuário
    st.sidebar.header("Filtros de Análise")
    categoria_selecionada = st.sidebar.selectbox("Selecione uma categoria", df['Categoria'].unique())

    # Filtro de categoria
    df_filtrado = df[df['Categoria'] == categoria_selecionada]
    st.write(f"Analisando produtos da categoria: {categoria_selecionada}")
    st.write(df_filtrado[['Produto', 'Vendas', 'Avaliação Média']])

    print('Dashboard inicializada com sucesso.')