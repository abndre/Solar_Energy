from subprocess import check_output
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import matplotlib as mpl

def Teste():
    print("Nada")

def WordcloudPlot(frame):
    list_di=[]
    for i in frame["ID"]:
        if not i == None:
            for j in i.split(';'):
                list_di.append(j)
    #mpl.rcParams['figure.figsize']=(8.0,6.0)    #(6.0,4.0)
    mpl.rcParams['font.size']=12                #10 
    mpl.rcParams['savefig.dpi']=100             #72 
    mpl.rcParams['figure.subplot.bottom']=.1 
    stopwords = set(STOPWORDS)
    wordcloud = WordCloud(
                              background_color='white',
                              stopwords=stopwords,
                              width=800, height=400,
                              max_words=200,
                              max_font_size=40, 
                              random_state=42
                             ).generate(str(list_di))
    fig = plt.figure(1)
    plt.figure( figsize=(20,10), facecolor='k')
    plt.imshow(wordcloud)
    plt.axis('off')
    fig.savefig("word1.png", dpi=1800)
    plt.show()