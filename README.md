# OCP12
# Projet démarré

# Contexte

Epic Events est une entreprise qui organise des événements (fêtes,
réunions professionnelles, manifestations hors les murs) pour ses clients. Ils souhaitent développer un logiciel CRM (Customer Relationship
Management) pour améliorer leur travail.
Le logiciel CRM permet de collecter et de traiter les données des clients
et de leurs événements, tout en facilitant la communication entre les
différents pôles de l'entreprise.

# Comment Epic Events fonctionne

Nos équipes opérationnelles sont divisées en trois départements :
● le département commercial
● le département support
● le département gestion

Les commerciaux démarchent les clients. Ils créent et mettent à jour
leurs profils sur la plateforme. Lorsqu’un client souhaite organiser un
événement, un collaborateur du département gestion crée un contrat et
l’associe au client.

# Exigences techniques et de sécurité

Vous devrez utiliser Python 3 (la version 3.9 ou une version plus
récente).
● L’application sera faite en ligne de commande.
● Vous devrez empêcher les injections SQL.
● Vous devrez mettre en œuvre et faire appliquer le principe du
moindre privilège lors de l'attribution de l'accès aux données.

Veillez à ce que les utilisateurs n'aient accès qu'aux données dont
ils ont besoin.

● Une journalisation utile et efficace sera mise en place avec Sentry :
les applications doivent consigner les exceptions et les erreurs
produites

Une fois le contrat signé, le commercial crée l’événement dans la
plateforme et le département gestion désigne un membre du
département support qui sera responsable de l’organisation et du
déroulé de l’événement.

# Estimation de livraison

L’application CRM doit être livrée dans deux mois.

# Les clients

| Information                        | Exemple               |
|------------------------------------|-----------------------|
| Nom complet                        | Kevin Casey           |
| Email                              | kevin@startup.io      |
| Téléphone                          | +678 123 456 78       |
| Nom de l’entreprise                | Cool Startup LLC      |
| Date de création (premier contact) | 18 avril 2021         |
| Dernière mise à jour/contact       | 29 mars 2023          |
| Contact commercial chez Epic Events| Bill Boquet           |

# Les contrats

Un contrat contient :
● un identifiant unique ;
● les informations sur le client ;
● le contact commercial pour le contrat (= le commercial associé au
client) ;
● le montant total du contrat ;
● le montant restant à payer ;
● la date de création du contrat ;
● le statut du contrat (= si le contrat a été signé).

# Les événements

À l’heure actuelle, le département support utilise une feuille Excel pour
suivre les événements. Voici deux exemples d’événements :

## Exemple 1

| A                 | B                                                  |
|-------------------|----------------------------------------------------|
| 1                 | John Ouick Wedding                                 |
| 2                 | Event ID 109                                       |
| 3                 | Contract ID 652                                    |
| 4                 | Client name John Ouick                             |
| 5                 | Client contact john.ouick@gmail.com <br>+1 234 567 8901 |
| 6                 | Event date start 4 Jun 2023 @ 1PM                  |
| 7                 | Event date end 5 Jun 2023 @ 2AM                    |
| 8                 | Support contact Kate Hastroff                      |
| 9                 | Location 53 Rue du Château, 41120 Candé-sur-Beuvron, France |
| 10                | Attendees 75                                       |
| 11                | Notes Wedding starts at 3PM, by the river. <br> Catering is organized, reception starts at 5PM. |

## Exemple 2

| A                 | B                                                               |
|-------------------|-----------------------------------------------------------------|
| 1                 | Lou Bouzin General Assembly                                     |
| 2                 | Event ID 1023                                                    |
| 3                 | Contract ID 412                                                  |
| 4                 | Client name Lou Bouzin                                           |
| 5                 | Client contact Jacky Blangier <br>jacky@loubouzin.grd <br>+ 666 12345 |
| 6                 | Event date start 5 May 2023 @ 3PM                                |
| 7                 | Event date end 5 May 2023 @ 5PM                                  |
| 8                 | Support contact Aliénor Vichum                                   |
| 9                 | Location Salle des fêtes de Mufflins                             |
| 10                | Attendees 200                                                    |
| 11                | Notes Assemblée générale des actionnaires (~200 personnes).      |

# Besoins et fonctionnalités

## Besoins généraux

| Exigence                                                        | Description                                                                                                                                                   |
|-----------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Identifiants pour chaque collaborateur                          | Chaque collaborateur doit avoir ses propres identifiants pour utiliser la plateforme.                                                                          |
| Association des collaborateurs à un rôle                        | Chaque collaborateur est associé à un rôle, dépendant de son département.                                                                                     |
| Stockage et mise à jour des informations                        | La plateforme doit permettre de stocker et de mettre à jour les informations concernant les clients, les contrats et les événements.                          |
| Accès en lecture seule pour tous les collaborateurs             | Tous les collaborateurs doivent avoir la capacité d'accéder à toutes les informations concernant les clients, les contrats et les événements en mode lecture seule. |

## Besoins individuels : équipe de gestion

| Fonctionnalité                                 | Description                                                                                                        |
|------------------------------------------------|--------------------------------------------------------------------------------------------------------------------|
| Créer, mettre à jour et supprimer des collaborateurs | Permet de créer, mettre à jour et supprimer des collaborateurs dans le système CRM.                                 |
| Créer et modifier tous les contrats            | Autorise la création et la modification de tous les contrats dans le système.                                       |
| Filtrer l’affichage des événements             | Permet de filtrer l'affichage des événements, par exemple, afficher tous les événements sans « support » associé.   |
| Modifier des événements                        | Autorise la modification d'événements, y compris l'association d'un collaborateur support à l'événement.           |

## Besoins individuels : équipe commerciale

| Fonctionnalité                                     | Description                                                                                                                                                         |
|----------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Créer des clients                                  | Permet aux utilisateurs de créer des clients, qui seront automatiquement associés à eux.                                                                              |
| Mettre à jour les clients responsables             | Autorise les utilisateurs à mettre à jour les informations des clients dont ils sont responsables.                                                                   |
| Modifier/mettre à jour les contrats des clients    | Permet de modifier ou de mettre à jour les contrats des clients dont les utilisateurs sont responsables.                                                             |
| Filtrer l’affichage des contrats                   | Autorise le filtrage des contrats selon certains critères, comme ceux qui ne sont pas encore signés ou pas encore entièrement payés.                                 |
| Créer un événement pour un client avec contrat     | Permet de créer un événement pour un client qui a signé un contrat, offrant une gestion événementielle intégrée pour les clients sous contrat.                       |

## Besoins individuels : équipe support

| Fonctionnalité                              | Description                                                                                      |
|---------------------------------------------|--------------------------------------------------------------------------------------------------|
| Filtrer l'affichage des événements          | Permet de filtrer l'affichage des événements pour n'afficher que ceux attribués à l'utilisateur. |
| Mettre à jour les événements responsables   | Autorise les utilisateurs à mettre à jour les événements dont ils sont responsables.             |




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
- **Administration**: Gestion des employés

---

# Guide d'implémentation

## Architecture générale

- Modèle MVC (Modèle-Vue-Contrôleur) pour séparer les responsabilités
- Base de données POSTGRES SQL pour un prototype rapide (en gardant à l'esprit les contraintes de sécurité)

### Authentification

- Utilisation de jetons JWT pour authentifier les collaborateurs

### Département Commercial / SALES

- Interface en ligne de commande pour ajouter/mettre à jour les clients et contrats
- Filtres de recherche pour les contrats non signés, etc.

### Département Support / SUPPORT

- Interface pour filtrer et mettre à jour les événements qui leur sont attribués
- Notifications pour les changements d'état des événements

### Département Gestion / ACCOUNTING

- Interface admin pour la gestion des collaborateurs, contrats et événements
- Filtres pour afficher les événements sans support, etc.

### Département Administration / ADMIN

- Utilisé comme un rôle pour filtrer une permission spéciale d'accès au menu d'administration pour la gestion des employés.

### Sécurité

- Utilisation de requêtes paramétrées pour prévenir les injections SQL
- Implémentation du principe du moindre privilège via des rôles et permissions

### Journalisation

- Intégration de Sentry pour capturer les erreurs et exceptions

# Diagram ERD
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
# La base de donnée

## 1. Installation de PostgreSQL et PgAdmin:

Les étapes d'installation impliquent la disponiiblité d'un server linux Fedora/RedHat/CentOS.

### Installation du server PSQL
- PostgreSQL:

``` Shell
sudo dnf update sudo dnf install postgresql-server postgresql-contrib
```

### Après l'installation, initialiser la base de données:

``` Shell
sudo postgresql-setup --initdb
```

### Puis démarrer et activer le service:

```shell
sudo systemctl start postgresql sudo systemctl enable postgresql
```

### PgAdmin:

```Shell
sudo dnf install pgadmin4
```

## 2. Créer une nouvelle base de données:

### SHELL : Se connecter à la base de données par défaut (postgres) avec l'utilisateur par défaut (postgres) :

``` Shell
 psql -U postgres -h localhost -d epic_events

```

### Créer une nouvelle base de données avec le nom : `epic_events`.

## 3. Créer un utilisateur pour l'application:

- Créer un nouvel utilisateur (ou "Role" dans le jargon PostgreSQL).
- Attribuer un nom et un mot de passe et assurer les droits suffisants sur la base de données epic_events.


## 4. Configurer les variables d'environnement:

- Les informations de connexion à la base de données dans des variables d'environnement pour des raisons de sécurité. Nous utilisons la librairie  `dot_env`

## 5. Créer un environnement virtuel Python:

### Dans le répertoire du projet, crée un environnement virtuel:


    ``` Python
    python3 -m venv .venv
    ```

### Activer l'environnement:

   ``` Shell
   source .venv/bin/activate
   ```

### Installer les dépendances comme `SQLAlchemy` et `Dot_env`:

#### Créer un fichier pour les variables d'environnement

1. **Crée un fichier `.env` dans le répertoire de ton projet**. Ce fichier contiendra tes variables d'environnement.


``` Shell
touch .env
```


### Ouvrir ce fichier avec un éditeur de texte** et ajouter les variables.

- Par exemple :

``` Shell
DATABASE_URL=postgresql://username:password@localhost/dbname SECRET_KEY=mysecretkey

DATABASE_URL=postgresql://user:Password@localhost/epic_events
EPICEVENTS_USER=user
EPICEVENTS_PW=Password
EPICEVENTS_SK=mySecretKey
```

Ici, `username` et `password` sont ceux définis lors de la création de l'utilisateur PostgreSQL, et `dbname` est le nom de la base de données créée précédememnt.


### Charger les variables d'environnement dans l'application

1. **Installer la librairie `python-dotenv`**: Cette librairie permet de charger les variables d'environnement depuis un fichier `.env` dans le projet.
```Shell
pip install python-dotenv
```

2. **Charger les variables dans le code Python**:

``` Python
from dotenv import load_dotenv import os  load_dotenv()  database_url = os.getenv("DATABASE_URL") secret_key = os.getenv("SECRET_KEY")
```

Ici, `load_dotenv()` lit le fichier `.env` et charge les variables pour les utiliser avec `os.getenv().

# Démonstration

Dans le cadre de ce projet, certains composants sont volontairement exclus de synchronisation avec GitHub comme le fichier .env pour illustrer une bonne pratique consistant à ne pas partager les informations sensibles sur un dépôt public.

# FRONTEND

Conformément au cahier de charges, la partie cliente est entièrement réalisée en ligne de commande en utilisant la librairie RICH.

# BACKEND

Le backend est réalisé en Python 3.12 et utilise les librairies suivantes:

- SQLAlchemy
- Dotenv
- Rich
