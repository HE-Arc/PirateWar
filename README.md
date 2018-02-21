# PirateWar
Little management game with pirates implemented with Django.

## Idée
Chaque joueur (compte utilisateur) possède une flotte de bateau, de l'équipage, de l'équipement et des resources.
Les joueurs peuvent envoyer leurs bateaux réaliser des attaques contre des autres joueurs. Au terme de la bataille, le perdant perd des resources et le gagnant en gagne.

## Description
### Resources
- Argent
- Bois
- Fer
- Equipage
- Canons

### Fonctionnalités
- Construction de bateaux avec du bois
- Recrutement d'équipage avec de l'argent
- Construction de canons avec du fer
- Ajout/suppression d'équipage dans un bateau (augmente vitesse d'attaque) 
- Ajout/suppression de cannon avec du fer (augmente l'attaque)
- Amélioration de bateaux (+ de points de vie, + d'emplacement d'équipage, + d'emplacement canon) 

### Attaques
1. Déplacement vers un adversaire
2. Combat tour par tour (auto), l'attaquant commence
3. Le premier a ne plus avoir de PV perd des ressources
4. Le vainqueur gagne des resources

## Pages
- Page d'accueil
    - Liste des bateaux (activité, pv restants, niveau, equipements)
    - Historique d'activité
- Gestion d'un bateau (réparation, amélioration, gestion canon/equipage)
- Nouvelle activité
    - attaque d'adversaire
    - mission de transport
    - mission de défense