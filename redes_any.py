import pdb
from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt
#import community
import operator
import nltk
import glob
import codecs
import pandas as pd

columns =  ['PT', 'AU', 'BA', 'BE', 'GP', 'AF', 'BF', 'CA', 'TI', 'SO', 'SE', 'BS',
       'LA', 'DT', 'CT', 'CY', 'CL', 'SP', 'HO', 'DE', 'ID', 'AB', 'C1', 'RP',
       'EM', 'RI', 'OI', 'FU', 'FX', 'CR', 'NR', 'TC', 'Z9', 'U1', 'U2', 'PU',
       'PI', 'PA', 'SN', 'EI', 'BN', 'J9', 'JI', 'PD', 'PY', 'VL', 'IS', 'PN',
       'SU', 'SI', 'MA', 'BP', 'EP', 'AR', 'DI', 'D2', 'EA', 'EY', 'PG', 'WC',
       'SC', 'GA', 'UT', 'PM', 'OA', 'HC', 'HP', 'DA']

files ='Solar_Energy/WoS/all/'
allFiles = glob.glob(files + "/*.txt")
#doc = codecs.open(myfile,'rU','UTF-16')

frame = pd.DataFrame()
list_ = []
for file_ in allFiles:
    #print(file_)
    doc = codecs.open(file_,'rU','UTF-16')
    df = pd.read_csv(doc,usecols=columns, sep='\t',parse_dates=True)
    df=df.where((pd.notnull(df)), None)
    list_.append(df)
frame = pd.concat(list_)
#remove_list=['PT','BA','BE','MA','EA','GP','BF','BS','PM','OA','HC','HP']
get_list =['AU','CR','TI','SO','ID','AB','PU','PI','J9','WC','SG','PY']
remove_list = list(set(columns) - set(get_list))
frame.drop(remove_list, axis=1, inplace=True)

text =''
for abstract in frame.AB:
    if not abstract == None:
        text = text + abstract


words = nltk.word_tokenize(text)
print ('quantidade palavras: ', len(words))

# Remove single-character tokens
words = [word for word in words if len(word) > 4]
print ('quantidade palavras apos removao de palavras com tamanho menor que 4: ',len(words))


freq = nltk.FreqDist(words)


print ('apresentando grafico com 20 maiores frequencias')
#TODO: rotacionar o eixo x das palavras para melhor visualiacao
freq.plot(20, cumulative=False)
