import sys
from PyQt6.QtWidgets import QApplication, QInputDialog, QMessageBox, QLineEdit
from Modele import ModeleMagasin
from Vue import *

class Controleur:

    def __init__(self):
        self.app = QApplication(sys.argv)
        self.modele = ModeleMagasin()
        self.modele.charger_csv("liste_produits.csv")
        
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
        self.vue_accueil = VueAccueil()
        self.vue_accueil.mode_selectionne.connect(self.changer_mode)

    def lancer_application(self):
        self.vue_accueil.show()
        self.app.exec()

    def changer_mode(self, mode):
        self.vue_accueil.close()
        if mode == "creation":
            mdp, ok = QInputDialog.getText(None, "Authentification", "Mot de passe :", echo=QLineEdit.EchoMode.Password)
            if ok and mdp == "admin":
                self.vue_creation = VuePlanCreation("plan.jpg", cell_size=8)
                self.vue_creation.celluleCliquee.connect(self.traiter_clic_creation)
                self.vue_creation.bouton_sauvegarder.clicked.connect(self.sauvegarder_donnees)
                self.vue_creation.show()
            else:
                QMessageBox.warning(None, "Erreur", "Mot de passe incorrect")
                self.vue_accueil.show()
        elif mode == "utilisation":
            self.vue_utilisation = VuePlanUtilisation("plan.jpg", cell_size=8)
            self.vue_utilisation.celluleCliquee.connect(self.traiter_clic_utilisation)
            self.vue_utilisation.show()

    def traiter_clic_utilisation(self, row, col):
        for secteur, infos in self.vue_utilisation.sectors.items():
            if (row, col) in infos["cells"]:
                rayon = self.correspondance_secteurs_rayons.get(secteur)
                if rayon:
                    produits = self.modele.get_produits(rayon)
                    self.vue_utilisation.afficher_produits_secteur(secteur, produits, col * self.vue_utilisation.cell_size, row * self.vue_utilisation.cell_size)
                else:
                    self.vue_utilisation.afficher_produits_secteur(secteur, [])
                break
        else:
            self.vue_utilisation.vider_produits_secteur()

    def traiter_clic_creation(self, row, col):
        dernier_champ = None
        for i in range(self.vue_creation.zone_produits.count()-1, -1, -1):
            widget = self.vue_creation.zone_produits.itemAt(i).widget()
            if widget.toPlainText().strip() != "":
                dernier_champ = widget
                break

        if dernier_champ:
            texte = dernier_champ.toPlainText().strip()
            self.modele.ajouter_produit_emplacement(texte, row, col)
            self.vue_creation.afficher_popup("Produit placé", f"Produit '{texte}' positionné en ({row}, {col})")
            dernier_champ.clear()
        else:
            self.vue_creation.afficher_popup("Erreur", "Veuillez d'abord saisir un produit avant de cliquer sur une case.")

    def sauvegarder_donnees(self):
        self.modele.sauvegarder_csv("produits_place.csv")
        self.vue_creation.afficher_popup("Sauvegarde", "Les produits ont été sauvegardés dans le fichier CSV.")
