
#Tempo de execucao estimado ~ 35 a 40 s

import pandas as pd
import sys

from sklearn.neighbors import NearestNeighbors
from sklearn import preprocessing

#Esse metodo recebe um nome e retorna seu respectivo indice
def get_id(name):
    return anime[anime["name"]==name].index.tolist()[0]

#Esse metodo recebe o id e o vetor de indices do anime e imprime os 5 animes mais parecidos com o anime fornecido
def print_similar(id,indices):
    for i in indices[id][1:]:
        print "Anime:",anime.ix[i]["name"],"Episodios:", anime.ix[i]["episodes"],"Rating:",anime.ix[i]["rating"]

#Esse metodo imprime a quantidade "u" de animes pertencentes ao genero "w" fornecido
def print_genres(w,u):
    for i in range(0,len(anime)):
        if str(anime.ix[i]["genre"]).upper().find(w.upper())>=0:
            print "Anime:",anime.ix[i]["name"],"Episodios:", anime.ix[i]["episodes"],"Rating:",anime.ix[i]["rating"]
            u+=1
    print "O genero do tipo",w,"possui a seguinte quantidade de animes listados",u

#Esse metodo imprime as informacoes de um dado anime utilizando seu indice id
def print_anime(id):
	print "Genero:",anime.ix[id]["genre"],"\nTipo:",anime.ix[id]["type"],"\nEpisodios:",anime.ix[id]["episodes"],"\nRating:",anime.ix[id]["rating"],"\nIndex:",id

#Esse metodo verifica se o anime "w" existe no dataset
def check_anime(w):
    for i in range(0,len(anime)):
        if anime.ix[i]["name"] == w:
            return 1
    return 0

#Esse metodo verifica se o genero "w" existe no dadaset
def check_genre(w):
    for i in range(0,len(anime)):
        if str(anime.ix[i]["genre"]).upper() == w.upper():
            return 1
    print "Esse genero nao consta na lista\n"
    return 0

#Esse metodo recebe o nome do anime e a quantidade da nova quantidade de episodios "w" e o atualiza
def att_anime(name,w):
    anime.loc[(anime["name"]==name),"episodes"] = w

# Esse metodo recebe todas as informacoes de um anime e o adiciona no dataset
def add_anime(x,y,z,w,t,u):
	df = pd.DataFrame([[len(anime),x,y,z,w,t,u]],columns=['anime_id','name','genre','type','episodes','rating','members'])
	return pd.concat([anime,df],ignore_index=True)

#Esse metodo executa o knn retornando os indices e as distacias
def knn():
	print "Knn em execucao"
	#Formatacao das caracteristicas
	var_train = pd.concat([anime["genre"].str.get_dummies(sep=","),pd.get_dummies(anime[["type"]]),anime[["rating"]],anime[["members"]],anime["episodes"]],axis=1)

	#Reajuste das caracteristicas
	max_abs_scaler = preprocessing.MaxAbsScaler()
	#min_max_scaler = preprocessing.MinMaxScaler(feature_range=(0, 100))

	#Normalizacao das informacoes
	var_train = max_abs_scaler.fit_transform(var_train)
	#var_train = min_max_scaler.fit_transform(var_train)

	#Aplicacao do knn
	nbrs = NearestNeighbors(n_neighbors=6, algorithm='ball_tree').fit(var_train)
	return nbrs.kneighbors(var_train)

#Esse metodo remove um anime da lista de acordo com o indice id
def remove(id):
	return anime.drop(anime.index[[id]])

#Leitura do dataset
anime = pd.read_csv(open(sys.argv[1]))

#distances eh um vetor com as distancias do anime entre ele e ele mesmo, e os parecidos com ele de forma ordenada crescente
#indices eh um vetor de valores numericos, cada valor eh unico para cada anime, ou seja, um novo identificador
distances, indices = knn()
print "Knn realizado com sucesso"

#Interface de decisoes tomadas de acordo com o usuario
k = int(input("\nDigite 1 - Para listar os animes referentes a um genero dado\n" 
                "Digite 2 - Para listar os animes similares a um anime dado\n"
                "Digite 3 - Para obter as informacoes de um anime dado\n"
                "Digite 4 - Para atualizar a quantidade de episodios de um anime\n"
                "Digite 5 - Para adicionar um novo anime ao banco de dados\n"
                "Digite 6 - Para remover um anime do banco de dados\n"
                "Digite 7 - Sair \n"))
while (k != 7):
	
	if k == 1:
		genero = raw_input("Escolha um genero ")
		if check_genre(genero):
			print "Os animes do genero",genero,"sao"
			print_genres(genero,0)

	elif k == 2:
		nome = str(raw_input("Escreva um anime ")).title()
		if check_anime(nome):
			print "Os animes parecidos com",nome,"sao:"
			print_similar(get_id(nome),indices)
		else:
			print "Esse anime nao consta na lista\n"

	elif k == 3:
		nome = str(raw_input("Escreva um anime ")).title()
		if check_anime(nome):
			print "As informacoes do anime",nome,"sao:"
			print_anime(get_id(nome))
		else:
			print "Esse anime nao consta na lista\n"

	elif k == 4:
		nome = str(raw_input("Escreva um anime ")).title()
		if check_anime(nome):
			nova_qtde = int(raw_input("Indique a nova quantidade de episodios "))
			att_anime(nome,nova_qtde)

			print "A quantidade de episodios foi atualizada, aguarde a atualizacao do agrupamento"
			distances, indices = knn()
			print "Knn realizado com sucesso"
		else:
			print "Esse anime nao consta na lista\n"

	elif k==5:
		nome = str(raw_input("Informe o nome do anime: ")).title()
		if check_anime(nome)==0:
			genero = str(raw_input("Informe todos os generos que o anime possue separados por virgula: ")).title()
			tipo = str(raw_input("Informe o tipo do anime escolhendo entre: TV, Movie, OVA, ONA, Special e Music: ")).title()
			episodios = int(raw_input("Informe o numero de episodios do anime, caso nao saiba o numero exato, escreva 0 ou um numero aproximado: "))
			nota = float(raw_input("Informe a nota de classificacao do anime de 0.0 a 10.0: "))
			membros = int(raw_input("Informe o numero de fas do anime, caso nao saiba o numero exato, escreva 0 ou um numero aproximado: "))
			anime = add_anime(nome,genero,tipo,episodios,nota,membros)

			print "Seu anime foi inserido, aguarde a atualizacao do agrupamento"
			distances, indices = knn()
			print "Knn realizado com sucesso"
		else:
			print "Esse anime ja consta na lista\n"
	elif k==6:
		nome = str(raw_input("Informe o nome do anime: ")).title()
		if check_anime(nome):
			anime = remove(get_id(nome))
			anime.to_csv(sys.argv[1],index=False)
			print "Seu anime foi removido, aguarde a atualizacao do agrupamento"
			anime = pd.read_csv(open(sys.argv[1]))
			distances, indices = knn()
			print "Knn realizado com sucesso"
		else:
			print "Esse anime nao consta na lista\n"
	
	k = int(input("\nDigite 1 - Para listar os animes referentes a um genero dado\n" 
            "Digite 2 - Para listar os animes similares a um anime dado\n"
            "Digite 3 - Para obter as informacoes de um anime dado\n"
            "Digite 4 - Para atualizar a quantidade de episodios de um anime\n"
            "Digite 5 - Para adicionar um novo anime ao banco de dados\n"
            "Digite 6 - Para remover um anime do banco de dados\n"
            "Digite 7 - Sair \n"))
#fim do while


#envia o conteudo de anime para o mesmo arquivo csv lido, atualizando, assim, o dataset
anime.to_csv(sys.argv[1],index=False)

