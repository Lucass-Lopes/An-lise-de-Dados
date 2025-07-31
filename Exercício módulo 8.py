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

# Gráfico de Barras: Quantidade Vendida por Categoria
bar_fig = px.bar(
    df.groupby("Categoria")["Qtd_Vendidos"].sum().reset_index(),
    x='Categoria', y='Qtd_Vendidos',
    title='Total de Vendas por Categoria',
    labels={'Qtd_Vendidos': 'Total Vendido'}
)

# Gráfico de Pizza: Participação nas Vendas por Categoria
pizza_fig = px.pie(
    df, names='Categoria', values='Qtd_Vendidos',
    title='Distribuição de Vendas por Categoria'
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
