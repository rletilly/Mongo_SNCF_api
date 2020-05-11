import pymongo
import os
from mongoFunctions import *  #Created by us
clear = lambda: os.system('clear') #on Mac System
#clear = lambda: os.system('cls') #on windows System
clear()

#Connection to mongodb
client = pymongo.MongoClient('localhost',27017)
db = client["finalProject"]
train = db["train"]
problemes = db["problemes"]

print("Bienvenue dans notre projet de NoSQL DBS.")
print("Pour toutes informations autres que le fonctionnement les fonction allez dans le README.")
#Liste des elements : 
#"retard","gare_arrivee","type","gare_depart","heure_depart","id_route","date"

def run_once():
    #Just configuring the database
    path = input("Quel est le path des fichiers train.json et problemes.json ?")
    importData(path) #If you are not using a Unix system it will not work (os.system not available on Windows)
    #On windows, every database import has to be done trough command line in your bin repo or with this function :

    #path = input("Quel est le path des fichiers train.json et problemes.json ?")
    #importDataWindows(path)

    deleteDuplicateTrain(db = db,client = client, train = train)
    deleteDuplicatePb(client=client,db=db,problemes=problemes)
    temps_perdu()
    changing_minute()
    convert_toint()

    
def let_run():
    la_suite = 'o'
    while(la_suite != 'n'):
        toutes_gares = ["Tourcoing (Tourcoing)","Menton (Menton)","Bar-le-Duc (Bar-le-Duc)","Dunkerque (Dunkerque)","Grenoble (Grenoble)","Essen-Hbf (Essen)","Bordeaux-St-Jean (Bordeaux)","Nancy-Ville (Nancy)",
        "Paris Gare du Nord (Paris)","Milano-Porta-Garibaldi (Milano)","Perpignan (Perpignan)","Poitiers (Poitiers)","Nice-Ville (Nice)","Marseille-St-Charles (Marseille)",
        "Miramas (Miramas)","Paris-Gare-de-Lyon (Paris)","Hendaye (Hendaye)","Aéropt-C-de-Gaulle-TGV (Le Mesnil-Amelot)","Lille Europe (Lille)","St-Malo (Saint-Malo)",
        "Paris-Montparnasse 1-2 (Paris)","Nantes (Nantes)","Brest (Brest)","Toulouse-Matabiau (Toulouse)","Rennes (Rennes)","Amsterdam-Centraal (Amsterdam)",
        "Lyon-Perrache (Lyon)","Bruxelles-M./Brussel-Z. (Saint-Gilles - Sint-Gillis)","arne-la-Vallée-Chessy. (Chessy)","Tarbes (Tarbes)","Remiremont (Remiremont)",
        "Mulhouse (Mulhouse)","Lyon-Part-Dieu (Lyon)","Strasbourg (Strasbourg)","Montpellier-Sud-France (Montpellier)","Paris-Est (Paris)","Boulogne Ville (Boulogne-sur-Mer)",
        "Valenciennes (Valenciennes)","Dortmund-Hbf (Dortmund)"]

        print("Que voulez-vous faire : \n (1)-Compter le nombre de lignes de la collection train \n (2)-Compter le nombre de lignes de la collection problèmes \n",
        "(3)-Sélectionnez tous les départs d'une certaine gare \n (4)-Le nombre de trains partant d'une gare à une heure donnée \n",
        "(5)-Montrez moi toutes les gare de départ de TGV INOUI \n (6)-Quand commence et finit notre BD \n",
        "(7)-Quelle est la ligne la plus souvent en panne \n (8)-Quels sont les problèmes récurrents \n",
        "(9)-En moyenne, de combien de temps un incident retarde t-il un train ? \n (10)-Voulez-vous placer un index quelque part ? \n",
        "(11)-Quel type de train a le plus gros retard ? \n (12)-Quel type de train passe par quelles lignes \n",
        "(13)-Combien de train partent par jour ? \n (14)-Quelles sont les connexions connues d'une gare ? \n",
        "(15)-Faire un test de $lookup \n (16)-Créer votre propre query !!! \n")
        choice = input()
        print(choice)
        clear()
        if (choice == "1"):
            clear()
            a = db.train.estimated_document_count()
            print(a)
        if (choice == "2"):
            clear()
            b = db.problemes.estimated_document_count()
            print(b)
        if (choice == "3"):
            clear()
            #Sélectionnez tous les départs d'une certaine gare 
            print("Voici le choix de vos gares : ")
            for i in range(0,len(toutes_gares)):
                print("("+str(i+1)+")-"+toutes_gares[i])
            choix2 = input ("De quelle gare partez vous : ")
            gare = toutes_gares[int(choix2)-1]
            depart_gare(gare)
        if (choice == "4"):
            clear()
            #A quelle heure partez-vous et de quelle gare ?
            heure = input("A quelle heure partez-vous ? (xxhxx)")
            print("Voici le choix de vos gares : ")
            for i in range(0,len(toutes_gares)):
                print("("+str(i+1)+")-"+toutes_gares[i])
            choix2 = input ("De quelle gare partez vous : ")
            gare = toutes_gares[int(choix2)-1]
            d = train_heure_depart(heure, gare)
        if (choice == "5"):
            clear()
            #Montrez moi toutes les gare de départ de TGV INOUI - e
            depart_INOUI()
        if (choice == "6"):
            clear()
            #Quelle est l'étendue de notre bds - f
            nos_dates()
        if (choice == "7"):
            clear()
            #Quelle est la ligne la plus souvent en panne - g
            pb_trajet()
        if (choice == "8"):
            clear()
            #Quels sont les problèmes récurrents - h
            type_pb()
        if (choice == "9"):
            clear()
            #En moyenne, de combien de temps un incident retarde t-il un train ? - i
            avg_late()
        if (choice == "10"):
            clear()
            #Souaitez-vous poser un index qq part - j
            Set_index()
        if (choice == "11"):
            clear()
            #Quel type de train a le plus gros retard - k
            best_retarde()
        if (choice == "12"):
            clear()
            #Chaque type de train passe par quelles lignes - l
            traing = input("Quel type de train voulez-vous voir ? TGV INOUI / Thalys / OUIGO")
            vos_lignes(traing)
        if (choice == "13"):
            clear()
            #Combien de train partent par jour - m
            nb_train_jour()
        if (choice == "14"):
            clear()
            #Quelles sont les destinations connues d'une gare - n
            print("Voici le choix de vos gares : ")
            for i in range(0,len(toutes_gares)):
                print("("+str(i+1)+")-"+toutes_gares[i])
            choix2 = input("De quelle gare voulez-vous connaitre les connexions ?")
            gare = toutes_gares[int(choix2)-1]
            connexion(gare)
        if (choice == "15"):
            clear()
            #Quels sont tous les trains ayant le plus d'accidents  ? - o
            voyage_rate() 
        if (choice == "16"):
            clear()
            #Créez votre propre query
            print("Voici le choix de vos gares : ")
            for i in range(0,len(toutes_gares)):
                print(toutes_gares[i])
            your_simple_query()
        print("Voulez-vous continuer ? (o/n)")
        la_suite =input()
        clear()

################     run_once ne doit être lancée qu'une seule fois     #######################
#run_once()
################                                                        #######################
let_run()