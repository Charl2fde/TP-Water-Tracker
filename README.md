run the server

```bash
flask --app app run
```

init some data

```bash
flask --app main sample-data
```
Utilisation avec Docker

1. Construire l'image Docker
Exécutez cette commande à la racine du projet pour construire l'image :

```bash
docker build -t mon-app-python .
```

2. Lancer le conteneur
Une fois l'image construite, lancez un conteneur :

```bash
docker run -d -p 8000:5000 --name conteneur-app-python mon-app-python
```

3. Accéder à l'application
Votre application est maintenant prête et accessible sur http://localhost:8000.