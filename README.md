# TPE POO GROUP 14
Une application sur la gestion d'une banque

## Conditions préalables

Le programme fonctionne sur uniquement sur **python3**. Nous vous conseillons d'installer de preferance python3.6, pour telecharger python3.6, suivez ce lien [https://www.python.org/ftp/python/3.6.8/python-3.6.8-amd64.exe](https://www.python.org/ftp/python/3.6.8/python-3.6.8-amd64.exe).

Il faudra aussi install virtualenv pour creer un environment virtuel.
Pour install virtuelenv tapez :
- `pip3 install virtualenv`

## Executer le code
Pour executer le code, suivez le etapes suivants :

#### creer un environment virtuel
- linux : `virtualenv -p python3.6 venv`
- windows: `virtualenv -p py venv`
> sur windows veillez verifie que la version de python est bien 3.6

#### active l'environment virtuel
Pour active l'environment virtual, tapez la commande :
- linux : `source venv/bin/activate`
- windows: `.\venv\Scripts\Activate.bat`
> sur windows, veillez vous placez dans le repertoire du project
> cette commande n'est valable que pour cmd sur windows

#### installation des dependances
pour installer les dependances du programme, utilisez la commande :
- `pip3 install -r requirements.txt`
> il est possible que l'installation produise une erreur si votre version de python n'est pas 3.6

##### Lancer l'application
pour lancer l'application, executer la commande : 
- linux: `python3 main.py`
- windows: `py main.py`

## construit avec: 
- [PyQt5](https://www.riverbankcomputing.com/software/pyqt/) - le framework utilise pour l'interface graphique
- [SqlAlchemy](https://www.sqlalchemy.org/) - l'ORM utilise pour la laison a la base de donnnees

## Contribuant

- Ousmane Hamadou
- Youmbi Kuate Lauraine   https://youtu.be/-QZ_1XKaUzU
- Oumar Hassane Adoum
- Tomte Fidel
- Fissou Henri Joel
- Taiki Payang Parfait
- Idriss Adoum Idriss
- Al-mine Oro Kondi
- Ibrahim Saleh Annour Aldjabir
- Ammanuel Bollah

## Remerciements
- les developpeurs de PyQt5 et SqlAlchemy
- Dr-Ing Franklin Tchakounte
