# Description de l'application

Ce projet consiste à développer une API sécurisée pour une application de gestion de relation
client (CRM) via une interface front-end (site d'administration Django) et un ensemble de points de terminaison.

## Lancement de l'application

* Ouvrez un invite de commande
* Placez-vous dans le dossier contenant le répertoire ProjetOC_12
* Création de l'environnement virtuel : ```python -m venv env```
* Activation de l'environnement virtuel :
    * Pour Windows : ```env\Scripts\activate.bat```
    * Pour Linux   : ```env/bin/activate```
* Installation des dépendances : ```pip install -r requirements.txt```
* Restaurez-la database oc_12_db : utiliser un outil de restoration postgresql
* Ouvrez le fichier setting.py et configurer votre database :
```
  DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '<database_name>',
        'USER': '<user>',
        'PASSWORD': '<password>',
        'HOST': 'localhost',
        'PORT': '<port>'
    }
  }
```
* Lancement du serveur local : ```python manage.py runserver```
* Connectez-vous au site d'administration django : http://127.0.0.1:8000/admin/

Il existe déjà 3 comptes :

Compte administrateur : Login : admin / Password : admin
* Utilisez ce compte pour ajouter de nouveau compte administrateur ou ajouter des utilisateurs en leur associant
un des deux groupes possibles (sales_group, support_group), ces utilisateurs auront ensuite accés au site
  d'administration Django et à l'ensemble des points de terminaison.

Compte vente : Login : Quentin / Password : GxA784NTS

Compte support : Login : Alex / Password : GxA784NTS

### Points de terminaison

La documentation des points de terminaison sont accéssible ici : https://documenter.getpostman.com/view/16912752/UVJWpKQo

