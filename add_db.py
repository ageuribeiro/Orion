import sqlite3 as sql

con = sql.connect('app_orion_database.db')
cur = con.cursor()
cur.execute('DROP TABLE IF EXISTS users')

sql = '''CREATE TABLE "users" (
    "ID" INTEGER PRIMARY KEY AUTOINCREMENT,
    "NOME" TEXT,
    "EMAIL" TEXT,
    "SENHA" TEXT
)'''

sql_member = '''CREATE TABLE "members" (
    "ID" INTEGER PRIMARY KEY AUTOINCREMENT,
    "NOME" TEXT,
    "PAI" TEXT,
    "MAE" TEXT,
    "DATA_NASC" TEXT,
    "ESTADO_CIVIL" TEXT,
    "CPF" TEXT,
    "RG" TEXT,
    "SETOR_ATUAL" TEXT,
    "IGREJA_ATUAL" TEXT,
    "SETOR_ANTERIOR" TEXT,
    "IGREJA_ANTERIOR" TEXT,
    "BATIZADO_COM_ESPIRITO_SANTO" TEXT,
    "ESCOLARIDADE" TEXT,
    "PROFISSAO" TEXT,
    "BATIZADO_NAS_AGUAS" TEXT,
    "DATA_BATISMO_NAS_AGUAS" TEXT,
    "IGREJA_DE_BATISMO" TEXT,
    "ADMITIDO_POR" TEXT,
    "DATA_DA_CONSAGRACAO" TEXT,
    "DATA_DA_APRESENTACAO" TEXT,
    "CARGO_NA_IGREJA" TEXT,
    "ENDERECO" TEXT,
    "BAIRRO" TEXT,
    "CIDADE" TEXT,
    "ESTADO" TEXT,
    "CEP" TEXT,
    "TELEFONE" TEXT,
    "EMAIL" TEXT,
    "TEM_CARTAO_DE_MEMBRO" TEXT,
    "FOTO" TEXT
)'''
cur.execute(sql)
cur.execute(sql_member)
con.commit()
con.close()