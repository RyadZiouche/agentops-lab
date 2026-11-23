# ADR 0001 : choix du jeu de données d'essai

- **Statut** : accepté
- **Date** : 2026-11-23

## Contexte

AgentOps Lab est un assistant qui répond à des questions sur des comptes-rendus de réunion. Pour construire puis mesurer le RAG (chunking, top-k, qualité de la recherche), il faut des réunions réelles, des questions, et idéalement des passages de référence. Le projet est public : on ne peut utiliser aucune donnée d'entreprise, et la licence des données doit être claire.

## Décision

On utilise **QMSum, domaine Produit** (réunions du corpus AMI), avec **5 réunions** : `IS1009d`, `ES2004c`, `ES2003a`, `ES2015b`, `IS1003b`.

- **Critères de sélection** : une seule réunion par série (cinq équipes différentes), au moins une réunion de lancement (lettre `a`), et le plus grand nombre de questions utiles.
- **Filtre sur les questions** : on ne garde que celles dont les passages pertinents (`relevant_text_span`) couvrent **40 tours de parole au plus**. Un passage plus long ne peut pas être couvert par un chunk raisonnable, il fausserait la mesure de la recherche.
- **Résultat** : 33 questions utiles (10 + 7 + 6 + 5 + 5).
- **Mise en place** : les fichiers sont téléchargés par `scripts/fetch_qmsum.py` dans `data/raw/qmsum/`, dossier ignoré par git. On versionne le script, pas les données.

## Licences

- **QMSum** (questions, résumés, passages annotés) : licence MIT.
- **Transcriptions AMI** : Creative Commons Attribution 4.0 (CC BY 4.0). Citer la source si des extraits sont montrés (README, démo) : Carletta et al., « The AMI Meeting Corpus: A Pre-announcement », MLMI 2005.
- Les données ne sont pas redistribuées dans le dépôt.

## Alternatives écartées

- **Écrire tous les comptes-rendus soi-même** : contrôle total et réponses connues, mais long, et moins réaliste qu'un corpus existant. On garde l'idée à plus petite échelle : 3 ou 4 comptes-rendus maison serviront de second jeu de test à l'étape 3.
- **Autres domaines de QMSum** (réunions universitaires ICSI, comités parlementaires) : moins proches d'une réunion de projet en entreprise.

## Conséquences

**Avantages**
- Reproductible : un script, des licences claires.
- Des passages de référence annotés : on peut mesurer si la recherche retrouve les bons passages, sans annoter à la main.
- Réunions jouées par des acteurs (équipe fictive de conception d'une télécommande) : pas de données personnelles réelles.

**Limites**
- Petit échantillon : 33 questions, donc des chiffres à interpréter avec prudence.
- Transcriptions en anglais, bruitées : environ 38 % des tours font 3 mots ou moins (« Mm-hmm », « Great »).
- Les réponses de référence sont des résumés, pas des réponses courtes : on évalue surtout la recherche, la qualité des réponses se mesure autrement.
- Un réglage optimisé sur ces réunions peut ne pas se généraliser : d'où le second jeu de test maison.
