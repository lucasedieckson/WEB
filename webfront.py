from flask import Flask, render_template
#from flask_sqlalchemy import SQLAlchemy
import plotly.graph_objs as go

app = Flask(__name__)

# Configuração do banco de dados SQLite
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///relatorio.db'
#db = SQLAlchemy(app)

dados = pd.read_csv('dados.csv')

# Definição do modelo de dados do relatório
class Dado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    categoria = db.Column(db.String(50), nullable=False)
    valor = db.Column(db.Float, nullable=False)

# Rota para a página inicial do relatório
@app.route('/')
def index():
    # Recuperar os dados do banco de dados
    dados = Dado.query.all()

    # Preparar os dados para o gráfico
    categorias = [d.categoria for d in dados]
    valores = [d.valor for d in dados]

    # Criar o gráfico de barras
    grafico = go.Bar(x=categorias, y=valores)

    # Layout do gráfico
    layout = go.Layout(title='Relatório',
                       xaxis=dict(title='Categoria'),
                       yaxis=dict(title='Valor'))

    # Criar a figura
    figura = go.Figure(data=[grafico], layout=layout)

    # Converter a figura para JSON
    grafico_json = figura.to_json()

    return render_template('index.html', grafico_json=grafico_json)

if __name__ == '__main__':
    db.create_all()  # Criar as tabelas do banco de dados se não existirem
    app.run(debug=True)
