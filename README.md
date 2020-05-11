# mongoSncfApi
# Projet Final de Mongodb avec utilisation de l'API Sncf

## Les commentaires de l'équipe

Dans ce repo vous pourrez trouver quelques fichier python : 

**apiSncf.py** contient le code dans lequel nous allons demander les informations sur trois types de trains. Pour construire notre base de données, nous avons fait tourner ce code à plusieurs reprise pendant de longs intervalles de temps sur une raspberry.

**projectMainScript.py** Dans ce fichier vous pourrez trouver le menu et une fonction à n'utiliser que lorsque votre donné est brute et non traitée. Elle contient toutes les fonctions de traitement de nos données.

**mongoFunctions.py** ce fichier contient toutes les query auxquelles vous allez faire appel ou que vous allez créer de vous même ;)

Et deux fichiers Json : 

**Probleme.json / train.json** Dans le cas ou vous n'avez pas de clé pour l'API sncf nous vous laissons accès à un premier jet de données recoltées. Elle vous serviront pour tester notre programme

## Comment commencer 
**Ouvrez une invite de commandes**

```bash
cd C:\Program Files\MongoDB\Server\4.2\bin
mongo
db
use finalProject
db.createCollection("train")
db.createCollection("problemes")
```
C'est tout pour l'invite de commande !!

## Utiliser le code
**Si vous possedez une clée sncf, lancez les fonctions du fichier apiSncf**
Il est important de n'utiliser cette fonction qu'une fois lorsque les données sont brutes. Une fois utilisée, commenter là et n'y faites plus attention.

```python
#d'abord 
run_once()
#let_run()

#Puis
#run_once()
let_run()
```
let_run() est la fonction qui vous amènera au menu.

## Notre étude
Les données fournies par la sncf sont remplies d'information non désireables qu'il a fallut traiter avant de pouvoir les utiliser réellement.
Nous avons choisit l'étude des trains évoluants sur grandes lignes partout en france et dans les pays deservit par les Thalys.
Nous avons concentré notre étude sur les connexions existantes, les retards renseignés et les incidents notables.

C'est pourquoi en plus des informations sur les TGV INOUI / Thalys / OUIGO nous avons aussi pris les incidents notables.
Nos query font quelques observations sur les retards moyens ou la fréquentation d'une certaine gare.
En conclusion, l'API de la sncf est intéressante mais ne fournit pas un panel d'informations renouvelées souvent ou même facilement compréhensible. 
