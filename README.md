# OCP12
# Projet démarré

# In progress

## Résumé du cahier des charges

- **Entreprise**: Epic Events, organisateur d'événements
- **Objectif**: Développer un logiciel CRM en Python 3.9+ pour la gestion des clients, contrats et événements.
- **Départements concernés**: Commercial, Support, Gestion
- **Sécurité et contraintes techniques**: Pas d'injections SQL, principe du moindre privilège, journalisation avec Sentry.
- **Livraison**: Dans un mois, en ligne de commande, avec une documentation d'implémentation.

### Données à gérer

- **Clients**: Nom, Email, Téléphone, etc.
- **Contrats**: ID unique, infos sur le client, montant, etc.
- **Événements**: ID, ID du contrat, nom du client, etc.

### Fonctionnalités

- **Tous les collaborateurs**: Accès en lecture seule à toutes les données
- **Équipe de gestion**: CRUD sur les collaborateurs, contrats et événements
- **Équipe commerciale**: Gestion des clients et contrats
- **Équipe support**: Filtrage et mise à jour des événements

---

## Quelques idées pour le guide d'implémentation

### Architecture générale

- Utiliser un modèle MVC (Modèle-Vue-Contrôleur) pour séparer les responsabilités
- Base de données POSTGRES SQL pour un prototype rapide (en gardant à l'esprit les contraintes de sécurité)

### Authentification

- Utilisation de jetons JWT pour authentifier les collaborateurs

### Département Commercial

- Interface en ligne de commande pour ajouter/mettre à jour les clients et contrats
- Filtres de recherche pour les contrats non signés, etc.

### Département Support

- Interface pour filtrer et mettre à jour les événements qui leur sont attribués
- Notifications pour les changements d'état des événements

### Département Gestion

- Interface admin pour la gestion des collaborateurs, contrats et événements
- Filtres pour afficher les événements sans support, etc.

### Sécurité

- Utilisation de requêtes paramétrées pour prévenir les injections SQL
- Implémentation du principe du moindre privilège via des rôles et permissions

### Journalisation

- Intégration de Sentry pour capturer les erreurs et exceptions

# Diagram
```mermaid
erDiagram
    Client ||--o{ Contract : has
    Employee ||--o{ Contract : manages
    Employee ||--o{ Event : organizes
    Contract ||--o{ Event : results_in
    Client {
        int id
        string full_name
        string email
        string phone
        string company_name
        date first_contact
        date last_update
        int commercial_contact_id
    }
    Contract {
        int id
        int client_id
        int commercial_id
        float total_amount
        float amount_to_be_paid
        date creation_date
        string status
    }
    Employee {
        int id
        string full_name
        string email
        date creation_date
        string department
    }
    Event {
        int id
        int contract_id
        int support_contact_id
        date start_date
        date end_date
        string location
        int attendees
        string notes
    }

```

### 1. Installation de PostgreSQL et PgAdmin:

- PostgreSQL:


``` Shell
sudo dnf update sudo dnf install postgresql-server postgresql-contrib
```

Après l'installation, initialiser la base de données:

``` Shell
sudo postgresql-setup --initdb
```

Puis démarrer et activer le service:

```shell
sudo systemctl start postgresql sudo systemctl enable postgresql
```

- PgAdmin:

```Shell
sudo dnf install pgadmin4
```
### 2. Créer une nouvelle base de données:

- En Shell :
- TO DO : lister les commandes pour créer et configurer les droits sur la DB

``` Shell
 psql -U postgres -h localhost -d epic_events

```


- Crée une nouvelle base de données avec le nom : `epic_events`.

### 3. Créer un utilisateur pour l'application:

- Créer un nouvel utilisateur (ou "Role" dans le jargon PostgreSQL).
- Attribuer un nom et un mot de passe et assurer les droits suffisants sur la base de données epic_events.


### 5. Configurer les variables d'environnement:

- Les informations de connexion à la base de données dans des variables d'environnement pour des raisons de sécurité. Nous utilisons la librairie  `dot_env`

### 6. Créer un environnement virtuel Python:

- Dans le répertoire où tu vas stocker ton projet, crée un environnement virtuel:


    ``` Python
    python3 -m venv .env
    ```

- Activer l'environnement:


   ``` Shell
   source .env/bin/activate
   ```

- Installer les dépendances comme `SQLAlchemy` et `Dot_env`:
### Créer un fichier pour les variables d'environnement

1. **Crée un fichier `.env` dans le répertoire de ton projet**. Ce fichier contiendra tes variables d'environnement.


   ``` Shell
   touch .env
   ```


1. **Ouvrir ce fichier avec un éditeur de texte** et ajouter les variables.

- Par exemple :

``` Shell
DATABASE_URL=postgresql://username:password@localhost/dbname SECRET_KEY=mysecretkey

DATABASE_URL=postgresql://user:Password@localhost/epic_events
EPICEVENTS_USER=user
EPICEVENTS_PW=Password
EPICEVENTS_SK=mySecretKey
```

Ici, `username` et `password` sont ceux que tu as définis lors de la création de l'utilisateur PostgreSQL, et `dbname` est le nom de la base de données que tu as créée.


### Charger les variables d'environnement dans ton application

1. **Installer la librairie `python-dotenv`**: Cette librairie permet de charger les variables d'environnement depuis un fichier `.env` dans le projet.
```Shell
pip install python-dotenv
```

2. **Charger les variables dans le code Python**:

``` Python
from dotenv import load_dotenv import os  load_dotenv()  database_url = os.getenv("DATABASE_URL") secret_key = os.getenv("SECRET_KEY")
```

Ici, `load_dotenv()` lit le fichier `.env` et charge les variables pour les utiliser avec `os.getenv().


# A SUIVRE - In Progress