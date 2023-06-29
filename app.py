from flask import Flask, render_template, request, redirect, flash, url_for, session
from firebase_admin import auth
import requests, json, pdfkit, datetime, os, firebase_admin, pyrebase

firebase_admin.initialize_app()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'files'


config ={
    'apiKey': "AIzaSyCuATOltNI_Vxu_ucfzXPNmN2V1puvqABU",
    'authDomain': "appweb-orion-php.firebaseapp.com",
    'databaseURL': "https://appweb-orion-php-default-rtdb.firebaseio.com",
    'projectId': "appweb-orion-php",
    'storageBucket': "appweb-orion-php.appspot.com",
    'messagingSenderId': "365589111987",
    'appId': "1:365589111987:web:cc51e2470cbe43ec40fcc6"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

app.secret_key = 'secret'

# URL do banco de dados do firebase
firebase_url = "https://appweb-orion-php-default-rtdb.firebaseio.com/"

member_dados = {
  "id": 0,
  "nome": "null",
  "pai": "null",
  "mae": "null",
  "data_nasc": "null",
  "estado_civil": "null",
  "cpf": "null",
  "rg": "null",
  "setor_atual": "null",
  "igreja_atual": "null",
  "setor_anterior": "null",
  "igreja_anterior": "null",
  "batizado_com_espirito_santo": "null",
  "escolaridade": "null",
  "profissao": "null",
  "batizado_nas_aguas": "null",
  "data_batismo_nas_aguas": "null",
  "igreja_de_batismo": "null",
  "admitido_por": "null",
  "data_da_consagracao": "null",
  "data_da_apresentacao": "null",
  "cargo_na_igreja": "null",
  "endereco": "null",
  "bairro": "null",
  "cidade": "null",
  "estado": "null",
  "cep": "null",
  "telefone": "null",
  "email": "null",
  "tem_cartao_de_membro": "null",
  "foto": "null"
}

# criar membro
req_create_member = requests.post(f'{firebase_url}/membros/.json', data = json.dumps(member_dados))

# index
@app.route("/")
def index():
    
    # Obter todos os usuarios do firebase
    response = requests.get(f'{firebase_url}/usuarios.json')
    users = response.json() if response.ok else {}
    return render_template("index.html", users=users)

# ======================== Login ==============================================================================

# login session 
@app.route("/login", methods=["POST", "GET"])
def login():
    if('user' in session):
        return 'Hi, {}'.format(session['user'])

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        try:
            # Autentique o usuário com o Firebase Authentication
            user = auth.sign_in_with_email_and_password(email, password)
            session['user'] = email

            flash("Login realizado com sucesso.","success")
            return redirect(url_for("list_member"))
    
        except:
            # Trate os erros de autenticação do Firebase
            flash("Failed to login. Try again later.", "danger")

    return render_template("index.html")

# logout session    
@app.route("/logout")
def logout():
    session.pop('user')
    return redirect(url_for("index"))

# ======================== Usuarios ==============================================================================

# listar usuarios
@app.route("/list_user")
def list_user():
    con = sql.connect("app_orion_database.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute("select * from users")
    data=cur.fetchall()

    user_id = session.get('user_id')
    if user_id is None:
        flash("Você precisa fazer login para acessar esta página.", "danger")
        return redirect(url_for("login"))

    return render_template("usuarios/read.html", datas=data, user_id = user_id)

# adicionar usuario
@app.route("/add_user", methods=["POST", "GET"])
def add_user():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        usuario =request.form["usuario"]
        senha = request.form["senha"]

        # Criar o objeto de usuario
        user_data = {
            "nome":nome, 
            "email":email, 
            "senha":senha
            }
        # Enviar a requisição POST para criar o usuario no Firebase
        response = requests.post(f'{firebase_url}/usuarios.json', json=user_data)

        if response.ok:
            
            return redirect(url_for('index'))
            flash("Dados cadastrados com sucesso.","success")
        else:
            return "Erro ao criar novo usuario."
    return render_template("usuarios/read.html")

# editar usuario        
@app.route("/edit_user/<string:user_id>", methods=["POST", "GET"])
def edit_user(user_id):
    
    response = requests.get(f'{firebase_url}/usuarios/{user_id}.json')
    user_data = response.json() if response.ok else {}

    if request.method == "POST":
        # Obter os dados do formulario
        nome = request.form["nome"]
        email = request.form["email"]
        usuario =request.form["usuario"]
        senha = request.form["senha"]


        # Atualizar os dados do  usuario
        user_data["nome"] = nome
        user_data["email"] = email
        user_data["usuario"] = usuario
        user_data["senha"] = senha

        # Enviar a requisição PUT para atualizar o usuario no firebase
        response = requests.put(f"{firebase_url}/usuarios/{user_id}.json", json=user_data)

        if response.ok:
            return redirect(url_for("index"))
        else:
            return "Erro ao atualizar usuário."
        
    return render_template("usuarios/update.html", user_id=user_id, user=user_data)

# deletar usuario
@app.route("/delete_user/<string:user_id>", methods=["POST"])
def delete_user(user_id):
    
    # Enviar a requisição DELETE para remover o usuaario do Firebase
    response = requests.delete(f'{firebase_url}/usuarios/{user_id}.json')

    if reponse.ok:
        return redirect(url_for("index"))
    else:
        return "Erro ao excluir usuario."
    
#============================ Membros ===========================================================================================

# listar membro
@app.route("/list_member")
def list_member():

    return render_template("membros/read.html")

#adicionar membro
@app.route("/add_member", methods=["POST", "GET"])
def add_member():
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

        # formatando a data de nascimento
        data_nascimento_format = datetime.datetime.strptime(data_nasc, "%Y-%m-%d").date()
        formatted_date_nasc = data_nascimento_format.strftime("%d/%m/%Y")

        # formatando a data de batismo
        data_batismo_format = datetime.datetime.strptime(data_batismo, "%Y-%m-%d").date()
        formatted_date_batismo = data_batismo_format.strftime("%d/%m/%Y")

        # formatando a data da consagração
        data_da_consagracao_format = datetime.datetime.strptime(data_da_consagracao, "%Y-%m-%d").date()
        formatted_data_da_consagracao = data_da_consagracao_format.strftime("%d/%m/%Y")
        
        # formatando a data da apresentação
        data_da_apresentacao_format = datetime.datetime.strptime(data_da_apresentacao, "%Y-%m-%d").date()
        formatted_data_da_apresentacao = data_da_apresentacao_format.strftime("%d/%m/%Y")

        # Criar diretorio com nome do membro
        nome_less = nome.replace(" ","")
        dir_membro = os.path.join('static','files', nome_less) 
        os.makedirs(dir_membro, exist_ok=True)

        # Salvar Imagem
        imagem_path = os.path.join(dir_membro, nome_less + '.png')
        foto.save(imagem_path)

        # Inserir no banco de dados
        con = sql.connect("app_orion_database.db")
        cur = con.cursor()
        cur.execute("insert into members(NOME, PAI, MAE, DATA_NASC, ESTADO_CIVIL, CPF, RG, SETOR_ATUAL, IGREJA_ATUAL, SETOR_ANTERIOR, IGREJA_ANTERIOR, BATIZADO_COM_ESPIRITO_SANTO, ESCOLARIDADE, PROFISSAO, BATIZADO_NAS_AGUAS, DATA_BATISMO_NAS_AGUAS, IGREJA_DE_BATISMO, ADMITIDO_POR, DATA_DA_CONSAGRACAO, DATA_DA_APRESENTACAO, CARGO_NA_IGREJA, ENDERECO, BAIRRO, CIDADE, ESTADO, CEP, TELEFONE, EMAIL, TEM_CARTAO_DE_MEMBRO, FOTO) values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",(nome, pai, mae,formatted_date_nasc, estado_civil, cpf, rg, setor_atual, igreja_atual, setor_anterior, igreja_anterior, batizado_com_espirito_santo, escolaridade, profissao, batizado, formatted_date_batismo, igreja_de_batismo, admitido_por, formatted_data_da_consagracao, formatted_data_da_apresentacao, cargo_na_igreja, endereco, bairro, cidade, estado, cep, telefone, email, tem_cartao, imagem_path))
        con.commit()

        # Exibir mensagem de flash
        flash("Dados cadastrados com sucesso.","success")

        # Redirecionar para o PDF gerado
        return redirect(url_for('list_member'))

    
    user_id = session.get('user_id')
    if user_id is None:
        flash("Você precisa fazer login para acessar esta página.", "danger")
        return redirect(url_for("login"))

    return render_template("membros/add_member.html", user_id = user_id)


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
        return redirect(url_for("list_member"))
    
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

if __name__=='__main__':
    app.run(debug=True, port=911)