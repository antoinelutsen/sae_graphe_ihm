import sys
from PyQt6.QtWidgets import QApplication
from Modele import ModeleMagasin
from Vue import VuePlanCreation

class Controleur:

    def __init__(self):
        self.app = QApplication(sys.argv)
        self.modele = ModeleMagasin()
        self.vue = VuePlanCreation("plan.jpg", cell_size=8)
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
        self.vue.bouton_sauvegarder.clicked.connect(self.sauvegarder_donnees)

    def lancer_application(self):
        self.vue.show()
        sys.exit(self.app.exec())

    def traiter_clic_utilisation(self, row, col):
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

    def traiter_clic_creation(self, row, col):
        dernier_champ = None
        for i in range(self.vue.zone_produits.count()-1, -1, -1):
            widget = self.vue.zone_produits.itemAt(i).widget()
            if widget.toPlainText().strip() != "":
                dernier_champ = widget
                break

        if dernier_champ:
            texte = dernier_champ.toPlainText().strip()
            self.modele.ajouter_produit_emplacement(texte, row, col)
            self.vue.afficher_popup("Produit placé", f"Produit '{texte}' positionné en ({row}, {col})")
            dernier_champ.clear()
        else:
            self.vue.afficher_popup("Erreur", "Veuillez d'abord saisir un produit avant de cliquer sur une case.")

    def sauvegarder_donnees(self):
        self.modele.sauvegarder_csv("produits_place.csv")
        self.vue.afficher_popup("Sauvegarde", "Les produits ont été sauvegardés dans le fichier CSV.")

if __name__ == "__main__":
    controleur = Controleur()
    controleur.lancer_application()