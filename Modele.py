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


if __name__ == "__main__":
    modele = ModeleMagasin()
    modele.charger_csv("liste_produits.csv")

    test_produits = ["porc", "beurre", "abricots", "cervelas", "kiwis", "nonexistent"]

    print("Rayon par produit :")
    for produit in test_produits:
        rayon = modele.get_rayon(produit)
        print(f"  {produit} -> {rayon}")

    print("\nProduits dans le rayon 'Viandes' :")
    print(modele.get_produits("Viandes"))

    print("\nRépartition des produits dans la liste :")
    repartition = modele.produits_dans_liste(test_produits)
    for rayon, produits in repartition.items():
        print(f"  {rayon} : {produits}")
