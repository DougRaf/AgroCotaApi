# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import mysql.connector

html = requests.get("https://www.noticiasagricolas.com.br/cotacoes/sucroenergetico/acucar-cristal-cepea").content
soup = BeautifulSoup(html, 'html.parser')
all_tables = soup.find("table")
tables = all_tables.findAll('td')
vencimento = tables[0].text.strip()
saca = tables[1].text.strip()
variacao = tables[2].text.strip()

# conectando ao banco de dados antes de inserir as informações

db = mysql.connector.connect(
    host="opmy0013.servidorwebfacil.com",
    user="dougr_projetos",
    password="Douglas@2019",
    database="dougraf35_projetos"
)

dados = db.cursor()
dados.execute("SELECT vencimento from webdados order by idCod desc limit 1 ")
resultado = dados.fetchone()

for row in resultado:
    if row == vencimento:
        print("Esse item já existe na base de dados")
        exit()
    else:
        # Preparando e inserindo as informações no banco de dados.
        sql = "INSERT INTO webdados (vencimento, saca, variacao) VALUES (%s, %s, %s)"
        val = (vencimento, saca, variacao)
    try:
        # Executando comando em sql
        dados.execute(sql, val)

        # Comprometendo as mudanças no banco.
        db.commit()

        # Exibindo o status da atualização.
        print(dados.rowcount, "atualizado com sucesso")

    except:
        # Caso encontre algum erro é reportado de volta com a mensagem.
        db.rollback()
        print(dados.rowcount, "Falha na atualização")