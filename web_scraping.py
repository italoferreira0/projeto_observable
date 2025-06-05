import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import json
from datetime import date

url = "https://investidor10.com.br/acoes/rankings/maiores-dividend-yield/"

#Email e Senha no site Investidor10
email = ""
senha = ""

data_atual = str(date.today())

option = Options()
driver = webdriver.Chrome(options=option)

driver.get(url)
time.sleep(5)

for c in range(1):
    driver.execute_script("window.scrollBy(0, 500);")
    time.sleep(1)

button = driver.find_element(By.CSS_SELECTOR, 'button[data-id="read-more-action"]')
button.click()

time.sleep(5)
email_input = driver.find_element(By.NAME, "email")
email_input.send_keys(email)

senha_input = driver.find_element(By.NAME, "password")
senha_input.send_keys(senha)

botao_entrar = driver.find_element(By.CSS_SELECTOR, 'input[type="submit"][value="Entrar"]')
botao_entrar.click()

time.sleep(5)

for c in range(1):
    driver.execute_script("window.scrollBy(0, 500);")
    time.sleep(1)

time.sleep(5)

button = driver.find_element(By.CSS_SELECTOR, 'button[data-id="read-more-action"]')
button.click()

time.sleep(5)

for c in range(1):
    driver.execute_script("window.scrollBy(0, -500);")
    time.sleep(1)

time.sleep(5)

filtro = driver.find_element(By.CSS_SELECTOR, 'th[data-name="name_sector"]')
filtro.click()

time.sleep(5)

table_element = driver.find_element(By.ID, "rankigns")

linhas = table_element.find_elements(By.TAG_NAME, "tr")

dados = []

def para_float(valor):
    try:
        return float(valor.replace('%','').replace(',','.'))
    except (ValueError, AttributeError):
        return None


for linha in linhas:
    colunas = linha.find_elements(By.XPATH, ".//th | .//td")
    dado = [coluna.text.strip() for coluna in colunas]

    # print("Dado: ", dado)
    if dado[7] == 'Consumo Cíclico':
        dado[7] = 'Consumo Ciclico'

    if dado[7] == 'Consumo não Cíclico':
        dado[7] = 'Consumo nao Ciclico'

    objeto = {
        "codigo": dado[0],
        "dividendo_atual": para_float(dado[1]),
        "dividendo_medio": para_float(dado[2]),
        "p_l": para_float(dado[3]),
        "p_vp": para_float(dado[4]),
        "setor": dado[7],
        "data": data_atual

    }

    dados.append(objeto)

dados.pop(0)
(len(dados))

caminho_arquivo = 'json/Maiores_Dividendos.json'

with open(caminho_arquivo, 'w') as f:
    json.dump(dados, f, indent=4)

driver.quit()