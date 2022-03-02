import pandas as pd
from math import pi
import matplotlib.pyplot as plt
import os
import random
from multiprocessing import Process



def generate_graph(dico,email):
    dico_temp = {"group":["A"]}
    for i in dico.keys():
        dico_temp[i] = [dico[i]*10]
    dico=dico_temp
    df = pd.DataFrame(dico)
    categories=list(df)[1:]
    N = len(categories)
    
    values=df.loc[0].drop('group').values.flatten().tolist()
    values += values[:1]
    
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]
    
    ax = plt.subplot(111, polar=True)
    
    plt.xticks(angles[:-1], categories, color='grey', size=8)

    ax.set_rlabel_position(0)
    plt.yticks([20,40,60,80,100], ["20","40","60","80","100"], color="grey", size=7)
    plt.ylim(0,110)
    
    ax.plot(angles, values, linewidth=1, linestyle='solid')

    ax.fill(angles, values, 'b', alpha=0.1)

    random_str = "".join(str(random.randint(0,9)) for i in range(30))
    plt.savefig(f'./static/{random_str}.png',transparent=True)
    with open(f'./static/{random_str}.png','rb') as file:
        data = file.read()
    with open(f'./static/{email}.png','wb') as file:
        file.write(data)
    os.remove(f'./static/{random_str}.png')
    plt.clf()


def main_graph(dico,email):
    p = Process(target=generate_graph, args=(dico,email,))
    p.start()
    p.join()
