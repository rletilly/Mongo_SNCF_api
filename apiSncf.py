import requests
import json , os
from datetime import date, time, datetime
import pymongo

#URL to connect to test API
#https://canaltp.github.io/navitia-playground/play.html?request=https%3A%2F%2Fapi.navitia.io%2Fv1%2Fcoverage%2Fsncf%2Fcommercial_modes%2Fcommercial_mode%253AINOUI%2Flines%3F

os.system("clear")
url = "http://api.navitia.io/"

#Lecture du fichier api_key
def import_key():
    with open('api_key.json') as json_data:
        data_dict = json.load(json_data)
        return data_dict
#On attribue la clé
api_key = import_key()['api_key']
#Dictionnaire de requetes
requetes = {}
requetes["TGV_INOUI"] = "https://api.navitia.io/v1/coverage/sncf/commercial_modes/commercial_mode%3AINOUI/departures?"
requetes["TGV_OUIGO"]= "https://api.navitia.io/v1/coverage/sncf/commercial_modes/commercial_mode%3Aouigo/departures?"
requetes["TGV_THALYS"]= "https://api.navitia.io/v1/coverage/sncf/commercial_modes/commercial_mode%3Athalys/departures?"
#Fonction de date
def cutDateTime(date):
    return {'date':date[0:8],'hour':date[9:11],'min':date[11:13],'sec':date[13:]}
#Connection a mongodb
client = pymongo.MongoClient('localhost',27017)
mydb = client["SNCF"]
mycoll = mydb["Train"]
mycoll2 = mydb["Problemes"]


#Une requete
data = []
data.append(requests.get(requetes["TGV_INOUI"],auth = (api_key," ")).json())
data.append(requests.get(requetes["TGV_OUIGO"],auth = (api_key," ")).json())
data.append(requests.get(requetes["TGV_THALYS"],auth = (api_key," ")).json())




for requete in data : 
    BigData = []
    for i in range(len(requete['departures'])):
        try : 
            train = {}
            train["heure_depart"] = cutDateTime(str(requete['departures'][i]['stop_date_time']['departure_date_time']))['hour']+"h"+cutDateTime(str(requete['departures'][i]['stop_date_time']['departure_date_time']))['min']
            retardH = (int(cutDateTime(str(requete['departures'][i]['stop_date_time']['departure_date_time']))['hour']) - int(cutDateTime(str(requete['departures'][i]['stop_date_time']['base_departure_date_time']))['hour']))*60
            retardM = int(cutDateTime(str(requete['departures'][i]['stop_date_time']['departure_date_time']))['min']) - int(cutDateTime(str(requete['departures'][i]['stop_date_time']['base_departure_date_time']))['min'])
            train["retard"] = str((retardH+retardM))+"min"
            train["gare_depart"] = str(requete['departures'][i]['display_informations']['direction'])
            train["gare_arrivee"] = str(requete['departures'][i]['stop_point']['name'])
            mtn = datetime.now()
            train["date"] = str(mtn.day)+"/"+str(mtn.month)+"/"+str(mtn.year)
            train['id_route'] = str(requete['departures'][i]['route']['id'])
            train["type"] = str(requete['departures'][i]['display_informations']['commercial_mode'])
            BigData.append(train)
            print(train)
        except:
            print("An exception occurred")
    #On envoie les données 
    #print('insert')
    #mycoll.insert_many(BigData)
    #print('done')

    #Ajout des problemes
    BigData2 = []
    for i in range(len(requete['disruptions'])):
        try : 
            probleme = {}
            heure_b = cutDateTime(str(requete['disruptions'][i]['application_periods'][0]['begin']))['hour']
            minute_b = cutDateTime(str(requete['disruptions'][i]['application_periods'][0]['begin']))['min']
            heure_e = cutDateTime(str(requete['disruptions'][i]['application_periods'][0]['end']))['hour']
            minute_e =cutDateTime(str(requete['disruptions'][i]['application_periods'][0]['end']))['min']

            probleme['heure_arrive'] = heure_e+"h"+minute_e
            probleme['heure_depart'] = heure_b+"h"+minute_b
            mtn = datetime.now()
            probleme["date"] = str(mtn.day)+"/"+str(mtn.month)+"/"+str(mtn.year)
            probleme['gare_arrive'] = str(requete['disruptions'][i]['impacted_objects'][0]['impacted_stops'][len(requete['disruptions'][i]['impacted_objects'][0]['impacted_stops'])-1]['stop_point']['name'])
            probleme['gare_depart'] = str(requete['disruptions'][i]['impacted_objects'][0]['impacted_stops'][0]['stop_point']['name'])
            probleme['incident'] = requete['disruptions'][i]['messages'][0]['text']
            BigData2.append(probleme)
            print(probleme)
        except:
            print("An exception occurred")
    #On envoie les données 
    #print('insert')
    #mycoll2.insert_many(BigData2)
    #print('done')


    




