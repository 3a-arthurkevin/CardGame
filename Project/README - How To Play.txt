Documentation dans laquelle se trouvent les élèments suivant
	- Comment lancer le jeu (GoTo line 7)
	- Les régles du jeu (GoTo line 17)
	- Comment joueur (GoTo line )
	
	
1 - Comment lancer le jeu

	Pour lancer le jeu, veuillez run sur console avec IDLE le fichier main.py se trouver à l'emplacement ci dessous : 
	CardGame/src/main
	
	
	
	
	

2 - Les régles du jeu

	スーパ　ガード　ファイタ (ou "super jeu de carte" dans la langue de molière)est un jeu de carte dans lequel 2 joueurs s'affrontent.
	Leurs but est de mettre les points de vie des son adversaire à 0.
	Chaque joueur commence une partie avec 10 pts de vie.
	La défaite d'un joueur peut aussi être déclanché si il n'a plus de carte dans sa pioche
	
	
	Le joueur possède un deck de 20 cartes. Ce deck peut être construit lors d'un debut de partie lorsque, on doit choisir 1 carte parmis 3 successivement jusqu'à en avoir 20.
	Il est possible de sauvegarder un deck crée, mais aussi de le charge en debut de partie ce qui évite de devoir crée un deck à chaque fois.
	
	
	Il y a 3 types de carte dans ce jeu : 
		- les serviteurs
			Les joueurs les invoques pour pouvoir s'attaquer entre eux
		- les armes
			Armes équipables sur un serviteur, modifient les statisiques du serviteur cible
		- les objets
			Objets améliorant une statistique du serviteur sur lequel l'objet est appliqué
	
	
	Un joueur dispose de 4 points de mana à chaque tour. Ces points lui permet de poser des cartes, selon le cout d'une carte en mana.
			
	Le terrain de jeu sur lequel les joueurs s'affronteront est séparé en 2 zones
	Une pour chaque joueur. Dans ces zones se trouve 3 emplacements pour poser ses serviteurs, et 3 emplacements pour poser ses armes et item.
	A noter qu'un item s'utilise directement et ne reste pas sur le terrain, mais pour pouvoir l'utiliser il faut au moins un emplacement libre pour poser la carte.
	
	
	Dans ce jeu, chaque serviteur a une classe : 
		Epeiste - SwordMaster 				(pouvant équiper des épées)
		Combattant - Warrior				(pouvant équiper des haches)
		Lancier - Halbardier				(pouvant équiper des lances)
		Archer - Archer					 	(pouvant équiper des arcs)
		Chevalier Pegase - Pegasus Knight 	(pouvant équiper des lances)
		Magicien - Mage						(pouvant équiper des tomes élémentaires)
		
	Les serviteurs possèdes des statistiques : 
		- hp			(point de vie du servant)
		- force			(force de frappe pour une attaque physique)
		- intelligence	(force de frappe pour une attaque magique)
		- précision		(Détermine le % de toucher sa cible)
		- vitesse		(Détermine le % d'esquive d'une attaque)
		- defence		(Défense face aux attaques physique)
		- resistance	(Défense face aux attaques magiques)
		- critique		(Détermine le % de chance de faire un coup critique --> dommage*3)
	
	Les serviteurs sont soumis à un systeme d'expérience et de level up selon leurs points d'experience.
	En effet, un serviteur a la possibilité de monté de 1 niveau. Ceci est valable que pour les serviteurs de base.
	Pour cela, il doit atteindre les 100 points d'expériences.
	L'expérience se gagne soit en combattant un serviteur, ou bien en tuant un serviteur.
	Un serviteur niveau supérieur possède un "++" à la fin de son nom
		- Archer (serviteur de base) --> level up --> Archer++ (serviteur évolué)
	Il est possible de poser des serviteurs évolué, mais ils coutent plus cher en mana, et leurs statisiques ne valents pas celle d'un serviteur ayant level up en combattant
		
	Les cartes armes permette d'améliorer la force d'une unité
	
	Le système des armes n'est pas à ignorer dans ce jeu.
		- les épées ont l'avantage face aux haches
		- les haches ont l'avantage face aux lances
		- les lances ont l'avantage face aux épée
		
	Un avantage d'arme ajoute 2 points d'attaque en plus et 2 points de précision lors d'un combat au serviteur
	Un desavantage d'arme enlève 2 points d'attaque en plus et 2 points de précision lors d'un combat au serviteur
	
	La classe de l'unité est aussi à prendre en compte car une classe de servant est plus adapté à se battre contre un autre classe de servant
	
	Dans certains cas (un seul pour le moment), une classe peut etre très sensible face à une arme.
		- Les chevaliers pégases sont très sensibles au flèche. En effet, un arc possède un bonus de 5 points d'attaque face à un chevalier pégase
	
	
	Pour enlever des vies à son adversaire, il y a 2 moyens.
		- Soit tuer un de ses serviteurs. A ce moment la, il perdra en point de vie le niveau de son serviteur mort
		- Soit l'attaque directement (possible quand il n'a aucun serviteurs sur son terrain)




		
3 - Comment joueur

	