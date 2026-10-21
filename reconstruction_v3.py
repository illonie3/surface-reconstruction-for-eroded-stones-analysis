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
from plotly.subplots import make_subplots



def getdatas(dossier):
    L=[]
    M=[]
    def onclick(event):
        L.append((int(event.xdata),int(event.ydata)))
        print(L)
    for image in os.listdir(dossier):
        M.append(image)
        fig, ax = plt.subplots()
        cid = fig.canvas.mpl_connect('button_press_event', onclick)
        img=np.array(Image.open(dossier+image))
        plt.imshow(img)
        plt.show()
        fig.canvas.mpl_disconnect(cid)
    if len(L)==0:
        L=[(0,0)]*len(M)
    return {M[k]:L[k] for k in range(len(L))}



def recadrer_normaliser(dossier):
    'nom du dossier suivi de /. Pointer une fois par image une infractuosité \n commune; si images identiques, fermer directement les fenêtres.'
    L=[]
    i=0
    D=getdatas(dossier)
    limx=min([D[k][0] for k in D])
    limy=min([D[k][1] for k in D])
    for image in os.listdir(dossier):
        i+=1
        print(i,'/',len(os.listdir(dossier))*2)
        img=np.array(Image.open(dossier+image))
        m=min([img.shape[0],img.shape[1]])
        img=Image.fromarray(img)
        img=img.crop((D[image][0]-limx,D[image][1]-limy,m+D[image][0]-limx,m+D[image][1]-limy))
        img.save(dossier+image)
        img=np.array(Image.open(dossier+image))
        L.append(luminosite(img))
    matrix=array([[[1,1,1] for i in range(m)]for k in range(m)],dtype=uint8)
    E=[k-80 for k in L]
    for image in os.listdir(dossier):
        i+=1
        print(i,'/',len(os.listdir(dossier))*2)
        img=np.array(Image.open(dossier+image))
        e=E[i-len(os.listdir(dossier))-1]
        img=img-e*matrix
        img[img > 255] = 255
        img[img < 0] = 0
        img=uint8(img)
        img=Image.fromarray(img)
        img.save(dossier+image)
def luminosite(img):
    return int(mean([sum(img[x,y])/3 for y in range(img.shape[1]) for x in range(img.shape[0])]))






##algorithme de reconstruction##   
def traitement(dossier):
    'nom du dossier suivi de /.'
    I,mask,S = read_data_file(dossier)
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

    plt.figure()
    rho = sqrt(M_1**2 + M_2**2 + M_3**2).reshape(I.shape[0],I.shape[1])
    plt.imshow(rho,cmap = plt.cm.gray)
    plt.title("2-D Image for albedo")

    n_1 = (M_1 / rho.reshape(-1)).reshape(I.shape[0],I.shape[1])
    n_2 = (M_2 / rho.reshape(-1)).reshape(I.shape[0],I.shape[1])
    n_3 = (M_3 / rho.reshape(-1)).reshape(I.shape[0],I.shape[1])

    z = unbiased_integrate(n_1,n_2,n_3,mask)

    #display_depth_matplotlib(z)
    #display_depth_mayavi(z)

    #plt.imshow()
    graphique1(dossier,z.shape[0],z)
    plt.show()
    a=histogram(z)[0]
    b=histogram(z)[1][:-1]
    plt.plot(b,a)
    print(histogram(z))
#    np.save(dossier+'mat_profondeur.npy',z) #permet de sauvegarder les matrices d'altitude pour la fonction graphique2
    plt.savefig(dossier+str(std(z))+".jpg")
    plt.show()


def graphique1(dossier,a,Z):
    X,Y=arange(0,a,1),arange(0,a,1)
    X,Y=meshgrid(X, Y)
    fig = go.Figure(data=[go.Surface(z=Z*70/0.8, x=X, y=Y)])
    fig.update_layout(title=dict(text='Surface'), autosize=False,
                  width=1500, height=700,
                  margin=dict(l=65, r=50, b=65, t=90))
    fig.update_layout(scene_aspectmode='manual',scene_aspectratio=dict(x=1, y=1, z=0.1))
    fig.write_html(dossier+'/reconstruction.html')
    fig.show()

def graphique2(dossier):
	"""
	nom dossier avec les 5 fichiers npy contenant les matrices d'altitude suivi de /
	"""
	Z = [0]*5
	L = os.listdir(dossier)
	for i in range(5):
		Z[i] = np.load(dossier+L[i])
	a = Z[0].shape[0]
	X,Y=arange(0,a,1),arange(0,a,1)
	X,Y=meshgrid(X, Y)
	for k in range(len(L)):
		nom = list(L[k])
		for i in range(len(nom)):
			if nom[i] == '_':
				nom[i] = ' '
			if nom[i] == 'z':
				nom[i] = 'é'
		L[k] = "<span style='text-decoration:underline;'>"+''.join(nom[:-4])+"</span>"
	fig = make_subplots(rows = 2, cols = 6,
					specs = [[{'colspan':3, 'is_3d': True},None, None, 
							{'colspan':3,'is_3d': True}, None, None],
							[{'colspan':2,'is_3d': True},None, 
							{'colspan':2, 'is_3d': True},None, 
							{'colspan':2, 'is_3d': True},None]],
					subplot_titles = L,
					)
	LPos = [(1, 1), (1, 4), (2, 1), (2, 3), (2, 5)]
	for i in range(5):
		Pos = LPos[i]
		fig.add_trace(go.Surface(z=Z[i]*70/0.8, x=X, y=Y, coloraxis = 'coloraxis'), Pos[0], Pos[1])
	fig.update_layout(coloraxis= dict(colorscale = 'Plasma', colorbar = dict(title = "<span style='text-decoration:underline;'>altitude en µm</span>")), showlegend = True)
	fig.update_scenes(dict(aspectmode = 'manual', 
						aspectratio = dict(x = 1.5, y = 1.5, z = 0.1),
						camera = dict(eye=dict(x=0., y=0., z=2.5))))
	fig.update_layout(title = dict(text = "<span style='text-decoration:underline;'><b>surface de calcaires dans différentes conditions</span>"))
	fig.write_html(dossier + 'comparaison_surfaces.html')
	fig.show()
		
