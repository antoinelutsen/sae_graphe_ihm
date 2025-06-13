import csv, random, unicodedata, json
from heapq import heappop, heappush

def normaliser_texte(texte: str) -> str:  # Supprime les accents, met en minuscules et enlève les espaces superflus pour homogénéiser les chaînes
    texte = texte.strip().lower()
    texte = unicodedata.normalize('NFKD', texte)
    return ''.join(c for c in texte if not unicodedata.combining(c))

def dijkstra(start, objectifs, accessibles):
    objectifs = set(objectifs)
    file = [(0, start, [])]
    visites = set()

    while file:
        cout, position, chemin = heappop(file)
        if position in visites:
            continue
        visites.add(position)
        chemin = chemin + [position]

        if position in objectifs:
            return chemin

        x, y = position
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            voisin = (x + dx, y + dy)
            if voisin in accessibles and voisin not in visites:
                heappush(file, (cout + 1, voisin, chemin))

    return []

class ModeleMagasin:
    def __init__(self):
        # Initialise les structures de données :
        # - rayons : liste des noms de rayons
        # - produit_vers_rayon : dictionnaire produit -> rayon
        # - produits_positionnes : dictionnaire produit -> (rayon, ligne, colonne)
        self.rayons = []
        self.produit_vers_rayon = {}
        self.produits_positionnes = {}
        self.descriptif = {}
        self.toutes_les_cases = None
        max_col = 1200 // 8  # nombre de colonnes
        max_row = 1000 // 8  # nombre de lignes
        self.initialiser_toutes_les_cases(max_row, max_col)
    
    def initialiser_toutes_les_cases(self, max_row, max_col):
        self.toutes_les_cases = set((r, c) for r in range(max_row) for c in range(max_col))
    
    def set_grille_magasin(self, secteurs, inaccessibles): # Définit la grille du magasin à partir des secteurs (zones valides) et des cases inaccessibles
        self.secteurs = secteurs  # dict[str, set[tuple[int, int]]]
        self.inaccessible_cells = inaccessibles
        self.positions_utilisées = set()

    def charger_descriptif(self, chemin: str):
        with open(chemin, encoding='utf-8') as f:
            self.descriptif = json.load(f)

    def get_descriptif(self) -> dict:
        return self.descriptif

    def charger_csv(self, chemin_csv: str, separateur=';'):
        with open(chemin_csv, encoding='utf-8') as fichier:
            lecteur = csv.DictReader(fichier, delimiter=separateur)
            for ligne in lecteur:
                produit = ligne["Produit"].strip()
                rayon = ligne["Rayon"].strip()
                if produit and rayon:
                    produit_norm = normaliser_texte(produit)
                    rayon_norm = normaliser_texte(rayon)
                    self.produit_vers_rayon[produit_norm] = rayon_norm

    def get_rayon(self, produit: str) -> str | None: # Retourne le rayon associé à un produit (normalisé) et None s'il n'existe pas
        produit_norm = normaliser_texte(produit)
        return self.produit_vers_rayon.get(produit_norm)
    
    def get_cases_secteur(self, nom_secteur: str) -> list[tuple[int, int]]:
        return list(self.secteurs.get(nom_secteur, set()))

    def get_produits(self, rayon: str) -> list[str]: # Retourne tous les produits d'un rayon
        rayon_norm = normaliser_texte(rayon)
        return [prod for prod, r in self.produit_vers_rayon.items() if normaliser_texte(r) == rayon_norm]
    
    def ajouter_produit_emplacement(self, produit: str, row: int, col: int, rayon: str): # Ajoute / met à jour la position d'un produit avec son rayon
        if rayon is None:
            rayon = self.get_rayon(produit)
        self.produits_positionnes[produit] = (rayon, row, col)


    def sauvegarder_csv(self, chemin: str):
        donnees_existantes = {}

        try:
            with open(chemin, newline='', encoding="utf-8") as f:
                reader = csv.reader(f, delimiter=';')
                next(reader)
                for ligne in reader:
                    if len(ligne) >= 4:
                        produit = ligne[0].strip().lower()
                        rayon = ligne[1].strip()
                        row = int(ligne[2])
                        col = int(ligne[3])
                        donnees_existantes[produit] = (rayon, row, col)
        except FileNotFoundError:
            pass

        for produit, (rayon, row, col) in self.produits_positionnes.items():
            donnees_existantes[produit.lower()] = (rayon, row, col)

        with open(chemin, "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(["Produit", "Rayon", "Ligne", "Colonne"])
            for produit, (rayon, row, col) in donnees_existantes.items():
                writer.writerow([produit, rayon, row, col])

    def attribuer_position(self, rayon): # Choisit une case disponible de manière aléatoire dans un rayon donné, en évitant les cases inaccessibles
        cases_possibles = self.secteurs.get(rayon, set())
        cases_libres = [c for c in cases_possibles if c not in self.inaccessible_cells]
        if not cases_libres:
            return None
        return random.choice(cases_libres)
    
    def construire_chemin_depuis_entree(self, entree: tuple[int, int], produits: list[str]) -> list[tuple[int, int]]:
        accessibles = self.toutes_les_cases - self.inaccessible_cells
        accessibles.add(entree)

        etapes = []
        for nom_produit in produits:
            position = next(((row, col) for p, _, row, col in self.produits_places if normaliser_texte(p) == normaliser_texte(nom_produit)), None)
            if position:
                etapes.append(position)

        sortie_cells = self.secteurs.get("Sortie", set())
        if not sortie_cells:
            return []

        chemin_total = []
        position_actuelle = entree

        for cible in etapes:
            chemin = dijkstra(position_actuelle, [cible], accessibles)
            if not chemin:
                continue
            chemin_total.extend(chemin[1:])
            position_actuelle = cible

        chemin_final = dijkstra(position_actuelle, sortie_cells, accessibles)
        if chemin_final:
            chemin_total.extend(chemin_final[1:])

        return chemin_total
    
    def set_descriptif(self, descriptif):
        self.descriptif = descriptif

    def sauvegarder_descriptif(self, chemin):
        with open(chemin, "w", encoding="utf-8") as f:
            json.dump(self.descriptif, f, ensure_ascii=False, indent=2)
