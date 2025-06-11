import sys
from PyQt6.QtWidgets import QApplication
from Modele import ModeleMagasin
from Vue import VuePlan

class Controleur:

    def __init__(self):
        self.app = QApplication(sys.argv)
        self.modele = ModeleMagasin()
        self.vue = VuePlan("plan.jpg", cell_size=8)
        self.modele.charger_csv("liste_produits.csv")
        
        self.connecter_signaux()
        self.correspondance_secteurs_rayons = {
            "Charcuterie": "Viandes",
            "Fruits": "Fruits",
            "Légumes": "Légumes",
            "Poissonnerie": "Poissons",
            "Produits frais": "Rayon frais",
            "Produits sucrés": "Épicerie sucrée",
            "Petit déj": "Petit déjeuner",
            "Crémerie": "Crèmerie",
            "Épicerie": "Épicerie",
            "Conserves": "Conserves",
            "Apéro": "Apéritifs",
            "Boissons": "Boissons",
            "Maison": "Articles Maison",
            "Hygiène": "Hygiène",
            "Bureau": "Bureau",
            "Animaux": "Animaux"
        }

    def connecter_signaux(self):
        self.vue.celluleCliquee.connect(self.traiter_clic)

    def lancer_application(self):
        self.vue.show()
        sys.exit(self.app.exec())

    def traiter_clic(self, row, col):
        for secteur, infos in self.vue.sectors.items():
            if (row, col) in infos["cells"]:
                rayon = self.correspondance_secteurs_rayons.get(secteur)
                if rayon:
                    produits = self.modele.get_produits(rayon)
                    self.vue.afficher_produits_secteur(secteur, produits, col * self.vue.cell_size, row * self.vue.cell_size)
                else:
                    self.vue.afficher_produits_secteur(secteur, [])
                break
        else:
            self.vue.vider_produits_secteur()



if __name__ == "__main__":
    controleur = Controleur()
    controleur.lancer_application()