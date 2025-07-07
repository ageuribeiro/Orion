from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)  # Libera o acesso de domínios externos (como o frontend separado)

# Função auxiliar para verificar usuário
def verificar_usuario(email, senha):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    print("Verificando no banco de dados:", email, senha)
    cursor.execute("SELECT * FROM usuarios WHERE email=? AND senha=?", (email, senha))
    user = cursor.fetchone()
    conn.close()
    return user is not None
@app.route('/', methods=['GET'])
def home():
    return jsonify({'message':'API está funcionando corretamente!'})


@app.route('/api/login', methods=['POST'])
def login():
    dados = request.get_json()
    email = dados.get('email')
    senha = dados.get('senha')

    print("Recebidos do frontend:", email, senha)
    if verificar_usuario(email, senha):
        return jsonify({'status': 'sucesso'})
    else:
        return jsonify({'status': 'erro', 'mensagem': 'Credenciais inválidas'}), 401

if __name__ == '__main__':
    app.run(debug=True)
