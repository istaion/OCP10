# OCP10

Créez une API sécurisée RESTful en utilisant Django REST

## instalation

Dans votre terminal placez-vous à la racine du projet puis :

### Créer votre environnement virtuel :


```bash
python3 -m venv env
```

### Activer votre environnement :

linux ou mac :
```bash
source env/bin/activate
```

windows :

```bash
env\\Scripts\\activate.bat
```

### Installer les packages :

```bash
pip install -r requirements.txt
```

## Utilisation :

### Génerer les migrations :

```bash
python manage.py makemigrations projects authentication
```
```bash
python manage.py migrate
```

### Lancer le serveur :

```bash
python manage.py runserver
```

### API :

Vous pouvez retrouver les points d'accés dans la doc :
[documentation API](https://documenter.getpostman.com/view/15931927/2s93CHuvQ9)

