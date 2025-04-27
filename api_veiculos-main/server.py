# pip install flask flask-sqlalchemy flask_cors

from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

# Inicializa o Flask e o SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
db = SQLAlchemy(app)

# Configura o CORS
CORS(app, origins=['http://127.0.0.1:5500'])

# Classe que representa entidade no banco de dados: Veiculo
class Veiculo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    marca = db.Column(db.String(80), nullable=False)
    modelo = db.Column(db.String(80), nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    preco = db.Column(db.Float, nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'marca': self.marca,
            'modelo': self.modelo,
            'ano': self.ano,
            'preco': self.preco,
        }

# Cria a tabela no banco de dados
with app.app_context():
    db.create_all()

# Rota para listar todos os veículos
@app.route('/veiculos', methods=['GET'])
def get_veiculos():
    veiculos = Veiculo.query.all()
    return jsonify([veiculo.serialize() for veiculo in veiculos])

# Rota para listar um veículo específico
@app.route('/veiculos/<int:veiculo_id>', methods=['GET'])
def get_veiculo(veiculo_id):
    veiculo = Veiculo.query.get(veiculo_id)
    if veiculo is None:
        return jsonify({'mensagem': 'Veículo não encontrado'}), 404
    return jsonify(veiculo.serialize())

# Rota para criar um novo veículo
@app.route('/veiculos', methods=['POST'])
def create_veiculo():
    dados = request.get_json()
    novo_veiculo = Veiculo(
        marca=dados['marca'],
        modelo=dados['modelo'],
        ano=dados['ano'],
        preco=dados['preco']
    )
    db.session.add(novo_veiculo)
    db.session.commit()
    return jsonify(novo_veiculo.serialize()), 201

# Rota para atualizar um veículo
@app.route('/veiculos/<int:veiculo_id>', methods=['PUT'])
def update_veiculo(veiculo_id):
    dados = request.get_json()
    veiculo = Veiculo.query.get(veiculo_id)
    if veiculo is None:
        return jsonify({'mensagem': 'Veículo não encontrado'}), 404
    veiculo.marca = dados['marca']
    veiculo.modelo = dados['modelo']
    veiculo.ano = dados['ano']
    veiculo.preco = dados['preco']
    db.session.commit()
    return jsonify(veiculo.serialize())

# Rota para deletar um veículo
@app.route('/veiculos/<int:veiculo_id>', methods=['DELETE'])
def delete_veiculo(veiculo_id):
    veiculo = Veiculo.query.get(veiculo_id)
    if veiculo is None:
        return jsonify({'mensagem': 'Veículo não encontrado'}), 404
    db.session.delete(veiculo)
    db.session.commit()
    return jsonify({'mensagem': 'Veículo excluído com sucesso'}), 200

# Rota para documentação (opcional)
#@app.route('/')
#def serve_documentation():
#    return send_file('docAPIVeiculo.html')

if __name__ == '__main__':
    app.run(debug=True)
