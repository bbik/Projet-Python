import csv
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import math
#f = open("C:\Users\ikram\Downloads\EIVP_KM.csv", "r")
#fichierCSV = csv.reader(f)
#print(fichierCSV)

fichierCSV=pd.read_csv("EIVP_KM.csv",sep=';', index_col='ID', parse_dates=True)
frame=pd.DataFrame(fichierCSV)
columns=frame.columns #renvoie l'intitulé des colonnes avec : print(columns)
print(fichierCSV)

#declaration des variables
temps=fichierCSV['sent_at'].to_list()
temperature= fichierCSV['temp'].to_list()
humidite=fichierCSV['humidity'].to_list()
niv_sonore= fichierCSV['noise'].to_list()
niv_lum=fichierCSV['lum'].to_list()
quantite_CO2=fichierCSV['co2'].to_list()
humidex = 'humidex'

#constantes pour le calcul de l'indice humidex
cste = 17.27
cste2 = 237.7 #°C
cste3 = 5417.7530

def trseconde(a):
    b=str(a).split()
    c=b[0].split("-")
    jour=c[2]
    d=b[1].split("+")
    e=d[0].split(":")
    heure=e[0]
    minute=e[1]
    seconde=e[2]
    heureseconde=int(heure)*3600
    minuteseconde=int(minute)*60
    reference=int(jour)-11
    resultat=reference*24*3600+heureseconde+minuteseconde+int(seconde)
    return(resultat)
def fusion (L1,L2):
    if L1==[]:
        return L2
    elif L2==[]:
        return L1
    elif L1[0]<L2[0]:
        return [L1[0]]+fusion(L1[1:],L2)
    else:
        return [L2[0]]+fusion(L1,L2[1:])
def tri_fusion(L):
    if len(L)<=1:
        return L
    else:
        n=len(L)
        L1=L[:n//2]
        L2=L[n//2:]
        return fusion(tri_fusion(L1), tri_fusion(L2))


def display(variable,debut=None,fin=None):
    plt.title('Evolution de la variable dans le temps')
    plt.xlabel('Temps')
    temps_seconde=[]
    for i in range (len(temps)):
        temps_seconde.append(trseconde(str(temps[i])))
    temps_seconde=tri_fusion(temps_seconde)
    if variable!=humidex:
        if debut==None or fin==None:
            plt.plot(temps_seconde,variable)
        else:
                d = temps.index(debut)
                f = temps.index(fin)
                duree = temps_seconde[d:f]
                variable_duree = variable[d:f]
                plt.plot(duree,variable_duree)
                plt.show()
        
# indice humidex
    phi=[]
    Trosee=[]
    Humidex=[]
    
    if variable==humidex: 
        if debut==None or fin==None:
            print('Entrer dates')
        else:
            d = temps.index(debut)
            f = temps.index(fin)
            
 #calcul de la fonction phi en fonction de la temperature de l'air Tair et de l'humidite relative HR
            for Tair,RH in zip(temperature[d:f],humidite[d:f]):
                phi.append(((cste*Tair)/(cste2+Tair))+math.log(RH/100))
                
 #calcul de la temperature de rosee (en fonction de la valeur de phi)
            for i in range(len(phi)):
                Trosee.append((cste2*phi[i])/(cste-phi[i]))
            #print('Temperature de rosee = ',Trosee, "\n") 
            
 #calcul indice humidex
            for Tair, Tr in zip(temperature[d:f],Trosee):
                Humidex.append(Tair + 0.5555*(6.11*math.exp(cste3*((1/273.16)-(1/(273.15+Tr))))-10))
            print('Indice humidex = ', Humidex)
            
#affichage de l'indice humidex en fonction du temps
            duree = temps_seconde[d:f]
            plt.plot(duree,Humidex)
            plt.show()
 

def displayStat(variable, debut= None, fin= None):
#affichage des valeurs statistiques

    plt.title('Evolution de la variable dans le temps')
    plt.xlabel('Temps')
    
    temps_seconde=[]
    d = temps.index(debut)
    f = temps.index(fin)
    duree = temps_seconde[d:f]
    variable_duree = variable[d:f]
    
    for i in range (len(temps)):
        temps_seconde.append(trseconde(str(temps[i])))
     
    if variable!=humidex:
        if debut==None or fin==None:
            plt.plot(temps_seconde,variable)
        else:
            plt.plot(duree,variable_duree)
           

#affichage de la valeur minimale de la variable

        print('Valeur minimale :',min(variable_duree), "\n")
#index correspondant à la valeur min de la variable :
        index_min = variable.index(min(variable_duree))
#point min
        plt.annotate("Minimum",xy=(duree[index_min],min(variable_duree)),xytext=(duree[index_min]+30000,min(variable_duree)),arrowprops=dict(facecolor='black', arrowstyle='->'))
    
        
#affichage de la valeur maximale de la variable    
        print('Valeur maximale :',max(variable_duree), "\n")
        index_max = variable.index(max(variable_duree))
        plt.annotate("Maximum",xy=(duree[index_max],max(variable_duree)),xytext=(duree[index_max]+30000,max(variable_duree)),arrowprops=dict(facecolor='black', arrowstyle='->'))

#affichage de la valeur médiane de la variable

        print('Valeur médiane :',np.median(variable_duree), "\n")
#index correspondant à la valeur médiane de la variable :
        index_med = variable.index(np.median(variable_duree))
#point médiane
        plt.annotate("Médiane",xy=(duree[index_min],np.median(variable_duree)),xytext=(duree[index_med]+30000,np.median(variable_duree)),arrowprops=dict(facecolor='black', arrowstyle='->'))

        print('Valeur moyenne :',np.mean(variable_duree), "\n")
        
#affichage de la valeur écart-type de la variable

        print('Valeur écart-type :',np.std(variable_duree), "\n")

#affichage de la variance de la variable

        print('Valeur variance :',np.var(variable_duree), "\n")    
    

def correlation(variable1,variable2, debut= None, fin= None):

    if len(variable1) != len(variable2):
        print('erreur')

#calcul des écarts types de la variable1 et de la variable2
    ecart_type1 = np.std(variable1)
    ecart_type2 = np.std(variable2)
    
#calcul des moyennes de la variable1 et de la variable2
    moy1 = np.mean(variable1)
    moy2 = np.mean(variable2)
    
#calcul covariance variable1
    sum=0
    n=len(variable1)
    for i in range(0,n):
        sum += ((variable1[i]-moy1)*(variable2[i]-moy2))
    Cov=sum/(n)
    print('Covariance :',Cov,"\n")
    
#calcul indice de corrélation
    ind_correlation=Cov/(ecart_type1*ecart_type2)
    print('Indice de correlation :', ind_correlation)
    
    
#affiche du titre du graphique et du nom des axes
    plt.title('Evolution des variables dans le temps')
    plt.xlabel('Temps')
    
    temps_seconde=[]
    d = temps.index(debut)
    f = temps.index(fin)
    duree = temps_seconde[d:f]
    variable_duree1 = variable1[d:f]
    variable_duree2 = variable2[d:f]
    
    for i in range (len(temps)):
        temps_seconde.append(trseconde(str(temps[i])))
     
    if variable1!=humidex and variable2!=humidex:
        if debut==None or fin==None:
            plt.plot(temps_seconde,variable1)
            plt.plot(temps_seconde,variable2)
        else:
                plt.plot(duree,variable_duree1, color="blue")
                plt.plot(duree,variable_duree2, color="red")
                plt.legend(loc='upper left')
                plt.show()
          
        
def anomalies(variable, debut= None, fin= None):            
#detection anomalies

    temps_seconde=[]
    d = temps.index(debut)
    f = temps.index(fin)
    duree = temps_seconde[d:f]
    variable_duree = variable[d:f]
    
    for i in range (len(temps)):
        temps_seconde.append(trseconde(str(temps[i])))
    
#seuils des valeurs abberantes             
    Seuil_haut= np.median(variable_duree) + 3*np.std(variable_duree)
    Seuil_bas= np.median(variable_duree) - 3*np.std(variable_duree)
    
    L=variable_duree[d:f]
    anomalies=[]
    duree_anomalies=[]

#détection de ces valeurs     
    for i in range (len(L)):
         if L[i]>Seuil_haut or L[i]<Seuil_bas:
            anomalies.append(L[i])
            duree_anomalies.append(duree[i])
            
    if not(anomalies):
         print('Il ne semble pas y avoir de valeurs abberantes')
     
    plt.title('Evolution de la variable dans le temps')
    plt.xlabel('Temps')
    if variable!=humidex:
         if debut==None or fin==None:
              plt.plot(temps_seconde,variable)
         else:
              plt.plot(duree,variable_duree)
#affichage des anomalies
              plt.scatter(duree_anomalies,anomalies,c="red",linewidth = 0.5)
              plt.show()

