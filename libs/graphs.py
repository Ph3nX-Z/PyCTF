import pandas as pd
from math import pi
import matplotlib.pyplot as plt
import os
import random
import multiprocessing



def generate_graph_multi(dico,email):
    dico_temp = {"group":["A"]}
    for i in dico.keys():
        dico_temp[i] = [dico[i]*10]
    dico=dico_temp
    print(dico)
    df = pd.DataFrame(dico)
    # number of variable
    categories=list(df)[1:]
    N = len(categories)
    
    # We are going to plot the first line of the data frame.
    # But we need to repeat the first value to close the circular graph:
    values=df.loc[0].drop('group').values.flatten().tolist()
    values += values[:1]
    
    # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]
    
    # Initialise the spider plot
    ax = plt.subplot(111, polar=True)
    
    # Draw one axe per variable + add labels
    plt.xticks(angles[:-1], categories, color='grey', size=8)
    
    # Draw ylabels
    ax.set_rlabel_position(0)
    plt.yticks([10,20,30], ["10","20","30"], color="grey", size=7)
    plt.ylim(0,40)
    
    # Plot data
    ax.plot(angles, values, linewidth=1, linestyle='solid')
    
    # Fill area
    ax.fill(angles, values, 'b', alpha=0.1)


    # Show the graph
    #plt.show()
    random_str = "".join(str(random.randint(0,9)) for i in range(30))
    plt.savefig(f'./static/{random_str}.png',transparent=True)
    with open(f'./static/{random_str}.png','rb') as file:
        data = file.read()
    with open(f'./static/{email}.png','wb') as file:
        file.write(data)
    os.remove(f'./static/{random_str}.png')
    plt.clf()

def generate_graph(dico,email):
    global process
    process = multiprocessing.Process(target=generate_graph, args=(dico,email,))
    process.start()

if __name__=="__main__":
    pass
