import pymongo
import os
from bson import ObjectId
import json

client = pymongo.MongoClient('localhost',27017)
db = client["finalProject"]
train = db["train"]
problemes = db["problemes"]

## Ne marche qu'avec UNIX 
def importData(path):
    #This function importe all data we need
    os.system("mongoimport  --db finalProject --collection train --jsonArray --file "+path+"/train.json")
    os.system("mongoimport  --db finalProject --collection problemes --jsonArray --file "+path+"/probleme.json")

def importDataWindows(path):
    #C:\Users\ronan\Documents\ing4\semestre_2\Nosql\mongoSncfApi
    pa1 = path+"/train.json"
    pa2 = path+"/probleme.json"
    pa1.replace('\\', '/')
    pa2.replace('\\', '/')
    with open(pa1) as f:
        file_data = json.load(f)
    train.insert_many(file_data)
    with open(pa2) as f:
        file_data = json.load(f)
    problemes.insert_many(file_data)

#This function delete the duplicates of the train database
def deleteDuplicateTrain(client,db,train):
    cursor = db.train.aggregate(
    [
        {"$group": {
            "_id": { "gare_depart": "$gare_depart", "date": "$date","gare_arrivee": "$gare_arrivee" ,"heure_depart": "$heure_depart" },
            "unique_ids": {"$addToSet": "$_id"}, 
            "count": {"$sum": 1}
        }},
        {"$match": {"count": { "$gte": 2 }}}
    ]
    )
    response = []
    for doc in cursor:
        del doc["unique_ids"][0]
        for id in doc["unique_ids"]:
            response.append(id)

    train.remove({"_id": {"$in": response}})

#This function delete the duplicates of the probleme database
def deleteDuplicatePb(client,db,problemes):
    cursor = db.problemes.aggregate(
    [
        {"$group": {
            "_id": { "gare_depart": "$gare_depart", "date": "$date","gare_arrivee": "$gare_arrivee" ,"heure_depart": "$heure_depart" },
            "unique_ids": {"$addToSet": "$_id"}, 
            "count": {"$sum": 1}
        }},
        {"$match": {"count": { "$gte": 2 }}}
    ]
    )
    response = []
    for doc in cursor:
        del doc["unique_ids"][0]
        for id in doc["unique_ids"]:
            response.append(id)

    problemes.remove({"_id": {"$in": response}})

#This function is exclusively to insert a new field of how much time they've lost 
def temps_perdu():
    i = db.problemes.find()
    for doc in i:
        h_dep = doc['heure_depart']
        h_arr = doc['heure_arrive']
        delta_temps = abs((int(h_dep[:2]) * 60 + int(h_dep[-2:])) - (int(h_arr[:2]) * 60 + int(h_arr[-2:])))
        db.problemes.update({"_id" :ObjectId(doc["_id"])},{'$set' : {"temps_perdu" : delta_temps}})

#On enlève le préfixe min aux minutes
def changing_minute():
    k = db.train.find()
    for doc in k:
        if (len(doc['retard']) == 5):
            db.train.update({"_id" :ObjectId(doc["_id"])},{'$set' : {"retard" : doc['retard'][:2]}})
        else:
            db.train.update({"_id" :ObjectId(doc["_id"])},{'$set' : {"retard" : doc['retard'][:1]}})

#On converti les minutes en int 
def convert_toint():
    k = db.train.find()
    for doc in k:
        db.train.aggregate([{'$project' : {'_id' : 0, 'retard' : { '$toInt' : '$retard'}}}])


def stopsListe(db,train) : 
    cursor = db.train.aggregate( 
        [{ "$group": { 
            "_id":"$gare_depart" } }
    ] )
    liste = list(cursor)
    liste2 = []
    for element in liste : 
        liste2.append(element['_id'])
    return liste2

def depart_gare (gare):
    try :
        a = db.train.count_documents({"gare_depart" :gare})
        print(a)
    except:
        print("An exception occurred") 

def train_heure_depart(heure, gare):
    try:
        b = db.train.count_documents({"gare_depart" :gare, "heure_depart" : heure})
        print(b)
    except:
        print("An exception occurred") 

def depart_INOUI():
    temp = db.train.find({"type" : "TGV INOUI"})
    for doc in temp:
        depart = doc["gare_depart"]
        print(depart)

def nos_dates():
    collec = db.train.find()
    length = db.train.estimated_document_count()
    start = collec[0]
    end = collec[length-1]
    print("La première date de notre bd est le : "+ start["date"])
    print("La dernère date de notre bd est : "+ end["date"])

def pb_trajet():
    # trouver tous les couples 
    g = db.problemes.aggregate([{'$group' : {'_id' : {'gare_depart' : "$gare_depart", 'gare_arrive' : "$gare_arrive"}}}])
    #occurrence max
    number1 = db.problemes.estimated_document_count()
    for doc in g:
        print(doc)
        number2 = db.problemes.count_documents({'gare_depart' : doc['_id']['gare_depart'],'gare_arrive' : doc['_id']["gare_arrive"]})
        proba_final = (number2*100)/number1
        print("Il y a "+str(proba_final)+'%'+" des incidents sur la ligne "+doc['_id']["gare_depart"]+" - "+doc['_id']["gare_arrive"])

def type_pb():
    h = db.problemes.aggregate([{'$group' : {'_id' : {'incident' : "$incident"}}}])
    number1 = db.problemes.estimated_document_count()
    for doc in h:
        number2 = db.problemes.count_documents({'incident' : doc['_id']['incident']})
        proba_final = (number2*100)/number1
        print(str(proba_final)+'%'+" des incidents sont du à "+doc['_id']["incident"])

def avg_late():
    i = db.problemes.aggregate([{'$group' : {'_id' : None, 'avg_temp' : {'$avg' : '$temps_perdu'}}}])
    for doc in i:
        heure = int(doc['avg_temp'])/60
        print("le temps moyen de récupération d'un traffit normale est de "+str(doc['avg_temp'])+"minutes")
        print("Soit "+str(heure)+" heures")
    
def Set_index():
    sete = input("Pour quel champs voulez-vous créer un index")
    try:
        db.train.createIndex({sete : 1})
    except:
        print("Il y a eu un pb, renseignez un champ valide.")

def best_retarde():
    k = db.train.aggregate([{'$group' : {'_id' : {'type' : '$type'} , 'maxi' : {'$max' : '$retard'}}}])
    for doc in k:
        print("Les trains de type "+doc["_id"]['type']+" ont pour plus grand retard : "+doc["maxi"]+" minutes")

def vos_lignes(traing):
    try :
        l =  db.train.aggregate([{'$group' :{'_id' :{'gare_depart' : '$gare_depart', 'gare_arrivee' : '$gare_arrivee'}}}])
        for doc in l:
            l2 = db.train.count_documents({'$and' : [{'type': traing}, {'gare_depart' : doc['_id']['gare_depart']}, {'gare_arrivee' : doc['_id']['gare_arrivee']}]})
            if l2 != 0:
                print("la route "+doc['_id']['gare_depart']+" - "+doc['_id']['gare_arrivee']+" est parcourue par le "+traing)
                l2 = 0
    except:
        print("Surement un mauvais nom de train !!")

def nb_train_jour():
    m = db.train.aggregate([{'$group' :{'_id' :{'date' : '$date'}, 'count' : { '$sum' :1}}}])
    for doc in m:
        print("A la date du "+doc['_id']['date']+", "+str(doc['count'])+" train sont partis de nos gares")

def connexion (gare):
    try:
        n = db.train.aggregate([{'$match' :{'gare_depart' : gare}},{'$group' : {'_id' : {'gare_arrivee' : '$gare_arrivee'}}}])
        print("Les connexions de "+gare+" sont : ")
        for doc in n:
            print(doc['_id']['gare_arrivee'])
    except:
        print("AH! une erreur semblerait-il") 

def voyage_rate():
    o = db.train.aggregate([{'$lookup' :{'from' : "problemes", 'localField' : "gare_depart", 'foreignField' : "gare_depart", 'as' : "pb_de_train"}}])
    for doc in o:
        if(doc['retard'] != "0"):
            print(doc)

def your_simple_query():
    champ_train = ["gare_depart","gare_arrivee","date","heure_depart","type","retard"]
    champ_pb = ["gare_depart","gare_arrive","heure_depart","date","incident","heure_arrive"]
    try:
        choix1 = input("Sur quelle collection voulez-vous faire votre query\n (1)-train \n (2)-problemes\n")
        choix2 = input("Choisissez :\n (1)-estimated_document_count()\n (2)-document_count()\n (3)-aggregate\n (4)-find()\n")
        
        #Si l'utilisateur choisi le nb de lignes de nos colections
        if (choix1 == "1" and choix2 == "1"):
            p = db.train.estimated_document_count()
            print(p)
        if(choix1 == "2" and choix2 == "1"):
            q = db.problemes.estimated_document_count()
            print(q)

        #Si l'utilisateur choisi le nb de documents d'une certaine valeur d'un champs donné
        #train
        if(choix1 == "1" and choix2 == "2" or choix2 == "4"):
            print("Voici le choix de vos champs : ")
            for i in range(0,len(champ_train)):
                print(champ_train[i])
            champ_1_2_1 = input ("Quel champs prenez-vous : ")
            print("Vous avez la liste des gares au-dessus, voici les trois types de train : TGV INOUI / Thalys / OUIGO",
            " l'heure doit respecter cette forme : (xxhxx) et la date : x/x/xxxx \n Renseignez votre choix : ")
            champ_1_2_2 = input()
            if(choix2 == "2"):
                r = db.train.count_documents({champ_1_2_1 : champ_1_2_2})
                print(r)
            if(choix2 == "4"):
                t = db.train.find({champ_1_2_1 : champ_1_2_2})
                print(t)
        #problemes
        if(choix1 == "2" and choix2 == "2" or choix2 == "4"):
            print("Voici le choix de vos champs : ")
            for i in range(0,len(champ_pb)):
                print(champ_pb[i])
            champ_2_2_1 = input ("Quel champs prenez-vous : ")
            print("Vous avez la liste des gares au-dessus l'heure doit respecter cette forme : (xxhxx) et la date : x/x/xxxx",
            "voila les types d'incident : Train en panne / Régulation du trafic / Travaux sur les voies / Difficultés lors de la préparation du train en gare",
            "\n Renseignez votre choix : ")
            champ_2_2_2 = input()
            if(choix2 == "2"):
                s = db.problemes.count_documents({champ_2_2_1 : champ_2_2_2})
                print(s)
            if(choix2 == "4"):
                u = db.problemes.find({champ_2_2_1 : champ_2_2_2})

        ##########aggregate#####
        if(choix2 == "3"):
            print("Vous avez le choix entre $group / $match / $sort")
            choix_x_3 = input()
            if(choix1 == "1"):
                print("Voici le choix de vos champs : ")
                for i in range(0,len(champ_train)):
                    print(champ_train[i])
                champ_1_3_1 = input ("Quel champs prenez-vous : ")
                if(choix_x_3 == "$group" or choix_x_3 =="$match"):
                    v = db.train.aggregate([{choix_x_3 : {champ_1_3_1 : '$'+champ_1_3_1}}])
                    for doc in v:
                        print(doc[champ_1_3_1])
                else:
                    w = db.train.aggregate([{choix_x_3 : {champ_1_3_1 : 1}}])
                    for doc in w:
                        print(doc[champ_1_3_1])
            if (choix1 == "2"):
                print("Voici le choix de vos champs : ")
                for i in range(0,len(champ_pb)):
                    print(champ_pb[i])
                champ_2_3_1 = input ("Quel champs prenez-vous : ")
                if(choix_x_3 == "$group" or choix_x_3 =="$match"):
                    x = db.problemes.aggregate([{choix_x_3 : {champ_2_3_1 : '$'+champ_2_3_1}}])
                    for doc in x:
                        print(doc[champ_2_3_1])
                else:
                    y = db.problemes.aggregate([{choix_x_3 : {champ_2_3_1 : 1}}])
                    for doc in y:
                        print(doc[champ_2_3_1])
    except:
        print("Un des arguments donnés doit être réorthographié")