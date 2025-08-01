import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px

# Função para converter strings como '+10mil' em números, sei que existem outras formas de fazer o mesmo.
def texto_para_num(valor):
    if isinstance(valor, str):
        valor = valor.lower().replace('+', '').strip()
        if 'mil' in valor:
            valor = valor.replace('mil', '').strip()
            try:
                return float(valor) * 1000
            except:
                return None
        else:
            try:
                return float(valor)
            except:
                return None
    return valor

# Carregamento dos dados
df = pd.read_csv("ecommerce_estatistica.csv")

# Aplica a limpeza na coluna 'Qtd_Vendidos' com a função criada
df['Qtd_Vendidos'] = df['Qtd_Vendidos'].apply(texto_para_num)

# Remove valores ausentes e inválidos
df.dropna(inplace=True)

# Limpa e converte os preços para float
df['Preço'] = (
    df['Preço']
    .astype(str)
    .str.replace(r'[R$\s]', '', regex=True)
    .str.replace('.', '', regex=False)
    .str.replace(',', '.', regex=False)
    .astype(float)
)

# Criação de faixas de preço para organizar melhor as filtrações por ele
bins = [0, 50, 100, 200, 500, 1000, float('inf')]
labels = ['Até R$50', 'R$50–100', 'R$100–200', 'R$200–500', 'R$500–1000', 'Mais de R$1000']
df['Faixa_Preco'] = pd.cut(df['Preço'], bins=bins, labels=labels, include_lowest=True)

# Inicializa a aplicação Dash
app = dash.Dash(__name__)
app.title = "Análise de E-commerce"

# Gráfico de Dispersão: Avaliações vs Quantidade Vendida
scatter_fig = px.scatter(
    df, x='N_Avaliações', y='Qtd_Vendidos',
    title='Dispersão: Avaliações vs Quantidade Vendida',
    labels={'N_Avaliações': 'Número de Avaliações', 'Qtd_Vendidos': 'Quantidade Vendida'}
)

# Gráfico de Regressão: Nota Média vs Quantidade Vendida
reg_fig = px.scatter(
    df, x='Nota', y='Qtd_Vendidos', trendline='ols',
    title='Regressão: Nota vs Quantidade Vendida',
    labels={'Nota': 'Nota Média', 'Qtd_Vendidos': 'Quantidade Vendida'}
)

# Gráfico de Barras: Quantidade Vendida por Preço
bar_fig = px.bar(
    df.groupby("Faixa_Preco")["Qtd_Vendidos"].sum().reset_index(),
    x='Faixa_Preco', y='Qtd_Vendidos',
    title='Total de Vendas por Faixa de Preço',
    labels={'Faixa_Preco': 'Faixa de Preço', 'Qtd_Vendidos': 'Total Vendido'}
)

# Gráfico de Pizza: Quantidade Vendida por material
pizza_fig = px.pie(
    df.groupby("Material")["Qtd_Vendidos"].sum().reset_index(),
    names='Material', values='Qtd_Vendidos',
    title='Distribuição de Vendas por Material'
)
# Gráfico de Densidade: Distribuição da Nota Média
density_fig = px.histogram(
    df, x='Nota', nbins=20, marginal='rug',
    title='Distribuição da Nota Média',
    labels ={'Nota' : 'Nota'}
)

# Layout da aplicação
app.layout = html.Div([
    html.H1("Dashboard de E-commerce", style={'textAlign': 'center'}),

    dcc.Graph(figure=scatter_fig),
    dcc.Graph(figure=reg_fig),
    dcc.Graph(figure=bar_fig),
    dcc.Graph(figure=pizza_fig),
    dcc.Graph(figure=density_fig)
])

# Executa o servidor
if __name__ == '__main__':
    app.run_server(debug=True)

