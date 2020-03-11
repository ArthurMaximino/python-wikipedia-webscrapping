#Importação de bibliotecas:
#Importando requests para fazer as requisições pela web
import requests
#Importando BeautifulSoup para realizar o tratamento da página web recebida
from bs4 import BeautifulSoup
#Importando pandas para trabalhar com resultados organizados em tabelas
import pandas as pd
#Importando re para operações com expressões regulares
import re
#Importando os para as operações de encerramento do programa
import os


#Função main() como a função principal, que vai chamar todas as funções essenciais para o programa
def main():
    print("""" __          ___ _    _                                             _     
 \ \        / (_) |  (_)                                           | |    
  \ \  /\  / / _| | ___     _ __  _   _     ___  ___  __ _ _ __ ___| |__  
   \ \/  \/ / | | |/ / |   | '_ \| | | |   / __|/ _ \/ _` | '__/ __| '_ \ 
    \  /\  /  | |   <| |   | |_) | |_| |   \__ \  __/ (_| | | | (__| | | |
     \/  \/   |_|_|\_\_|   | .__/ \__, |   |___/\___|\__,_|_|  \___|_| |_|
                     ______| |     __/ |_____                             
                    |______|_|    |___/______|                            """)
    #A função main está num loop que só para ou quando o usuário não quiser mais usar o programa ou quando ele não der um comando corretamente
    repeat = True
    while repeat:
        word = input("Digite a palavra que deseja pesquisar:\t")
        #Para fazer uma busca pela url, a palavra com espaços recebe '_', como por exemplo em 'pão de mel' ficaria 'pão_de_mel'
        word = re.sub(r"\s+(?!$)", '_', word)
        search(word)
        answer = input("deseja fazer outra busca? <s/n>\t")
        if answer == 's':
            repeat = True
        elif answer == 'n':
            repeat = False
        else:
            print("Opção inválida! Encerrando o programa!")
            repeat = False
    print("Tchau, tchau! Espero ter ajudado!")
    return
    

#A função search() pesquisa na Wikipédia se há um artigo na wikipédia com a string digitada pelo usuário
def search(word):
    #Realizando a pesquisa na Wikipédia 
    website_url = requests.get("https://pt.wikipedia.org/wiki/"+word).text
    #Formatando os dados pelo BeautifulSoup
    soup = BeautifulSoup(website_url, 'lxml')
    #Se a operação no bloco try for um sucesso, é um sinal de que já existe um artigo na Wikipédia, então imprime o resultado para o usuário
    try:
        searchDesc = soup.find('div',{"mw-parser-output"}).p.get_text()
        print(searchDesc)
    #O except chama a função search_similiar_words() para verificar se o há algum artigo na Wikipédia que menciona o termo pesquisado pelo usuário
    except:
        search_similar_words(word)


#A função search_similar_words() procura por palavras semelhantes, usando os termos pequisados pelo usuário como palavras-chave   
def search_similar_words(word):
    print("Oops, houve um erro! Não foi encontrado um resultado!\n Verifique se estes resultados se assemelham ao que queria pesquisar: ")
    #Substituindo o '_' da string para '+', para realizar a busca na Wikipédia com as palavras-chave
    semiword =  re.sub(r"_", '+', word)
    website_url = requests.get("https://pt.wikipedia.org/w/index.php?search="+semiword+"&title=Especial%3APesquisar&go=Ir&ns0=1").text
    soup = BeautifulSoup(website_url, 'lxml')
    #Pegando o título de cada artigo relacionado
    searchDesc = soup.find_all('div', {"class":"mw-search-result-heading"})
    #Salvando os títulos em uma lista que será tratada pelo Pandas
    results = []
    for value in searchDesc:
        results.append(value.text)
    if len(results) == 0:
        print("Oops... não há nenhum registro semelhante também. Desculpe-me :'(")
        return
    df = pd.DataFrame()
    df["results"] = results
    print(df)
    choosenValue = input("Caso tenha encontrado encontrado o que procura, entre com o indíce do que resultado escolhido. Caso contrário, digite 'n':\t")
    if choosenValue == 'n':
        print("Tudo bem, desculpe-me por não ter oferecido resultados bons o bastante... :'( \n Mas você pode ajudar contribuindo para a Wikipédia!")
        return
    try:
        curValue = results[int(choosenValue)]
        curValue = re.sub(r"\s+(?!$)", '_', curValue)
        search(curValue)
    except:
        print("Oops... parece que você selecionou uma opção inexistente!\n")
        return
    
if __name__ == "__main__":
    main()
