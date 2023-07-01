import requests 
import json
import pdfkit 
import datetime
import os
import firebase_admin
import string
import firebase_admin
from flask import Flask, render_template, request, redirect, flash, url_for, session
from firebase_admin import auth, credentials
from flask_session import Session
from datetime import timedelta



app = Flask(__name__)
app.secret_key = 'secret'
app.config['UPLOAD_FOLDER'] = 'files'
app.config['SESSION_TYPE'] ='filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USER_SIGNER'] = True
app.config['SESSION_COOKIE_SECURE'] = True
app.config['PERMANET_SESSION_LIFETIME'] = timedelta(minutes=5)

Session(app)

config ={
    'apiKey': "AIzaSyCuATOltNI_Vxu_ucfzXPNmN2V1puvqABU",
    'authDomain': "appweb-orion-php.firebaseapp.com",
    'databaseURL': "https://appweb-orion-php-default-rtdb.firebaseio.com",
    'projectId': "appweb-orion-php",
    'storageBucket': "appweb-orion-php.appspot.com",
    'messagingSenderId': "365589111987",
    'appId': "1:365589111987:web:cc51e2470cbe43ec40fcc6"
}

cred = credentials.Certificate('Git/key/credencial.json')
firebase = firebase_admin.initialize_app(cred)
auth = firebase.auth()

app.secret_key = 'secret'

# URL do banco de dados do firebase
firebase_url = "https://appweb-orion-php-default-rtdb.firebaseio.com/members.json"

# ======================== Login ==============================================================================

# login session 
@app.route("/login", methods=["POST", "GET"])
def login():
    if('user' in session):
        return render_template('membros/read.html')
        gretting = 'Hi, {}'.format(session['user'])

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        try:
            # Autentique o usuário com o Firebase Authentication
            user = auth.sign_in_with_email_and_password(email, password)
            session['user'] = email

            flash("Login realizado com sucesso.","success")
            return redirect(url_for("index"))
    
        except:
            # Trate os erros de autenticação do Firebase
            flash("Failed to login. Try again later.", "danger")

    return render_template("index.html")

# logout session    
@app.route("/logout")
def logout():
    session.pop('user')
    session.clear()
    return redirect(url_for("index"))

#============================ Funções de configuração ===========================================================================================

# gerar id automaticamente
def generate_id():
    characters = string.ascii_uppercase + string.digits
    id = ''.join(random.choices(characters, k=16))
    return id

# verificar se o id gerado já existe
def check_id_exists(id):
    # Fazer a solicitação GET para obter os daods do nó "members"
    response = requests.get(f'{firebase_url}/members.json')

    if response.status_code == 200:
    
        # Verificar se o id já existe no nó membros
        members = response.json()
        if members:
            for member_id in members:
                if members[member_id]['key'] == id:
                    return True
    return False

# ======================== Funções CRUD para Membros ==============================================================================
# Rota para exibir os dados
@app.route("/")
def index():
    # verificar se o usuário está autenticado
    if 'user' not in session:
        return redirect(url_for('login'))

    data = read_data()
    return render_template('index.html', data=data)

# Rota para adicionar dados
@app.route("/add", methods=['GET','POST'])
def add():
    if request.method == "POST":
        nome = request.form["nome"]
        pai = request.form["pai"]
        mae =  request.form["mae"]
        data_nasc = request.form["data_nasc"]
        estado_civil = request.form["estado_civil"]
        cpf = request.form["cpf"]
        rg = request.form["rg"]
        setor_atual = request.form["setor_atual"]
        igreja_atual = request.form["igreja_atual"]
        setor_anterior = request.form["setor_anterior"]
        igreja_anterior = request.form["igreja_anterior"]
        batizado_com_espirito_santo = request.form["batizado_com_espirito_santo"]
        escolaridade = request.form["escolaridade"]
        profissao = request.form["profissao"]
        batizado = request.form["batizado"]
        data_batismo = request.form["data_batismo"]
        igreja_de_batismo = request.form["igreja_de_batismo"]
        admitido_por = request.form["admitido_por"]
        data_da_consagracao = request.form["data_da_consagracao"]
        data_da_apresentacao = request.form["data_da_apresentacao"]
        cargo_na_igreja = request.form["cargo_na_igreja"]
        endereco = request.form["endereco"]
        bairro = request.form["bairro"]
        cidade = request.form["cidade"]
        estado = request.form["estado"]
        cep = request.form["cep"]
        telefone = request.form["telefone"]
        email = request.form["email"]
        tem_cartao = request.form["tem_cartao"]
        foto = request.files["foto"]
        id = generate_id()
        
        # Verificar se o ID já existe
        while check_id_exists(id):
            id = generate_id()

        # Salvar a imagem em um diretorio local
        # Criar diretorio com nome do membro
        nome_less = nome.replace(" ","")
        dir_membro = os.path.join('static', 'files', nome_less) 
        os.makedirs(dir_membro, exist_ok=True)

        # Salvar Imagem
        imagem_path = os.path.join(dir_membro, nome_less + '.png')
        foto.save(imagem_path)

        # Salvar os dados no firebase
        data = {'id':id, 'nome':nome, 'pai':pai,'mae':mae, 'data_nasc':data_nasc, 'estado_civil':estado_civil, 'cpf':cpf, 'rg':rg,'setor_atual':setor_atual, 'igreja_atual':igreja_atual, 'setor_anterior':setor_anterior, 'igreja_anterior':igreja_anterior, 'batizado_com_espirito_santo':batizado_com_espirito_santo, 'escolaridade':escolaridade, 'profissao':profissao,'batizado':batizado,'data_batismo':data_batismo, 'igreja_de_batismo':igreja_de_batismo, 'admitido_por':admitido_por, 'data_da_consagracao':data_da_consagracao, 'data_da_apresentacao':data_da_apresentacao, 'cargo_na_igreja':cargo_na_igreja, 'endereco':endereco, 'bairro':bairro, 'cidade':cidade, 'estado':estado, 'cep':cep, 'telefone':telefone, 'email':email, 'tem_cartao':tem_cartao, 'foto': imagem_path }
        create_data(data)

        # Exibir mensagem de flash
        flash("Dados cadastrados com sucesso.","success")

        # Redirecionar para a lista de membros para gerar pdf
        return redirect(url_for('index'))
    return render_template('membros/add.html')

    user_id = session.get('user_id')
    if user_id is None:
        flash("Você precisa fazer login para acessar esta página. \n\r Estamos redirecionando para a página de login.", "danger")
        
        return redirect(url_for("login"))

    return render_template("add.html", user_id = user_id)


# Rota para exibir os dados do membro e gerar o PDF
@app.route("/member/view/<string:id>")
def view_member(id):
    con = sql.connect("app_orion_database.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM members WHERE ID = ?", (id,))
    member_data = cur.fetchone()
    con.close()

    if member_data is None:
        flash("Membro não encontrado.", "danger")
        return redirect(url_for("index"))
    
    return render_template("membros/view_member.html", member_data = member_data)


# Rota para gerar PDF do membro
@app.route("/member/<string:id>/generate_pdf")
def generate_pdf(id):
    con = sql.connect("app_orion_database.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM members WHERE ID = ?", (id,))
    member_data = cur.fetchone()
    con.close()

    if member_data is None:
        flash("Membro não encontrado.", "danger")
        return redirect(url_for("list_member"))
    else:
        # Gerar o conteudo HTML no PDF
        html = render_template("membros/view_member.html", member_data = member_data)

    # Retornar o PDF utilizando o conteudo HTML
    return send_file(pdf_path, as_attachment=False)

# editar membro        
@app.route("/edit_member/<string:id>", methods=["POST", "GET"])
def edit_member(id):
    if request.method=="POST":
        nome = request.form["nome"]
        pai = request.form["pai"]
        mae =  request.form["mae"]
        data_nasc = request.form["data_nasc"]
        estado_civil = request.form["estado_civil"]
        cpf = request.form["cpf"]
        rg = request.form["rg"]
        setor_atual = request.form["setor_atual"]
        igreja_atual = request.form["igreja_atual"]
        setor_anterior = request.form["setor_anterior"]
        igreja_anterior = request.form["igreja_anterior"]
        batizado_com_espirito_santo = request.form["batizado_com_espirito_santo"]
        escolaridade = request.form["escolaridade"]
        profissao = request.form["profissao"]
        batizado = request.form["batizado"]
        data_batismo = request.form["data_batismo"]
        igreja_de_batismo = request.form["igreja_de_batismo"]
        admitido_por = request.form["admitido_por"]
        data_da_consagracao = request.form["data_da_consagracao"]
        data_da_apresentacao = request.form["data_da_apresentacao"]
        cargo_na_igreja = request.form["cargo_na_igreja"]
        endereco = request.form["endereco"]
        bairro = request.form["bairro"]
        cidade = request.form["cidade"]
        estado = request.form["estado"]
        cep = request.form["cep"]
        telefone = request.form["telefone"]
        email = request.form["email"]
        tem_cartao = request.form["tem_cartao"]
        con = sql.connect("app_orion_database.db")
        cur=con.cursor()
        cur.execute("update members set NOME = ?, PAI = ?, MAE = ?, DATA_NASC = ?, ESTADO_CIVIL = ?, CPF = ?, RG = ?, SETOR_ATUAL = ?, IGREJA_ATUAL = ?, SETOR_ANTERIOR = ?, IGREJA_ANTERIOR = ?, BATIZADO_COM_ESPIRITO_SANTO = ?, ESCOLARIDADE = ?, PROFISSAO = ?, BATIZADO_NAS_AGUAS = ?, DATA_BATISMO_NAS_AGUAS = ?, IGREJA_DE_BATISMO = ? , ADMITIDO_POR = ?, DATA_DA_CONSAGRACAO = ?, DATA_DA_APRESENTACAO = ?, CARGO_NA_IGREJA = ?, ENDERECO = ?, BAIRRO = ?, CIDADE = ?, ESTADO = ?, CEP = ?, TELEFONE = ?, EMAIL = ?, TEM_CARTAO_DE_MEMBRO = ? WHERE ID = ? ",(nome, pai, mae, data_nasc, estado_civil, cpf, rg, setor_atual, igreja_atual, setor_anterior, igreja_anterior, batizado_com_espirito_santo, escolaridade, profissao, batizado, data_batismo, igreja_de_batismo, admitido_por, data_da_consagracao, data_da_apresentacao, cargo_na_igreja, endereco, bairro, cidade, estado, cep, telefone, email, tem_cartao, id))
        con.commit()
        flash("Dados atualizados com sucesso","success")
        return redirect(url_for("list_member"))
    con = sql.connect("app_orion_database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from members where ID = ?",(id,))
    data = cur.fetchone()
    return render_template("membros/edit_member.html", datas=data)

# deletar member
@app.route("/delete_member/<string:id>", methods=["GET"])
def delete_member(id):
    con = sql.connect("app_orion_database.db")
    cur = con.cursor()
    cur.execute("delete from members WHERE ID=?", (id,))
    con.commit()
    flash("Dados deletados.","warning")
    return redirect(url_for("list_member"))

# criar relatorio do membro
@app.route("/report_member/<string:id>", methods=["GET"])
def report_member(id):
    con = sql.connect("app_orion_database.db")
    cur = con.cursor()
    cur.execute("select * from members WHERE ID=?",(id))
    con.commit()
    flash("Relatório criado com sucesso","success")
    return redirect(url_for('list_member'))


# listar relatorio do membro
@app.route("/list_report")
def list_report():
    con = sql.connect("app_orion_database.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute("select * from members")
    data=cur.fetchall()

    user_id = session.get('user_id')
    if user_id is None:
        flash("Você precisa fazer login para acessar esta página.", "danger")
        return redirect(url_for("login"))

    return render_template("membros/list_report.html", datas=data, user_id = user_id)

#============================ Funções para os métodos HTTP ===========================================================================================

# Função para criar os dados
def create_data(data):
    response = requests.post(firebase_url, json.dumps(data))
    if response.status_code != 200:
        print('Erro ao criar dados.')

# Função para ler os dados
def read_data():
    response = requests.get(firebase_url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print('Erro ao ler dados.')

# Função para atualizar dados
def update_data(key, new_data):
    url_update = f"https://appweb-orion-php-default-rtdb.firebaseio.com/members/{key}.json"
    response = requests.patch(url_update, json.dumps(new_data))
    if response.status_code != 200:
        print('Erro ao atualizar dados.')

# Função para deletar dados
def delete_data(key):
    url_delete = f"https://appweb-orion-php-default-rtdb.firebaseio.com/members/{key}.json"
    response = requests.delete(url_delete)
    if response.status_code == 200:
        print('Dados excluídos com sucesso.')
    else:
        print('Erro ao excluir dados.')


# Rota para exibir os dados do membro e gerar o PDF
@app.route("/report/<key>")
def report(key):
   return render_template("index.html")

if __name__=='__main__':
    app.run(debug=True, port=911)