# Serveur Gestion Energie

## Description
Le serveur permet de gérer les informations liées à la consommation d'énergie électrique. Il est le nœud entre le consommateur et les outils de mesure et de maitrise de l'énergie électrique d'un foyer. 

## Fonctions
* Afficher les informations générées par le compteur communicant
* Interpréter les informations du compteur communicant pour être utile au consommateur et ainsi mieux gérer sa consommation 
* Avoir une vision détaillée de la consommation du foyer
* Controller les objets connectés pour maitriser la consommation
* Programmer le déclenchement des prises en fonction de plages horaires
* Paramétrer les priorités des objets alimentés pour un délestage intelligent 
* Stocker les données pour de faire du traitement de données

## Composants
* Raspberry Pi 3 
* nRF24

## Echanges d'informations
Le serveur tel qu'il est conçu possède deux type de connexion : Radio Fréquence et wifi.
La connexion radio fréquence sert à récupérer les informations générés par le compteur communicant (Linky) grâce à l'ajout d'un "décodeur" et d'un transmetteur RF (TIC).
La wifi permet de créer un réseau local afin que les objets connectés échange avec le serveur. 

### Informations récupérées
* Trame du compteur via la TIC en RF.
* Informations d'état des différents objets connectés via une API REST.
* Informations de mesure du courant des objets connectés

### Informations envoyées
* Information de pilotage des objets connectés. 

## To do
* Implémenter la collecte d'information via RF (librairie nRF24)
* Systématiser la collecte d'information des objets connectés (fonctionne partiellement pour l'[écran déporté](https://github.com/LF2L/RemoteLinkyInfo))
* Créer la fonction de délestage
