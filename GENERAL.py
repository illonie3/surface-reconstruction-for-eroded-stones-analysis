# coding: utf-8
from processing import *
from numpy import *
import matplotlib.pyplot as plt
from PIL import Image
import scipy.ndimage as ndimage
from matplotlib import cm
import os
import pandas as pd
import plotly.graph_objects as go
#importer PIL, os, pandas, plotly


##algorithme de reconstruction##
def traitement(dossier):
    'nom du dossier suivi de /.'
    I,mask,S = read_data_file(dossier) #angle réglable
##    plt.figure(figsize=(8,5))
##    for i in range(I.shape[2]):
##        print((2,int(I.shape[2]/2),i+1))
##        plt.subplot(2,int(I.shape[2]/2),i+1)
##        plt.imshow(I[:,:,i],cmap= plt.cm.gray)
##        plt.axis('off')
##        plt.title(i)
    I_all = I.reshape(I.shape[0]*I.shape[1],I.shape[2]).T

    M = linalg.pinv(S).dot(I_all)
    M_1 = M[0]
    M_2 = M[1]
    M_3 = M[2]

    rho = sqrt(M_1**2 + M_2**2 + M_3**2).reshape(I.shape[0],I.shape[1])

    n_1 = (M_1 / rho.reshape(-1)).reshape(I.shape[0],I.shape[1])
    n_2 = (M_2 / rho.reshape(-1)).reshape(I.shape[0],I.shape[1])
    n_3 = (M_3 / rho.reshape(-1)).reshape(I.shape[0],I.shape[1])

    z = unbiased_integrate(n_1,n_2,n_3,mask)
    graphique1(dossier,z.shape[0],z)
    return z

def graphique1(dossier,a,Z):
    X,Y=arange(0,a,1),arange(0,a,1)
    X,Y=meshgrid(X, Y)
    fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y)])
    fig.update_layout(title=dict(text='Surface'), autosize=False,
                  width=1500, height=700,
                  margin=dict(l=65, r=50, b=65, t=90))

    #ligne à modifier pour augmenter/diminuer la profondeur: modifier z à la ligne 124. 1=non modifié, 0.1=divisé par 10
    fig.update_layout(scene_aspectmode='manual',scene_aspectratio=dict(x=1, y=1, z=0.1))
    fig.write_html(dossier+'/reconstruction.html')



def graphique2(G,z,p):
    s=len(z[0])*len(z)
    save(G+'z.npy',z)
    y=cumsum([i/s for i in histogram(z)[0]])
    x=histogram(z)[1][:-1]
    plt.plot(x,y)
    plt.savefig(G+'repartition.jpg')
    plt.close()
    plt.plot(x,histogram(z)[0])
    plt.savefig(G+str(std(z))+".jpg")
    plt.close()
         #(1-p)/2
    m,M=0,len(y)-1
    while y[m]<(1-p)/2:
        m+=1
    while y[M]>1-(1-p)/2:
        M-=1
    return x[m],x[M]
def traitementgeneral(G,p):
    L=len(os.listdir(G))-1
    i=0
    for dossier in os.listdir(G):
        i+=1
        print(i/L*100,'%')
        z=traitement(G+dossier+'/')
        m,M=graphique2(G+dossier+'/',z,p)
        with open(G+'/'+'extrema.txt','a') as f:
            f.write('\n')
            f.write(str(dossier)+':'+str(m)+','+str(M))

calcaire_1m={3:-11.357327455681089,4:-11.538802142086313,5:-19.450614651165296}#3 du 10
calcaire_1bism={3:-17.133140381338677,5:-28.684865749429814}#3 du 10bis
calcaire_3m={2:-22.085806738275835,2.5:-9.087885496524345,3:-18.615686688361883,3.5:-24.411133762699883,4:-10.30238358455179,4.5:-15.76704592525503}
calcaire_3bism={2.5:-11.511106086635948,3:-6.976749509353084,3.5:-9.345452204796885,4:-16.2936043966589,4.5:-6.872816197447545}
calcaire_5m={2:-30.094024781075923,2.5:-20.601503993432328,3:-12.698417908434573,3.5:-13.05537805742108,4:-12.648300483907477,4.5:-41.88451066451516}#2 du 14
calcaire_5bism={2:-12.810812929071664,2.5:-21.659868219746354,3:-11.417601403416242,3.5:6.230772076770577,4:-8.397085879908019,4.5:-10.039881903269265}#2 du 14bis
calcaire_8m={3:-4.4820983085488875,5:-7.0803698093538046}
calcaire_8bism={3:-4.7409501961839755,5:-7.8745760246001755}
calcaire_9m={2:-14.667826377311169,4:-53.128274721878775,3:-11.320745107743821}
calcaire_9bism={2:-13.433868641755097,4:-15.94178268832205,3:-22.974940011810126}
calcaire_11m={1:-5.184921527411236,1.5:-3.475662250542697,2:-9.302912758588604,2.5:-5.1834025088045514}
calcaire_11bism={1:-8.678364381973022,1.5:-8.28039567469457,2:-10.98857599332125,2.5:-7.064157931695691}
calcaire_13m={1:-4.67006696500332,1.5:-14.534904657212493,2.5:-38.36802272233236}
calcaire_13bism={1:-7.5913377278733805,1.5:-10.07413366163297,2.5:-5.437018842558306}
calcaire_7m={}

calcaire_1M={3:-0.9716070406194497,4:3.8742863842209765,5:5.160163759835989}
calcaire_1bisM={3:-6.7343665637098695,5:1.3247508295457635}
calcaire_3M={2:1.9406674348507096,2.5:0.9346299581171653,3:-1.0043686920903383,3.5:5.500437952027525,4:-3.9707511066649346,4.5:-2.817570769584542}
calcaire_3bisM={2.5:-0.5387733307064018,3:3.754477405195612,3.5:2.9034235823841357,4:2.9137503823100133,4.5:1.5356438520939193}
calcaire_5M={2:5.246908226963967,2.5:8.340274026646462,3:3.0243320290319957,3.5:-1.6632946893669285,4:2.7796357461959715,4.5:17.06748930111769}
calcaire_5bisM={2:2.3802216802418563,2.5:3.0725224246650242,3:1.752601766601904,3.5:-1.9276745772501194,4:1.5166033920456101,4.5:1.9011804105009809}
calcaire_8M={3:0.22687292513065493,5:1.5612622132874776}
calcaire_8bisM={3:1.5877553863851954,5:2.4703344922583383}
calcaire_9M={2:-1.5722122892602641,4:2.758340104253506,3:0.11444732195730722}
calcaire_9bisM={2:1.0046146193628616,4:2.80050846324945,3:6.230772076770577}
calcaire_11M={1:0.6119833815130473,1.5:1.0864391153008564,2:-2.9110405238319004,2.5:1.065256151511612}
calcaire_11bisM={1:2.399624647216651,1.5:-3.1658000746835704,2:1.691679186310914,2.5:0.21241958428571728}
calcaire_13M={1:1.5170756065287296,1.5:0.19129092979750695,2.5:5.808617156664539}
calcaire_13bisM={1:-0.9373594654518698,1.5:-1.249566358062836,2.5:-1.2073279734930011}
calcaire_7M={}

calcaire_1={i:calcaire_1M[i]-calcaire_1m[i] for i in calcaire_1M}
calcaire_1bis={i:calcaire_1bisM[i]-calcaire_1bism[i] for i in calcaire_1bisM}
calcaire_3={i:calcaire_3M[i]-calcaire_3m[i] for i in calcaire_3M}
calcaire_3bis={i:calcaire_3bisM[i]-calcaire_3bism[i] for i in calcaire_3bisM}
calcaire_5={i:calcaire_5M[i]-calcaire_5m[i] for i in calcaire_5M}
calcaire_5bis={i:calcaire_5bisM[i]-calcaire_5bism[i] for i in calcaire_5bisM}
calcaire_8={i:calcaire_8M[i]-calcaire_8m[i] for i in calcaire_8M}
calcaire_8bis={i:calcaire_8bisM[i]-calcaire_8bism[i] for i in calcaire_8bisM}
calcaire_9={i:calcaire_9M[i]-calcaire_9m[i] for i in calcaire_9M}
calcaire_9bis={i:calcaire_9bisM[i]-calcaire_9bism[i] for i in calcaire_9bisM}
calcaire_11={i:calcaire_11M[i]-calcaire_11m[i] for i in calcaire_11M}
calcaire_11bis={i:calcaire_11bisM[i]-calcaire_11bism[i] for i in calcaire_11bisM}
calcaire_13={i:calcaire_13M[i]-calcaire_13m[i] for i in calcaire_13M}
calcaire_13bis={i:calcaire_13bisM[i]-calcaire_13bism[i] for i in calcaire_13bisM}
calcaire_7={}
def minmax():
    L=[calcaire_1,calcaire_1bis,calcaire_3,calcaire_3bis,calcaire_5,calcaire_5bis,calcaire_7,calcaire_8,calcaire_8bis,calcaire_9,calcaire_9bis,calcaire_11,calcaire_11bis,calcaire_13,calcaire_13bis]
    C=["red","red","brown","brown","blue","blue","red","green","green","red","red","blue","blue","brown","brown"]
    for i in range(len(L)):
        plt.plot(L[i].keys(),L[i].values(),label=str(i+1),color=C[i])
    plt.legend()
    plt.show()


def D(x):
    if x==None:
        return 0
    else:
        return x
def D2(x):
    if x==None:
        return 0
    else:
        return 1
def p(x,L):
    s=0
    for i in L:
        s+=D2(i.get(x))
    if s==0:
        return 1
    else:
        return s

def prof_moyenne():
    X=[0,1,1.5,2,2.5,3,3.5,4,4.5,5]

    ALT={i:(D(calcaire_1.get(i))+D(calcaire_1bis.get(i))+D(calcaire_9.get(i))+D(calcaire_9bis.get(i)))/p(i,[calcaire_1,calcaire_1bis,calcaire_9,calcaire_9bis]) for i in X}
    P_EAU={i:(D(calcaire_5.get(i))+D(calcaire_5bis.get(i))+D(calcaire_11.get(i))+D(calcaire_11bis.get(i)))/p(i,[calcaire_5,calcaire_5bis,calcaire_11,calcaire_11bis]) for i in X}
    P_ARGILE={i:(D(calcaire_3.get(i))+D(calcaire_3bis.get(i))+D(calcaire_13.get(i))+D(calcaire_13bis.get(i)))/p(i,[calcaire_3,calcaire_3bis,calcaire_13,calcaire_13bis]) for i in X}
    INALT={i:(calcaire_8[i]+calcaire_8bis[i])/2 for i in calcaire_8}

    ALT_err={i:std([D(calcaire_1.get(i)),D(calcaire_1bis.get(i)),D(calcaire_9.get(i)),D(calcaire_9bis.get(i))])/sqrt(p(i,[calcaire_1,calcaire_1bis,calcaire_9,calcaire_9bis])) for i in X}
    P_EAU_err={i:std([D(calcaire_5.get(i)),D(calcaire_5bis.get(i)),D(calcaire_11.get(i)),D(calcaire_11bis.get(i))])/sqrt(p(i,[calcaire_5,calcaire_5bis,calcaire_11,calcaire_11bis])) for i in X}
    P_ARGILE_err={i:std([D(calcaire_3.get(i)),D(calcaire_3bis.get(i)),D(calcaire_13.get(i)),D(calcaire_13bis.get(i))])/sqrt(p(i,[calcaire_3,calcaire_3bis,calcaire_13,calcaire_13bis])) for i in X}
    INALT_err={i:std([calcaire_8[i],calcaire_8bis[i]])/sqrt(2) for i in calcaire_8}

    plt.errorbar([0,1,2,3,4,5],[ALT[i] for i in [0,1,2,3,4,5]],yerr=[ALT_err[i] for i in [0,1,2,3,4,5]],color="red",capsize=4)
    plt.errorbar([0,1,1.5,2,2.5,3,3.5,4,4.5,5],[P_EAU[i] for i in [0,1,1.5,2,2.5,3,3.5,4,4.5,5]],yerr=[P_EAU_err[i] for i in [0,1,1.5,2,2.5,3,3.5,4,4.5,5]],color="blue",capsize=4)
    plt.errorbar([0,1,2,3,4,5],[P_ARGILE[i] for i in [0,1,2,3,4,5]],yerr=[P_ARGILE_err[i] for i in [0,1,2,3,4,5]],color="brown",capsize=4)
    plt.errorbar([3,5],[INALT[i] for i in [3,5]],yerr=[INALT_err[i] for i in [3,5]],color="green",capsize=4)
    plt.show()







