from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import pandas as pd
import pdfplumber

app = Flask(__name__)

# Função para buscar dados no site da ANAC
def buscar_dados_anac(matricula):
    url = f"https://sistemas.anac.gov.br/aeronaves/cons_rab.asp#matricula={matricula}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Exemplo de como capturar os dados
    # Isso depende da estrutura HTML do site
    modelo = soup.find("td", text="Modelo").find_next("td").text
    mtow = soup.find("td", text="MTOW").find_next("td").text
    return modelo, float(mtow)

# Função para buscar tarifas com base no MTOW
def buscar_tarifas(mtow):
    tarifas = []
    with pdfplumber.open("Tabela de Tarifas e Serviços 2025 SBJH.pdf") as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            # Processar e encontrar os valores baseados no MTOW
            # Transformar em lógica com base na tabela
            pass  # Substituir pelo processamento da tabela
    return tarifas

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        matricula = request.form["matricula"]
        modelo, mtow = buscar_dados_anac(matricula)
        tarifas = buscar_tarifas(mtow)
        return render_template("index.html", modelo=modelo, mtow=mtow, tarifas=tarifas)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
