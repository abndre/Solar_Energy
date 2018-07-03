import pdb
from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt
import community
import operator
import nltk

from networkx.readwrite import json_graph
import json

partition_colors = ['#DD0000', '#00DD00', '#0000DD', '#DDDD00',
	            '#00DDDD', '#DD00DD', '#880000', '#008800',
          	    '#000088', '#880088', '#888800', '#008888',
	            '#440000', '#004400', '#000044', '#440044',
          	    '#444400', '#004444', '#220000', '#002200',
          	    '#000022', '#220022', '#222200', '#002222']


G = nx.Graph()

#local
filelocal = './data/sample_wos_data.txt'

#nodes = defaultdict(int)

def format_wos_data(wos_list):
    result = {}

    for doc_index, doc in enumerate(wos_list):
	result[doc_index] = {}
	if 'AB' in doc:
	    result[doc_index]['abstract'] = ' '.join(doc['AB'])
	else:
	    result[doc_index]['abstract'] = ''
	if 'TI' in doc:
	    result[doc_index]['title'] = ' '.join(doc['TI'])
	else:
	    result[doc_index]['title'] = ''
	if 'PY' in doc:
	    result[doc_index]['publication_year'] = ' '.join(doc['PY'])
	else:
	    result[doc_index]['publication_year'] = ''
	if 'AU' in doc:
	    result[doc_index]['authors'] = doc['AU']
	else:
	    result[doc_index]['authors'] = []
	if 'CR' in doc:
	    result[doc_index]['references'] = doc['CR']
	else:
	    result[doc_index]['references'] = []
	if 'ID' in doc:
	    result[doc_index]['keywords'] = (' '.join(doc['ID'])).split(';')
	else:
	    result[doc_index]['keywords'] = []
	if 'DI' in doc:
	    result[doc_index]['doi'] = doc['DI'][0]
	else:
	    result[doc_index]['doi'] = ''
    return result

def parse_lines(doc_filepath, chunk_size = 2048, sep = '\n'):
    string_buffer = ''
    with open(doc_filepath, 'r') as file_handle:
	for chunk in iter(lambda: file_handle.read(chunk_size), ''):
	    string_buffer += chunk
	    splitted_buffer_list = string_buffer.split(sep)
	    while len(splitted_buffer_list) > 1:
		line = splitted_buffer_list.pop(0)
		if line:
		    yield line
		else:
		    pass

	    string_buffer = ''.join(splitted_buffer_list)
	else:
	    yield string_buffer

def load_wos_data_ex(file_path, count = None, output = None):
    #TODO: cuidar de multiplos DOIs.
    result = list()
    doc_list = list()
    temp_field = str()
    temp_data = str()
    temp_doc = dict()
    for line in parse_lines(file_path):
	if line[:2] == 'ER':
	    pass
	    doc_list.append(temp_doc.copy())
	    temp_doc = {}
	    if count and count < len(doc_list):
		break
	elif line[:2] == 'EF':
	    pass
	elif line[:2] != '  ':
	    pass
	    temp_field = line[:2]
	    temp_doc[temp_field] = []
	    temp_data = line[3:]
	    temp_doc[temp_field].append(temp_data)
	elif line[:2] == '  ':
	    pass
	    temp_data = line[3:]
	    temp_doc[temp_field].append(temp_data)
	else:
	    pass

    result = format_wos_data(doc_list)

    return result

texto = ''
def fretext(partition1, key1,texto,chave):
	for key, value in partition1.items():
		if value == key1:
			texto = texto + ' ' + ''.join(dicio_of_artic[key][chave])
	words = nltk.word_tokenize(texto)
	print 'quantidade palavras: ', len(words)

	# Remove single-character tokens
	words = [word for word in words if len(word) > 4]
	print 'quantidade palavras apos removao de palavras com tamanho menor que 4: ',len(words)

	#=====================================
	#pdb.set_trace()
	#x = filter(None, texto.split(' '))
	doubletext=defaultdict(int)
	for key,value in enumerate(words):
		try:
			newkey = value + x[key+1]
			doubletext[newkey]+=1
		except:
			pass

	a1 = sorted(doubletext	, key=doubletext.get, reverse=True)
	#pdb.set_trace()	
	#plt.bar(doubletext.keys(),doubletext.values())
	#plt.show()
	#======================================
	#pdb.set_trace()
	freq = nltk.FreqDist(words)
	#pdb.set_trace()

	print 'apresentando grafico com 20 maiores frequencias'
	#TODO: rotacionar o eixo x das palavras para melhor visualiacao 
	freq.plot(20, cumulative=False)

def grafi():
	#drawing
	size = float(len(set(partition.values())))
	pos = nx.spring_layout(G)
	count = 0.
	for com in set(partition.values()) :
	    count = count + 1.
	    list_nodes = [nodes for nodes in partition.keys() if partition[nodes] == com]
	    #pdb.set_trace()
	    nx.draw_networkx_nodes(G, pos, list_nodes, node_size = 40,
	                                node_color = str(count / size))
	
	nx.draw_networkx_labels(G,pos,font_size=11)
	nx.draw_networkx_edges(G,pos, alpha=0.5)
	plt.show()

#este dicionario contem um id unico com o nome
# do primeiro author e ano da publicacao: seguido do abstract e keywords como chaves 
#['doi', 'title', 'abstract', 'publication_year', 'references', 'authors', 'keywords']
dicio_of_artic = {}
def node_batchid(dicio):
	batchid = dicio['authors'][0].replace(" ","").replace(",","") + '_' +dicio['publication_year'] 
	dicio_of_artic[batchid]={'abstract':dicio['abstract'],'keywords':dicio['keywords']}
	return batchid 


#carrega os dados do WoS e armazena como dicionario
wos_dicio = load_wos_data_ex(filelocal)

#conta a quantidade de dados
quantidade_wos = len(wos_dicio)
quantidade_wos = 3000


#cria os nos e edges
#o edge e criado nas citacoes, se houver iguais citacoes ocorre o edge com os autores e ano como label
for quantidade in range(0,quantidade_wos):

	reference1=wos_dicio[quantidade]['references']
	new_value1 = node_batchid(wos_dicio[quantidade])
	G.add_node(new_value1)

	for quantidademaisum in range(quantidade+1,quantidade_wos):
		
		
		reference2=wos_dicio[quantidademaisum]['references']

		quantidade_de_referencias_em_comum = set(reference1).intersection(reference2)
		quantidade_de_referencias_em_comum = len(quantidade_de_referencias_em_comum)

		
		new_value2 = node_batchid(wos_dicio[quantidademaisum])
		G.add_node(new_value2)
		

		if quantidade_de_referencias_em_comum >=10	:
			#evitar nos iguais de criarem edges
			if  not (str(new_value1) == str(new_value2)):	
				G.add_edge(new_value1,new_value2,weight=quantidade_de_referencias_em_comum)
			
#remove nodes without edges
G.remove_nodes_from(list(nx.isolates(G)))

#cria as comunidades
partition = community.best_partition(G)

#plot grafic
#grafi()

##add group to nodes
for key, value in partition.items():
	G.add_node(key,group=value)


#===================
#organizando os cluster (partition)
#comparando com os dados do dicionario dos authores
dd=defaultdict(int)
for key, value in partition.items():
	dd[value]+=1

dds = sorted(dd.items(), key=operator.itemgetter(1))

#plot frequence
#fretext(partition, dds[-1][0],texto,'keywords')



###########################
#make D3JS	
###########################
import sys
data = json_graph.node_link_data(G)
s = json.dumps(data)
orig_stdout = sys.stdout
f = open('miserables.json', 'w')
sys.stdout = f
print s
sys.stdout = orig_stdout
f.close()
###########################
#make D3JS	
###########################

