import csv
import unicodedata

def normaliser_texte(texte: str) -> str:
    texte = texte.strip().lower()
    texte = unicodedata.normalize('NFKD', texte)
    return ''.join(c for c in texte if not unicodedata.combining(c))

class ModeleMagasin:
    def __init__(self):
        self.rayons = []
        self.produit_vers_rayon = {}
        self.produits_positionnes = {}

    def charger_csv(self, chemin_csv: str, separateur=';'):
        with open(chemin_csv, encoding='utf-8') as fichier:
            lecteur = csv.reader(fichier, delimiter=separateur)
            lignes = list(lecteur)
            if not lignes:
                return
            self.rayons = [r.strip() for r in lignes[0]]
            for col_index, rayon in enumerate(self.rayons):
                rayon_norm = normaliser_texte(rayon)
                for ligne in lignes[1:]:
                    if col_index < len(ligne):
                        produit = ligne[col_index].strip()
                        if produit:
                            produit_norm = normaliser_texte(produit)
                            self.produit_vers_rayon[produit_norm] = rayon

    def get_rayon(self, produit: str) -> str | None:
        produit_norm = normaliser_texte(produit)
        return self.produit_vers_rayon.get(produit_norm)

    def get_produits(self, rayon: str) -> list[str]:
        rayon_norm = normaliser_texte(rayon)
        return [prod for prod, r in self.produit_vers_rayon.items() if normaliser_texte(r) == rayon_norm]

    def produits_dans_liste(self, liste_produits: list[str]) -> dict[str, list[str]]:
        resultat = {}
        for produit in liste_produits:
            rayon = self.get_rayon(produit)
            if rayon:
                resultat.setdefault(rayon, []).append(produit)
        return resultat
    
    def ajouter_produit_emplacement(self, produit: str, row: int, col: int):
        self.produits_positionnes[produit] = (self.get_rayon(produit), row, col)


    def sauvegarder_csv(self, chemin: str):
        with open(chemin, "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(["Produit", "Rayon", "Ligne", "Colonne"])
            for produit, (rayon, row, col) in self.produits_positionnes.items():
                writer.writerow([produit, rayon, row, col])
