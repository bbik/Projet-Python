import csv
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import math
#f = open("C:\Users\ikram\Downloads\EIVP_KM.csv", "r")
#fichierCSV = csv.reader(f)
#print(fichierCSV)
fichierCSV=pd.read_csv(r"C:\Users\ikram\Downloads\EIVP_KM.csv",sep=';')
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
def display(variable,debut=None,fin=None):
    plt.title('Evolution de la variable dans le temps')
    plt.xlabel('Temps')
    temps_seconde=[]
    for i in range (len(temps)):
        temps_seconde.append(trseconde(str(temps[i])))
    if debut==None or fin==None:
        plt.plot(temps_seconde,variable)    
        plt.show()
    else:
        d=temps.index(debut)
        f=temps.index(fin)
        duree=temps_seconde[d:f]
        variable_duree=variable[d:f]
        plt.plot(duree,variable_duree)
        plt.show()
        

