from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json

# Login/senha
matricula = "*****"
password = "******"

# Inicializacao do driver Firefox
driver = webdriver.Firefox()

# Abrindo o sistacad na tela de login
driver.get("https://sistacad.cederj.edu.br/")

 
# Enviando o numero da matricula
elmnt = driver.find_element_by_id("txtIdLogin")
elmnt.send_keys(matricula)

# Enviando a senha
elmnt = driver.find_element_by_id("txtIdPassword")
elmnt.send_keys(password)

# Pressionando o botão de login
elmnt.send_keys(Keys.RETURN) # Como se apertasse Enter

# Indo para a pagina Notas do Semestre

driver.get("https://sistacad.cederj.edu.br/notassemestre.asp")
dados = {"notas":[]}
relatorios = driver.find_elements_by_class_name("Relatorio")
for relatorio in relatorios:
    disciplina = []
    titulos = relatorio.find_element_by_class_name("RelatorioTitulo")
    tabela = driver.find_element_by_class_name("RelatorioCorpo")
    nomeDisciplina = titulos.text.split("  ")[4]
    notas = tabela.text.split(" ")
    disciplina.append(nomeDisciplina)
    for nota in notas:
        disciplina.append(nota)
    dados["notas"].append(disciplina)

dados = json.dumps(dados)

print(dados)


# Indo para Histórico

notasHistorico = []
driver.get("https://sistacad.cederj.edu.br/historico.asp")


relatorios = driver.find_elements_by_class_name("Relatorio")
relatorioHoras = relatorios[0]
relatorioNotas = relatorios[1]
dadosHoras = []
# Parte responsavel por coletar os dados das horas cursadas 
tabela = relatorioHoras.find_element_by_class_name("RelatorioCorpo")
for dado in tabela.text:
    dadosHoras.append(dado)

#print(dadosHoras)


# Parte responsavel por coletar as disciplinas cursadas
dadosNotas = []
tabela = relatorioNotas.find_element_by_class_name("RelatorioCorpo")
colunas = tabela.find_elements_by_tag_name("tr")
for dado in colunas:
    informacao = dado.find_elements_by_tag_name("td")
    a=[]
    for i in informacao:
        a.append(i.text)

    
    dadosNotas.append(a)

#print(dadosNotas)


dadosJson = {"horas":{dadosHoras[0]:dadosHoras[1],dadosHoras[2]:dadosHoras[3],dadosHoras[4]:dadosHoras[5]},"notas":dadosNotas
}

json_dados = json.dumps(dadosJson)
print(json_dados)

# Fechando o driver
driver.close()
