---
_edit_last: "1"
_thumbnail_id: "2084"
_xmlsf_image_featured:
  caption: ""
  loc: https://javaetmoi.com/wp-content/uploads/2020/02/azure-fundamentals-600x600-1.png
  title: azure-fundamentals-600x600
author: admin
categories:
  - retour-d'expérience
featureImage: wp-content/uploads/2020/02/azure-fundamentals-600x600-1.png
featureImageAlt: azure-fundamentals-600x600
date: "2020-02-08T18:35:40+00:00"
thumbnail: wp-content/uploads/2020/02/azure-fundamentals-600x600-1.png
guid: https://javaetmoi.com/?p=2080
parent_post_id: null
post_id: "2080"
post_views_count: "9658"
summary: |-
  [![](https://javaetmoi.com/wp-content/uploads/2020/02/azure-fundamentals-600x600-1-150x150.png)](https://www.youracclaim.com/earner/earned/badge/e18659c6-5f65-4efa-becd-c4293079ea4b) Assurée par un formateur Microsoft, la formation «  Microsoft Azure Fondamentals » se déroule sur une journée et permet de se préparer à la **[certification AZ-900 « Microsoft Azure Fondamentals »](https://docs.microsoft.com/fr-fr/learn/certifications/exams/az-900)**. A l’issue de la formation, un voucher est donné à chaque participant. Ces derniers sont invités à passer leur certification dans la foulée.

  La formation est découpée en 4 modules.
  Les notes ci-dessous m’auront permis d’obtenir [ma certification](https://www.youracclaim.com/earner/earned/badge/e18659c6-5f65-4efa-becd-c4293079ea4b) du premier coup. J’espère qu’elles vous aideront à vous préparer. En rouge, sont notés les mots clés, concepts et noms de produits à retenir par cœur.

  ![azure-fundamentals-600x600](wp-content/uploads/2020/02/azure-fundamentals-600x600-1.png)
tags:
  - azure
  - cloud
title: Certification Microsoft Azure Fondamentals
url: /2020/02/certification-microsoft-azure-fondamentals/

---
[![](wp-content/uploads/2020/02/azure-fundamentals-600x600-1.png)](https://www.youracclaim.com/earner/earned/badge/e18659c6-5f65-4efa-becd-c4293079ea4b) Assurée par un formateur Microsoft, la formation «  Microsoft Azure Fondamentals » se déroule sur une journée et permet de se préparer à la **[certification AZ-900 « Microsoft Azure Fondamentals »](https://docs.microsoft.com/fr-fr/learn/certifications/exams/az-900)**. A l’issue de la formation, un voucher est donné à chaque participant. Ces derniers sont invités à passer leur certification dans la foulée.

La formation est découpée en 4 modules.
Les notes ci-dessous m’auront permis d’obtenir [ma certification](https://www.youracclaim.com/earner/earned/badge/e18659c6-5f65-4efa-becd-c4293079ea4b) du premier coup. J’espère qu’elles vous aideront à vous préparer. En rouge, sont notés les mots clés, concepts et noms de produits à retenir par cœur.

# Certification AZ-900

Certification AZ-900 : passage obligatoire pour toutes les autres certifications Azure (ex : AZ-203 : Developing Solutions for Microsoft Azure)
Durée : 1h
Score nécessaire : >= 700 / 1000
Entre 40 et 44 questions
Les 5 à 7 premières questions : on ne peut pas revenir sur ses réponses
L’examen est en anglais, chinois ou japonais.
Pour vous y préparer, vous pouvez suivre le [parcours d’apprentissage « Principes de base d’Azur ».](https://docs.microsoft.com/fr-fr/learn/paths/azure-fundamentals/)

## Module 1 – Cloud Concepts

Pourquoi : agilité, scalability / élasticité, sécurité, haute disponibilité / high availability (SLA), fault tolerance, on demand self-service, accessiblité / global reach (accessible de n’importe où), disaster recovery, customer latency capabilities, maitrise des coûts / predictive cost considerations

**Passage du modèle CapEx vers OpEx**

- CapEx : Capidatal Expanditure: modèle basé sur le capital / les serveurs, un ensemble de serveurs et d’Ops => On-premise
- OpEx : Operational Expanditure modèle du cloud computing. Le client n’achète plus les machines, mais les services

**Consumption-based model**
On ne paie que ce qu’on utilise : pay-as-you-go : on paie la consommation des services. Lorsqu’on arrête la VM, on paie quand même le stockage.
Lors de la scalabilité, on ne paie plus les ressources qu’on n’utilise plus.
Dans tous les modèles, la responsabilité est partagée par les 2 : Microsoft et le client
Accès au portail Azure : [portal.azure.com](https://portal.azure.com/" \l "home) **Comparaison des modèles Cloud**

- Public Cloud :
  - Propriété du fournisseur
  - Accessible depuis Internet
- Cloud Privé de Microsoft : Azure Stack
  - Fourni par le Cloud Provider
  - La sécurité physique des ressources est gérée par le client
  - Non accessible sur Internet
  - Cas d’usage : besoin accrue en termes de sécurité (ex : ministère de la Défense)
- Cloud Hybrid :
  - Combinaisons des clouds publics et privés
  - Ex : site web sur Cloud public et base de données sur Cloud privé
  - Les clients gèrent la sécurité

D’après l’expérience de la formatrice, 90% des clients combinent On-Promise et Cloud avec plusieurs fournisseurs.

**Types of services**

Responsabilités :

- IaaS (VM) : Microsoft gère le stockage, le réseau et le matériel. Le client gère l’OS, les applications
- PaaS (Azure Function ou Azure Webapp) : Microsoft gère la maj de l’OS, le client gère les données, les accès (AD en local ou Azure) et l’application
- SaaS (Office 365) : applications hébergées dans Azure que le client a besoin de configurer : l’admin doit configurer les accès à Outlook et Teams

## Module 2 – Core Azure Services

 **Regions**

Une région = une collection de Data Center
54 régions représentant 140 pays

Un Data Center et une Région existe en France (pas le cas en Belgique et en Allemagne)

Recommandation : utiliser les régions les plus proches de l’utilisateur à cause de la latence réseau et du **coût** **Region Pairs**

Chaque région est associée à une autre région pour assurer la bascule en cas de panne (sauf le Brésil).

**Géographies**

5 zones géographiques

**Availability Options**

- SLA 99,9% : Single VM avec stockage Prenium (géré par Microsoft)
- SAL de 99,95% : créer des availability sets
- VML SLA : 99,99% : créer des availability zones

Availabity Sets : lorsqu’on crée une VM, une bonne pratique consiste à le créer dans un Availability Sets dans le même datacenter pour avoir :

- Update Domains (UD) : mise à jour logiciel
- Fault domains (FD) : pb d’alimentation, gère les problèmes physiques

Availability zones : permet de remédier un pb arrivant sur un Data Center. On reste dans la même région

**Resource groups**

- Permet d’organiser les projets. N’a pas de lien avec la scalabilité
- Conteneurs de ressources (ex : web app, VM, stockage)
- Nécessaire lors de la création d’une ressource
- Une ressource n’existe que dans un groupe de ressource. On peut la déplacer d’un groupe de ressources à un autre
- Les ressources d’un groupe **peuvent être créées sur des régions différentes**. Utile lorsqu’un service n’existe pas sur la région privilégiée
- Permet de définir des droits sur un groupe de ressources : **Role Based Access Control** (RBAC). On définit les droits à l’aide de rôles. Une personne a les mêmes droits sur toutes les ressources du groupe

**Azure Resource Manager**

- Permet de déployer simultanément plusieurs ressources identiques en utilisant un template ARM (au format JSON) : pour déployer 50 VM, on déploie le template 50x.
- Terraform permet de déployer les templates en multi-Cloud
- Permet d’automatiser la création des ressources
- Souscriptions : pour travailler sur Azure, il faut avoir un compte Azure. Ce compte est soit rattaché à un compte pro, soit à une adresse perso. Sous le compte Azure, on retrouve 1 ou plusieurs souscriptions. La souscription gère la partie contractuelle. Certains clients ont une souscription par département (ex : finance, IT). Permet de gérer la partie facturation. Chaque souscription a sa propre facturation. L’administrateur gère les souscriptions.
- Management groups : services Azure donnant les droits différents sur des souscriptions différentes

**Azure Compute**

- Virtual machines
- Virtual machines scale sets : scalabilité des VM, permet d’augmenter le nombre d’instances de VM. On définit les conditions d’augmentation du nombre d’instances en fonction du taux d’utilisation du CPU et/ou de la RAM. On peut le configurer dans le template ARM
- Function App : server less, bout de code exécuté sans serveur derrière, un bout de code par fonctionnalité (ex : inscription, réservation, paiement, envoi de mail de confirmation). Le déclenchement d’une fonction est déclenchée en fonction d’un événement (trigger). Exemple : ajout d’une ligne en base de données. Architecture servless basée sur les évènements. Gain de coût : un client se trouvant sur la page d’inscription ne va pas solliciter la fonctionnalité de réservation.
- App Services : PaaS permet d’héberger une webapp dans Azure
- Kubernetes Services
- Availabity Sets : disponibilité, Update Domaine, Fault Domain
- Disks

**Container services**

2 services PaaS :

- Azure Container Instances
- Azure Kubernetes Services (AKS)

**Azure Network Services**

- Azure Virtual Network (VNet) : obligatoire, permet de communiquer entre VM, que ce soit en local ou dans Azure. Lorsqu’on crée une VM, on doit le placer dans un VNet. Dans un VNet, on retrouve des sous-réseaux (Subnet). Par défaut, un VNet est créé avec un Subnet. La sécurisation est assurée par NSG
- Azure Load Balancer : permet de répartir la charge et d’avoir de la HA
- VPN Gateway : permet de communiquer avec le OnPrem
- Azure Application Gateway : permet de gérer le trafic dans une application web
- Content Delivery Network : redirige les utilisateurs sur le point de stockage le plus proche afin de leur desservir des ressources statiques (images, vidéo). Système de cache

**Azure data categories**

- Structured data : schema, SGBD
- Semi-structured data : NoSQL, données clé/valeur
- Unstructured data : photos, videos

**Azure storage services**

- IaaS : pour les VM on a 2 possibilités : Premium Storage (Microsoft gère) ou autre si migration de VM (.vhd)

  - Disks : disque persistant pour les VM IaaS. Options : SSD ou pas, Lift and shift operations
  - Files : fichiers partagés avec SMB et REST. Azure File Share. Par défaut, 3 copies du fichier dans le même datacenter
- PaaS
  - Containers : données non structurées placées dans des blobs d’un espace de stockage. Plusieurs types de stockage. La taille d’un compte de stockage est limitée (5 TB). Le nombre de compte de stockage est limitée par la souscription. On peut demander au Support Azure d’augmenter le nombre de stockage permis pour une souscription.
    - Block blobs : petite taille de stockage (ex : image, pdf)
    - Page blobs : toutes les autres tailles
    - Append blobs : va être supprimé de la roadmap Azure
  - Tables : pour les données NoSQL, va être supprimé dans la roadmap Azure et remplacé par Azure Cosmos DB
  - Queues : gestion asynchrone des messages

Le cout d’un Storage est calculé en fonction de la capacité de stockage, le niveau de réplication (4 niveaux), le niveau d’accès (hot, cold, archive)

**Azure database services**

- Azure Cosmos DB : base de données globalement distribuée. Le temps de latence est géré par Cosmos.
- Azure SQL Database : la latence est gérée manuellement par duplication/synchronisation des données. Base compatible avec Microsoft SQL Server 2012
- Azure Database migration : permet de migrer le schéma et les données (ex : SQL Server ou Oracle) vers Azure SQL Database

**Azure Marketplace**

- Applications développées par les partenaires Microsoft ou d’autres sociétés
- Les applis sur le marketplace sont validées par Microsoft. Les

**Internet of Things**

- Azure IoT Cental : solution SaaS pour faire des démos autour de l’IoT : récupération, monitoring, restitution.
- Azure IoT Hub : permet d’ingérer les données. Utiliser une communication bidirectionnelle entre l’application IoT et les devices.

**Big data and analytics**

- Azure SQL Data Warehouse : service PaaS permet de faire des **traitements en //** sur une grosse volumétrie de données (To et **Péta-octets**). Basé sur SQL Server. SLA de 99,99%. Déployé sur des serveur HP7 ?
- Azure HDinsight : service PaaS big-data d’Azure utilisant des frameworks Open Source comme Hadoop et Spark. Facturé au niveau du compute et du stockage.
- Azure Data Lake Analytics : service PaaS développé par Microsoft pour le big data. Langage propre à Microsoft.

**Artificial Intelligence**

- Azure Machine Learning service : environnement PaaS pour faire de l’IA : développer des algorithmes, entrainer, tester, déployer, manager
- Azure Machine Learning studio : environnement collaboratif permettant de faire du drag and drop de fonctionnalités déjà développées
- Data Bricks : service permettant de préparer des données en vue du machine learning

**Serverless computing**

- Azure functions : code s’exécutant sur des infras basées sur des évènements. Gère lui mêmes les évènements.
- Azure Logic Apps : service permettant d’automatiser et d’orchestrer des tâches, des process BPM, les workflows. Exemple : la fonctionnalité d’envoi de mail est courante. Bout de code utilisée en boite noire.
- Azure Event Grid : fonctionne de pair avec Azure Logic Apps pour router les évènements entre logic apps.

**DevOps**

- Azure DevOps services : solution Microsoft pour collaborer sur le template JSON de déploiement. Anciennement TFS. Outils incluant repository Git, boards Kanban et cloud-based load testing.
- Azure DevTest Labs : permet de provisionner rapidement des environnements, généralement pour les développeurs

**Azure App Service**

- Service permettant d’héberger une application web
- Supporte plusieurs langages et frameworks : PHP, .NET, Ruby, Python ou bien encore Java
- DevOps optimization
- Global scale with high availability
- Connection aux plateformes SaaS et On Prem
- Applications templates : Wordpress,
- API and Mobile features
- Serverless code

**Azure Management tools**

- Azure portal
- Azure PowerShell : shell Windows permettant de créer des ressources
- Azure Command-Line Interface (CLI): language different d’Azure Command-Line. Créé en 2015 car PowerShell n’était pas compatible avec MacOS. En 2020, les 2 outils fonctionnent avec tous les OS : Windows, MacOS … Attention, les syntaxes des 2 langages sont différents.
- Azure Cloud Shell : installé directement dans le portal. On a le choix du langage : PowerShell ou Bash. Sur iPhone, on peut utiliser le portal Azure ou Cloud Shell
- Azure mobile app : application iPhone ou Android
- Azure REST API : pour les développeurs

**Azure advisor**

- Donne des recommandations sur le HA, la sécurité, les performances et le coût.
- Identifie les opportunités de diminuer les coûts en arrêtant / supprimant des VM non utilisées

## Module 3 – Security, privacy

 **Shared security**

Sécurité partagée par Microsoft et le client

**Azure Firewall**

- Permet de filtrer le trafic entrant et sortant au niveau du VNet

**Network Security Group (NSGs)**

- Permet de sécuriser les VM
- Composant permettant de déclarer des règles de sécurité.
- On définit des règles au niveau NSG. Le NSG peut être rattaché au Subnet. Toutes les VM du Subnet sont protégées. Recommandation : un NSG par Subnet.

**Azure Distributed Denial of Service (DDoS) protection**

- Service activé par défaut dans Azure en mode basic
- Optionnel, le mode « Standard service » permet d’avoir un rapport d’audit

**Authentication and authorization**

- Authentification : on vérifie que la personne fait partie de l’annuaire
- Authorization : on vérifie les droits

**Azure Active Directory (AD)**

- Fonctionnalité de base d’authentification
- Single sign-on (SSO)
- Application management : derrière Office 365, il y’a un Azure AD. L’administrateur nous a donné les droits d’utiliser Teams.
- B2B : on peut faire communiquer 2 AD : Generali et partenaire
- B2C : permet à l’utilisateur d’une application mobile de s’enregistrer dans un AD spécifique à l’appli
- Device management : permet d’utiliser un AD en BYOD
- L’outil AD Connect permet de synchroniser l’AD Azure et l’AD local

**Azure Multi-Factor Authentication (MFA)**

- Permet de renforcer l’authentification login / password
- Azure : envoi de code, appel téléphonique ou application
- Possible sur le LDAP gratuit

**Azure Security Center**

- Portail permettant d’avoir des recommandations sur la sécurité des ressources (ex : configuration du NSG)

**Azure Key Vault**

- Permet de stocker les certificats, les clés de chiffrage, les mots de passe

**Azure Advances Threat Protection (Azure ATP)**

- Portail détectant les failles de sécu d’un site web hébergé sur Azure
- Utiliser des sensors
- Envoi de reporting hebdo par mail

**Azure policy**

- Application de la stratégie d’une entreprise
- L’administrateur met en place des policies pour restreindre des possibilités :
  - Ex1 : stratégie de mettre les données que sur des Data Center français
  - Ex2 : les développeurs ne travaillent qu’avec les services PaaS
  - Ex3 : limiter les droits de l’utilisateur

**Implementing Azure Policy**

- Create a policy definition -> assign the definition to resources -> review the evaluation effects
- Permet de détecter les ressources qui ne sont pas alignées avec la stratégie

**Resource Locks**

- 2 types de Locks :
  - CanNotDelete : Read, Update (pas de suppression)
  - ReadOnly : Read

Un verrou peut être appliquer sur une souscription, un resource group ou une ressource. Le CanNotDelete est systématiquement mis en place sur souscription. Permet de protéger les resources Azure d’une suppression accidentelle.

Possibilité dans Azure de déléguer ou transférer le rôle Admin

**Azure Blueprints**

- Permet de créer un template d’Azure policies en vue de réutilisation sur d’autres environnement

**Subscription Governance**

La souscription facilite les tâches administratives :

- Billing : une facturation générée par souscription
- Access Control : role-based access control
- On peut déplacer les ressources d’une souscription à une autre

**Tags**

- Méta-données positionnées sur les ressources et les groupes de ressources
- Permet de s’y retrouver et de gérer la **facturation**
- Consiste en une paire clé/valeur
- Exemples : owner:joe, environment:production, department:marketing

**Azure Monitor**

- Service gratuit permettant de collecter et d’analyser l’actualité de toutes les ressources (VM ou autre)
- Chaque ressource créée possède un Azure Monitor
- Activity Logs : composant Azure Monitor permettant d’avoir des logs sur les actions réalisées sur la machine : création, mise à jour, changement de configuration …
- Conserve les métriques de la machine : performance, consommation …

**Log Analytics**

Utilisé en environnement multi-cloud : Azure, AWS et OnPrem.
Cet outil s’appuie sur les données remontées par Azure Monitor.
Dans les autres cloud, il faut ajouter des agents Log Analytics

**Azure Service Health**

- Service permettant d’avoir l’état de santé des services Azure. Problème venant de Microsoft et non des ressources du client.
- Plusieurs composants :
  - Azure Status : global overview Azure
  - Service Health : dashboard personnalisé
  - Azure Resource health : permet de diagnostiquer des problèmes Azure

**Monitoring applications and services**

- Azure Application Insights : similaire à Google Analytics, destiné aux applications web
- Azure Alerts : bonne pratique à mettre en place systématiquement. Exemple : en cas de pb sur une VM, on peut envoyer un mail, arrêt une VM … : pour les actions, on peut passer par Logic Apps, Azure Functions ou PowerShell
- Visualisation : on peut utiliser Power BI (outil de DataViz)

**Trust Center**

- Page indépendante d’Azure permet de connaître la gestion de la confidentialité

**Compliance Termes and Requirements**

- GDPR : européren
- ISO : international

**Microsoft privacy statement**

Document signé entre le client et Microsoft

**Compliance Manager**

- Outil permettant de donner un score pour évaluer la compliance
- S’appuie sur les Azure policies pour calculer les scores

**Azure Government services**

- Partie dans Azure dédiée aux personnes et entreprises américaines

**Azure China 21Vianet**

- Les contrats passent entre 21Vianet et le client. Instance d’Azure cloud localisée en Chine

**Azure Information Protection**

- Permet de chiffrer les emails

## Module 4 – Azure pricing and support

**Azure subscriptions**

- Exemple d’une Azure subscription par environnement : dev, test, production
- Facilite la facturation et les autres tâches administratives

**Subscription offers**

- Plusieurs offres : Free, Pay-as-you-go, Entreprise Agreement, Student
- Offre free :
  - Les souscriptions gratuites n’ont pas de SLA
  - Limitée : 170 euros par mois pendant 12 mois, tous les services ne sont pas dispos
  - Lorsque on dépense ce quota, la VM est bloquée
- Offre EA
  - Generali est un client tiers 1
  - Les clients tiers 2 passent par des partenaires (ex: Cap Gemini)

**Managment groups**

- Gérer les droits des personnes à des souscriptions différentes

**Purchasing Azure products and services**

- Partenaire ou Microsoft directement
- Les adresses IP publiques sont payantes

**Factors affecting costs**

- Resource Type : le storage est le service le moins cher
- Services : les partenaires fixent eux-mêmes leurs tarifs
- Location

**Zones for Billing Purposes**

- 90% du trafic entrant sont gratuits (ex : VM local -> VM dans Azure)
- Les trafics sortants sont tous payants et dépendent des zones
  - Zone 1 : West US, East US, West Europe and others => zone la moins chère
  - Zone 2 :
  - Zone 3 :
  - DE Zone 1 : Germany => le plus cher

**Princing calculator**

- Calculette permettant d’estimer le coût d’un projet
- Le coût de la VM est impacté par plusieurs éléments (ex : OS, localisation …)

**Total cost of ownership calculator**

- Outil permettant d’estimer la migration vers Azure de gros workloads

**Minimizing costs**

Recommandations :

- Utiliser Azure Advisor qui nous dit comment diminuer les couts
- Utiliser des spending limits : ex 200$ pour le Free, fixe
- Utiliser Azure reservation : permet de réserver une VM pendant 1 an ou 3 ans, ce qui permet de bénéficier d’une réduction de 35%. Offre réservée aux clients tiers 1
- Choisir les low-cost locations and regions
- Utiliser des tags pour identifier les ressources low-cost

**Azure Cost Managment**

- Outil intégré dans Azure permettant de suivre les couts
- Disponible pour les clients en tiers 1

**Support plan options**

- Support basic
- Support developer : trial and non-production **environnements** : possible via email depuis le portail azure aux heures de bureau. Réponse en 8h
- Support standard : pour les environnements de production, contact par email et téléphone 24/7. Réponse en 2h.
- Professional Direct : applications directes. Support 24/7, Réponse en 15mn via mail ou téléphone
- Support Premier : comme le Professional Direct avec un CSA (architecte)

**Alternative support channels**

- MSDN Azure forums
- Stack Overflow
- …
- Knowledge center : base de connaissance

**Service Level Agreement**

- 99,99%
- Remboursement sur compte bancaire en cas de SLA non atteint

**Composite SLAs**

- On multiplie tous les SLA
- SLA du projet : .9995 (webapp) **x** .9999 (database) = 99,94%

**Public and private preview features**

- Private preview : resource disponible pour une partie des clients et/ou une communauté (ex : MVP), testeurs Microsoft …
- Public preview : disponible pour tout le monde, non recommandé en prod, pas de SLA. Version beta
- General Availability : version finale

Azure updates permet de savoir quand une ressource passe en GA
