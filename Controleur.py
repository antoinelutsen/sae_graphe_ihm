import sys
from PyQt6.QtWidgets import QApplication, QInputDialog, QMessageBox, QLineEdit
from Modele import ModeleMagasin
from VueCreation import VuePlanCreation
from VueAccueil import VueAccueil
from VueUtilisation import VuePlanUtilisation

# Classe principale : orchestre l'interaction entre la vue et le modèle
class Controleur:

    def __init__(self):
        self.app = QApplication(sys.argv)
        self.modele = ModeleMagasin()
        self.modele.charger_csv("liste_produits.csv")
        self.modele.charger_descriptif("description.json") 
 
        self.vue_accueil = VueAccueil()
        self.vue_accueil.mode_selectionne.connect(self.changer_mode)

    def lancer_application(self): # Lance la boucle principale de l'application
        self.vue_accueil.show()
        self.app.exec()

    def changer_mode(self, mode): # Gère le changement de mode depuis l'écran d'accueil (création ou utilisation)
        self.vue_accueil.close()
        if mode == "creation": # Mode création : demande un mot de passe puis ouvre l'interface de placement des produits
            mdp, ok = QInputDialog.getText(None, "Authentification", "Mot de passe :", echo=QLineEdit.EchoMode.Password)
            if ok and mdp == "admin":
                self.vue_creation = VuePlanCreation("plan.jpg", cell_size=8)
                self.vue_creation.celluleCliquee.connect(self.traiter_clic_creation)
                self.vue_creation.bouton_sauvegarder.clicked.connect(self.sauvegarder_donnees)
                descriptif = self.modele.get_descriptif()
                self.vue_creation.mettre_a_jour_descriptif(descriptif)
                self.vue_creation.bouton_info.clicked.connect(lambda : self.afficher_info_plan_creation(descriptif))
                self.vue_creation.show()
            else:
                QMessageBox.warning(None, "Erreur", "Mot de passe incorrect")
                self.vue_accueil.show()
        elif mode == "utilisation": # Mode utilisation : charge les données du magasin et permet de consulter les produits par secteur
            self.vue_utilisation = VuePlanUtilisation("plan.jpg", cell_size=8)
            self.vue_utilisation.celluleCliquee.connect(self.traiter_clic_utilisation)
            donnees_vue = self.vue_utilisation.get_secteurs_et_cases()
            self.modele.set_grille_magasin(donnees_vue["sectors"], donnees_vue["inaccessibles"])
            self.modele.charger_ou_placer_produits("liste_produits.csv", "produits_place.csv")
            self.vue_utilisation.produitsModifies.connect(self.mettre_a_jour_chemin)
            self.position_entree = (101, 108)
            self.positions_sortie = self.modele.get_cases_secteur("Sortie")
            chemin_initial = self.modele.construire_chemin_depuis_entree(self.position_entree, [])
            self.vue_utilisation.afficher_chemin(chemin_initial)
            descriptif = self.modele.get_descriptif()
            self.vue_utilisation.mettre_a_jour_descriptif(descriptif)
            self.vue_utilisation.bouton_info.clicked.connect(lambda : self.afficher_info_plan_utilisation(descriptif))
            self.vue_utilisation.show()

    def on_produits_modifies(self, produits):
        chemin = self.modele.construire_chemin_depuis_entree(self.position_entree, produits)
        self.vue_utilisation.afficher_chemin(chemin)

    def traiter_clic_utilisation(self, row, col):
        # Lorsqu'une cellule est cliquée en mode utilisation :
        # - identifie le secteur concerné
        # - récupère les produits associés via le modèle
        # - affiche les produits dans une infobulle ou vide l'affichage si aucun secteur
        for secteur, infos in self.vue_utilisation.sectors.items():
            if (row, col) in infos["cells"]:
                produits = self.modele.get_produits(secteur)
                self.vue_utilisation.afficher_produits_secteur(
                    secteur, produits, col * self.vue_utilisation.cell_size, row * self.vue_utilisation.cell_size
                )
                break
        else:
            self.vue_utilisation.vider_produits_secteur()

    def traiter_clic_creation(self, row, col):
        # Lorsqu'une cellule est cliquée en mode création :
        # - récupère le dernier champ de saisie non vide
        # - place le produit dans la grille via le modèle
        # - vide le champ après placement ou affiche une erreur si aucun produit saisi
        dernier_champ = None
        for i in range(self.vue_creation.zone_produits.count() - 1, -1, -1):
            widget = self.vue_creation.zone_produits.itemAt(i).widget()
            if widget.toPlainText().strip() != "":
                dernier_champ = widget
                break

        if dernier_champ:
            texte = dernier_champ.toPlainText().strip()
            secteur_courant = None
            for secteur, infos in self.vue_creation.sectors.items():
                if (row, col) in infos["cells"]:
                    secteur_courant = secteur
                    break

            rayon = secteur_courant if secteur_courant is not None else "Inconnu"

            self.modele.ajouter_produit_emplacement(texte, row, col, rayon)
            self.vue_creation.afficher_popup("Produit placé", f"Produit '{texte}' positionné en ({row}, {col}) dans secteur {rayon}")
            dernier_champ.clear()
        else:
            self.vue_creation.afficher_popup("Erreur", "Veuillez d'abord saisir un produit avant de cliquer sur une case.")

    def sauvegarder_donnees(self): # Sauvegarde l'état actuel des produits placés dans un fichier CSV
        self.modele.sauvegarder_csv("produits_place.csv")
        self.vue_creation.afficher_popup("Sauvegarde", "Les produits ont été sauvegardés dans le fichier CSV.")

    def mettre_a_jour_chemin(self, liste_produits):
        chemin = self.modele.construire_chemin_depuis_entree(self.position_entree, liste_produits)
        self.vue_utilisation.afficher_chemin(chemin)
        self.calculer_distance_marches(chemin)

    def calculer_distance_marches(self, chemin):
        distance = len(chemin) // 5
        self.vue_utilisation.afficher_distance(distance)

    def afficher_info_plan_utilisation(self, _=None):
        descriptif = self.modele.get_descriptif()
        self.vue_utilisation.afficher_info_zone_plan(descriptif)

    def afficher_info_plan_creation(self, _=None):
        descriptif = self.modele.get_descriptif()
        self.vue_creation.afficher_info_zone_plan(descriptif)
