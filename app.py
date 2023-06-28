from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory, send_file
from models import User, Member
from forms import RegistrationFormMember
from routes import register_member
from flask_sqlalchemy import SQLAlchemy
import firebase_admin
from firebase_admin import credentials
import pdfkit
import datetime
import os


# credenciais GCP
cred = credentials.Certificate()
# Configuração do Flask e do banco de dados
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/AppOrion'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'files'
app.secret_key = os.urandom(16)

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(80), nullable=False)
    nome = db.Column(db.String(80), nullable=False)
    def __init__(self, email, senha, nome):
        self.email = email
        self.senha = senha
        self.nome = nome

    def __repr__(self):
        return f'<User: {self.NOME}>'

class Member(db.Model):
    __tablename__ = 'members'
    ID = db.Column(db.Integer, primary_key=True)
    NOME = db.Column(db.String(255))
    PAI = db.Column(db.String(255))
    MAE = db.Column(db.String(255))
    DATA_NASC = db.Column(db.String(255))
    ESTADO_CIVIL = db.Column(db.String(255))
    CPF = db.Column(db.String(255))
    RG = db.Column(db.String(255))
    SETOR_ATUAL = db.Column(db.String(255))
    IGREJA_ATUAL = db.Column(db.String(255))
    SETOR_ANTERIOR = db.Column(db.String(255))
    IGREJA_ANTERIOR = db.Column(db.String(255))
    BATIZADO_COM_ESPIRITO_SANTO = db.Column(db.String(255))
    ESCOLARIDADE = db.Column(db.String(255))
    PROFISSAO = db.Column(db.String(255))
    BATIZADO_NAS_AGUAS = db.Column(db.String(255))
    DATA_BATISMO_NAS_AGUAS = db.Column(db.String(255))
    IGREJA_DE_BATISMO = db.Column(db.String(255))
    ADMITIDO_POR = db.Column(db.String(255))
    DATA_DA_CONSAGRACAO = db.Column(db.String(255))
    DATA_DA_APRESENTACAO = db.Column(db.String(255))
    CARGO_NA_IGREJA = db.Column(db.String(255))
    ENDERECO = db.Column(db.String(255))
    BAIRRO = db.Column(db.String(255))
    CIDADE = db.Column(db.String(255))
    ESTADO = db.Column(db.String(255))
    CEP = db.Column(db.String(255))
    TELEFONE = db.Column(db.String(255))
    EMAIL = db.Column(db.String(255))
    TEM_CARTAO_DE_MEMBRO = db.Column(db.String(255))
    FOTO = db.Column(db.String(255))

    def __repr__(self):
        return f'<Member: {self.NOME}>'

users = []
users.append(object)

# index
@app.route("/")
def index():
    return render_template("index.html")

# login session 
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]
        
        user = User.query.filter_by(email=email, senha=senha).first()

        if user:
            session['user_id'] = user[0]
            flash("Login realizado com sucesso.","success")
            return redirect(url_for("list_member"))
    
        else:
            flash("Credenciais inválidas. Tente novamente.", "danger")
    return render_template("index.html")

# logout session    
@app.route("/logout")
def logout():
    session.pop('user_id',None)
    flash("Logout realizado com sucesso.", "success")
    return redirect(url_for("index"))

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

    return render_template("usuarios/list_user.html", datas=data, user_id = user_id)

@app.route("/register_user")
def register_user():
    return render_template('usuarios/add_user.html')

# adicionar usuario
@app.route("/add_user", methods=["POST", "GET"])
def add_user():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]

        user = User(nome=nome, email=email, senha=senha)
        db.session.add(user)
        db.session.commit()
        
        flash("Dados cadastrados com sucesso.","success")
        return redirect(url_for("list_user"))
    
    user_id = session.get('user_id')
    if user_id is None:
        flash("Você precisa fazer login para acessar esta página.", "danger")
        return redirect(url_for("login"))

    return render_template("usuarios/add_user.html", user_id = user_id)

# editar usuario        
@app.route("/edit_user/<int:id>", methods=["POST", "GET"])
def edit_user(id):
    
    user_id = session.get('user_id')
    if user_id is None:
        flash("Você precisa fazer login para acessar esta página.", "danger")
        return redirect(url_for("login"))
    
    user = User.query.get(id)

    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]


        user.nome = nome
        user.email = email
        user.senha = senha

        db.session.commit()
    
        flash("Dados atualizados com sucesso.", "success")
        return redirect(url_for("index"))

    return render_template("edit_user.html", datas=data, user_id=user_id)

# deletar usuario
@app.route("/delete_user/<string:id>", methods=["GET"])
def delete_user(id):
    con = sql.connect("app_orion_database.db")
    cur=con.cursor()
    cur.execute("delete from users WHERE ID=?",(id))
    con.commit()
    flash("Dados deletados.","warning")

    
    return redirect(url_for("list_user"))

# listar membro
@app.route("/list_member")
def list_member():
    
    con = sql.connect("app_orion_database.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute("select * from members")
    data=cur.fetchall()

    user_id = session.get('user_id')
    if user_id is None:
        flash("Você precisa fazer login para acessar esta página.", "danger")
        return redirect(url_for("login"))
    return render_template("membros/list_member.html", datas=data, user_id=user_id)

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
    with app.app_context():

        db.create_all()
    
    app.run(debug=True)