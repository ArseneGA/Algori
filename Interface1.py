from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel,
    QTabWidget, QPushButton, QComboBox, QLineEdit, QWidget,
    QFileDialog, QSpinBox, QScrollArea, QCheckBox, QFormLayout,QMessageBox
)
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import os
import random
from tqdm import tqdm

from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar
)
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle

from mpl_toolkits.mplot3d import Axes3D



class AlgemaApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ALGORI")
        self.setGeometry(100, 100, 800, 600)

        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Tab widget
        self.tab_widget = QTabWidget()
        self.central_layout = QVBoxLayout()
        self.central_layout.addWidget(self.tab_widget)
        self.central_widget.setLayout(self.central_layout)

        # Add tabs
        self.home_tab = self.create_home_tab()
        self.selection_tab = self.create_selection_tab()
        self.tab_widget.addTab(self.home_tab, "Accueil")
        self.tab_widget.addTab(self.selection_tab, "Sélection de Fonction")

        self.curve_tabs = {}  # Store dynamically created tabs for curves

        # Onglet de génération hasardeuse
        random_generation_tab = self.create_random_generation_tab()
        self.tab_widget.addTab(random_generation_tab, "Génération hasardeuse")

        # Onglet des fonctions au pas
        step_function_tab = self.create_step_function_tab()
        self.tab_widget.addTab(step_function_tab, "Fonctions au pas")

        # Onglet de construction de la fonction
        function_construction_tab = self.create_function_construction_tab()
        self.tab_widget.addTab(function_construction_tab, "Construction de la fonction")






    def close_tab(self, tab_widget):
        """
        Ferme l'onglet correspondant au widget donné.
        """
        current_index = self.tab_widget.indexOf(tab_widget)
        if current_index != -1:
            self.tab_widget.removeTab(current_index)


    def create_step_function_tab(self):
        """Créer un onglet pour la génération de fonctions au pas."""
        step_function_widget = QWidget()
        layout = QVBoxLayout()

        # Label pour expliquer l'objectif
        label = QLabel("Choisissez une fonction pour la génération au pas")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        # Dropdown pour sélectionner une fonction
        self.step_function_selector = QComboBox()
        self.step_function_selector.addItems([
            "Lissajous 2D", "Lissajous 3D", "Superformule",
            "Clelie 3D", "Exponentielle", "Hypertrochoïde"
        ])
        layout.addWidget(self.step_function_selector)

        # Bouton pour continuer
        proceed_button = QPushButton("Continuer")
        proceed_button.clicked.connect(self.open_step_function_curve_tab)
        layout.addWidget(proceed_button)

        step_function_widget.setLayout(layout)
        return step_function_widget

    def open_step_function_curve_tab(self):
        """
        Ouvre un onglet pour une fonction sélectionnée dans le mode au pas.
        """
        # Récupérer la fonction sélectionnée dans le menu déroulant
        selected_function = self.step_function_selector.currentText()

        # Vérifier si l'onglet existe déjà
        if f"Step {selected_function}" in self.curve_tabs:
            self.tab_widget.setCurrentWidget(self.curve_tabs[f"Step {selected_function}"])
            return

        # Créer un onglet spécifique à la fonction sélectionnée
        if selected_function == "Lissajous 2D":
            tab = self.create_lissajous_2d_step_tab()
        elif selected_function == "Lissajous 3D":
            tab = self.create_lissajous_3d_step_tab()
        elif selected_function == "Superformule":
            tab = self.create_superformule_step_tab()
        elif selected_function == "Clelie 3D":
            tab = self.create_clelie_3d_step_tab()
        elif selected_function == "Exponentielle":
            tab = self.create_exponentielle_step_tab()
        elif selected_function == "Hypertrochoïde":
            tab = self.create_hypertrochoid_step_tab()
        else:
            return  # Si aucune correspondance, ne rien faire

        # Ajouter le nouvel onglet et le rendre actif
        self.curve_tabs[f"Step {selected_function}"] = tab
        self.tab_widget.addTab(tab, f"Step : {selected_function}")
        self.tab_widget.setCurrentWidget(tab)


    def create_random_generation_tab(self):
        """Créer un onglet pour la génération hasardeuse."""
        random_generation_widget = QWidget()
        layout = QVBoxLayout()

        # Label pour expliquer l'objectif
        label = QLabel("Choisissez une fonction pour la génération hasardeuse")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        # Dropdown pour sélectionner une fonction
        self.random_function_selector = QComboBox()
        self.random_function_selector.addItems([
            "Lissajous 2D", "Lissajous 3D", "Superformule",
            "Clelie 3D", "Exponentielle", "Hypertrochoïde"
        ])
        layout.addWidget(self.random_function_selector)

        # Bouton pour continuer
        proceed_button = QPushButton("Continuer")
        proceed_button.clicked.connect(self.open_random_generation_curve_tab)
        layout.addWidget(proceed_button)

        random_generation_widget.setLayout(layout)
        return random_generation_widget


    def open_random_generation_function_tab(self):
        """
        Ouvre un onglet pour la génération hasardeuse en fonction de la sélection.
        """
        # Récupérer la fonction sélectionnée dans le menu déroulant
        selected_function = self.random_function_selector.currentText()

        # Vérifier si l'onglet existe déjà
        if selected_function in self.curve_tabs:
            self.tab_widget.setCurrentWidget(self.curve_tabs[selected_function])
            return

        # Créer un onglet spécifique à la fonction sélectionnée
        if selected_function == "Lissajous 2D":
            tab = self.create_lissajous_2d_random_tab()
        elif selected_function == "Lissajous 3D":
            tab = self.create_lissajous_3d_random_tab()
        elif selected_function == "Superformule":
            tab = self.create_superformule_random_tab()
        elif selected_function == "Clelie 3D":
            tab = self.create_clelie_3d_random_tab()
        elif selected_function == "Exponentielle":
            tab = self.create_exponentielle_random_tab()
        elif selected_function == "Hypertrochoïde":
            tab = self.create_hypertrochoid_random_tab()
        else:
            return  # Si aucune correspondance, ne rien faire

        # Ajouter le nouvel onglet et le rendre actif
        self.curve_tabs[selected_function] = tab
        self.tab_widget.addTab(tab, f"Génération : {selected_function}")
        self.tab_widget.setCurrentWidget(tab)

    def close_tab(self, tab_widget):
        current_index = self.tab_widget.indexOf(tab_widget)
        if current_index != -1:
            # Identifier le nom de la courbe associée à l'onglet
            curve_name = [name for name, widget in self.curve_tabs.items() if widget == tab_widget]
            if curve_name:
                del self.curve_tabs[curve_name[0]]  # Supprimer la clé correspondante
            self.tab_widget.removeTab(current_index)



    def create_home_tab(self):
        # Home tab: Welcome screen
        home_widget = QWidget()
        layout = QVBoxLayout()
        label = QLabel("Bienvenue sur ALGORI")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("color: white; font-size: 70px;")
        home_widget.setStyleSheet("background-color: black;")
        layout.addWidget(label)
        home_widget.setLayout(layout)
        return home_widget

    def create_selection_tab(self):
        # Selection tab: Dropdown to choose curve type
        selection_widget = QWidget()
        layout = QVBoxLayout()

        # Label for selection
        label = QLabel("Choisissez avec quelle fonction vous voulez vous amuser")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("font-size: 18px; color: black;")
        layout.addWidget(label)

        # Dropdown for selecting function
        self.curve_selector = QComboBox()
        self.curve_selector.addItems([
            "Lissajous 2D", "Lissajous 3D", "Superformule", 
            "Clelie 3D", "Exponentielle", "Hypertrochoïde"
        ])
        layout.addWidget(self.curve_selector)

        # Button to confirm selection
        select_button = QPushButton("Sélectionner")
        select_button.clicked.connect(self.open_function_curve_tab)
        layout.addWidget(select_button)

        selection_widget.setLayout(layout)
        return selection_widget

    def plot_trajectory(self, n, a, b, theta_range, color, background, line_width, num_points):
        """
        Trace la trajectoire exponentielle basée sur les paramètres donnés.
        
        Parameters:
        - n: Nombre de termes.
        - a: Liste des longueurs des barres.
        - b: Liste des vitesses angulaires.
        - theta_range: Tuple définissant le début et la fin de theta.
        - color: Couleur de la courbe.
        - background: Couleur de fond.
        - line_width: Épaisseur de la ligne.
        - num_points: Nombre de points pour l'échantillonnage.
        """
        try:
            # Calcul des trajectoires
            theta = np.linspace(theta_range[0], theta_range[1], num_points)
            x = np.zeros_like(theta)
            y = np.zeros_like(theta)

            for i in range(n):
                x += a[i] * np.cos(b[i] * theta)
                y += a[i] * np.sin(b[i] * theta)

            # Création de la figure
            fig, ax = plt.subplots(figsize=(6, 6))
            ax.plot(x, y, color=color, linewidth=line_width)
            ax.set_facecolor(background)
            ax.axis('off')

            return fig

        except Exception as e:
            print(f"Erreur dans plot_trajectory: {e}")
            return None


    def open_function_curve_tab(self):
        """
        Ouvre un onglet pour une courbe sélectionnée dans l'onglet de sélection de fonction.
        """
        curve_name = self.curve_selector.currentText()

        # Vérifie si l'onglet existe déjà
        if curve_name in self.curve_tabs:
            self.tab_widget.setCurrentWidget(self.curve_tabs[curve_name])
            return

        # Crée l'onglet en fonction de la courbe sélectionnée
        if curve_name == "Lissajous 2D":
            curve_tab = self.create_lissajous_2d_tab()
        elif curve_name == "Lissajous 3D":
            curve_tab = self.create_lissajous_3d_tab()
        elif curve_name == "Superformule":
            curve_tab = self.create_superformula_tab()
        elif curve_name == "Clelie 3D":
            curve_tab = self.create_clelie_3d_tab()
        elif curve_name == "Exponentielle":
            curve_tab = self.create_exponentielle_tab()
        elif curve_name == "Hypertrochoïde":
            curve_tab = self.create_hypertrochoid_tab()
        else:
            curve_tab = QWidget()  # Onglet placeholder si aucune correspondance

        # Ajoute et sélectionne le nouvel onglet
        self.curve_tabs[curve_name] = curve_tab
        self.tab_widget.addTab(curve_tab, curve_name)
        self.tab_widget.setCurrentWidget(curve_tab)


    def open_random_generation_curve_tab(self):
        """
        Ouvre un onglet pour une courbe avec des paramètres générés aléatoirement.
        """
        curve_name = self.random_function_selector.currentText()

        # Vérifie si l'onglet existe déjà
        if f"Random {curve_name}" in self.curve_tabs:
            self.tab_widget.setCurrentWidget(self.curve_tabs[f"Random {curve_name}"])
            return

        # Crée l'onglet en fonction de la courbe sélectionnée
        if curve_name == "Lissajous 2D":
            curve_tab = self.create_lissajous_2d_random_tab()
        elif curve_name == "Lissajous 3D":
            curve_tab = self.create_lissajous_3d_random_tab()
        elif curve_name == "Superformule":
            curve_tab = self.create_superformule_random_tab()
        elif curve_name == "Clelie 3D":
            curve_tab = self.create_clelie_3d_random_tab()
        elif curve_name == "Exponentielle":
            curve_tab = self.create_exponentielle_random_tab()
        elif curve_name == "Hypertrochoïde":
            curve_tab = self.create_hypertrochoid_random_tab()
        # Ajoutez les autres types de courbes ici
        else:
            curve_tab = QWidget()  # Onglet placeholder si aucune correspondance

        # Ajoute et sélectionne le nouvel onglet
        self.curve_tabs[f"Random {curve_name}"] = curve_tab
        self.tab_widget.addTab(curve_tab, f"Random {curve_name}")
        self.tab_widget.setCurrentWidget(curve_tab)


    def create_function_construction_tab(self):
        """
        Crée un onglet principal pour la sélection d'une fonction à construire.
        Comprend une liste déroulante pour choisir une fonction et un bouton pour ouvrir un onglet spécifique.
        """
        construction_widget = QWidget()
        layout = QVBoxLayout()

        # Title
        title = QLabel("Construction Interactive de Fonctions")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)

        # Instructions
        instructions = QLabel("Sélectionnez une fonction dans la liste déroulante et cliquez sur 'Construire'.")
        instructions.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(instructions)

        # Function selector
        function_selector = QComboBox()
        function_selector.addItems([
            "Lissajous 2D",
            "Lissajous 3D",
            "Clélie 3D",
        ])
        layout.addWidget(QLabel("Sélectionnez une fonction :"))
        layout.addWidget(function_selector)

        # Button to open specific tab
        construct_button = QPushButton("Construire")
        layout.addWidget(construct_button)

        def open_function_tab():
            selected_function = function_selector.currentText()

            # Check if the tab already exists
            if selected_function in self.curve_tabs:
                self.tab_widget.setCurrentWidget(self.curve_tabs[selected_function])
                return

            # Open specific tabs based on function
            if selected_function == "Lissajous 2D":
                tab = self.create_lissajous_2d_construction_tab()
            elif selected_function == "Lissajous 3D":
                tab = self.create_lissajous_3d_construction_tab()
            elif selected_function == "Clélie 3D":
                tab = self.create_clelie_3d_construction_tab()
            else:
                return  # Do nothing if no matching function

            # Add and switch to the new tab
            self.curve_tabs[selected_function] = tab
            self.tab_widget.addTab(tab, f"Construction : {selected_function}")
            self.tab_widget.setCurrentWidget(tab)

        construct_button.clicked.connect(open_function_tab)

        construction_widget.setLayout(layout)
        return construction_widget



    def open_function_construction_tab(self, function_name):
        """
        Ouvre un onglet pour la construction interactive de la fonction sélectionnée.
        """
        if function_name in self.curve_tabs:
            # Si l'onglet existe déjà, le rendre actif
            self.tab_widget.setCurrentWidget(self.curve_tabs[function_name])
            return

        if function_name == "Lissajous 2D":
            tab = self.create_lissajous_2d_construction_tab()
        elif function_name == "Lissajous 3D":
            tab = self.create_lissajous_3d_construction_tab()
        elif function_name == "Clélie 3D":
            tab = self.create_clelie_3d_construction_tab()
        else:
            return  # Si aucune correspondance, ne rien faire

        # Ajouter et afficher le nouvel onglet
        self.curve_tabs[function_name] = tab
        self.tab_widget.addTab(tab, f"Construction : {function_name}")
        self.tab_widget.setCurrentWidget(tab)

# +++++++++++++++++++++++++++++++     HASARD     ++++++++++++++++++++++++++++++++++++























































    def toggle_constant_input(self, state, widgets):
        is_constant = state == Qt.CheckState.Checked
        widgets[0].setDisabled(is_constant)  # Min
        widgets[1].setDisabled(is_constant)  # Max
        widgets[2].setDisabled(not is_constant)  # Constante



    def create_lissajous_2d_random_tab(self):
        curve_widget = QWidget()
        main_layout = QVBoxLayout()

        # Title
        title = QLabel("Génération aléatoire : Lissajous 2D")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        # Number of curves to generate
        num_curves_layout = QHBoxLayout()
        num_curves_label = QLabel("Nombre de courbes :")
        num_curves_input = QLineEdit("5")
        num_curves_layout.addWidget(num_curves_label)
        num_curves_layout.addWidget(num_curves_input)
        main_layout.addLayout(num_curves_layout)

        # Parameters section
        parameters_layout = QVBoxLayout()
        inputs = {}

        for param, default_range in {"A": (1, 10), "B": (1, 10), "p": (1, 5), "q": (1, 5), "delta": (0, 2 * np.pi)}.items():
            param_layout = QHBoxLayout()
            label = QLabel(f"{param} :")
            min_input = QLineEdit(str(default_range[0]))
            min_input.setPlaceholderText("Min")
            max_input = QLineEdit(str(default_range[1]))
            max_input.setPlaceholderText("Max")
            param_layout.addWidget(label)
            param_layout.addWidget(min_input)
            param_layout.addWidget(max_input)
            parameters_layout.addLayout(param_layout)

            inputs[param] = {"min": min_input, "max": max_input}

        main_layout.addLayout(parameters_layout)

        # Preview section
        preview_label = QLabel("Aperçu de la courbe :")
        preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(preview_label)

        preview_area = QLabel()
        preview_area.setFixedSize(600, 600)
        preview_area.setStyleSheet("background-color: white; border: 1px solid black;")
        main_layout.addWidget(preview_area)

        # Buttons
        button_layout = QHBoxLayout()

        # Generate button
        generate_button = QPushButton("Générer")
        generate_button.clicked.connect(
            lambda: self.generate_lissajous_2d_random(num_curves_input, inputs)
        )

        button_layout.addWidget(generate_button)

        # Back button
        back_button = QPushButton("Retour")
        back_button.clicked.connect(lambda: self.close_tab(curve_widget))
        button_layout.addWidget(back_button)

        main_layout.addLayout(button_layout)
        curve_widget.setLayout(main_layout)

        return curve_widget


    def generate_lissajous_2d_random(self, num_curves_input, inputs):
        try:
            # Récupérer le nombre de courbes à générer
            num_curves = int(num_curves_input.text())
            if num_curves <= 0:
                raise ValueError("Le nombre de courbes doit être supérieur à zéro.")

            # Demander à l'utilisateur de choisir un dossier pour enregistrer les fichiers
            output_folder = QFileDialog.getExistingDirectory(
                self,
                "Choisissez un dossier pour enregistrer les images"
            )
            if not output_folder:  # Si l'utilisateur annule, ne rien faire
                return

            # Générer et enregistrer les courbes
            for i in range(1, num_curves + 1):
                # Générer des paramètres aléatoires pour chaque courbe
                params = {
                    param: np.random.uniform(
                        float(inputs[param]["min"].text()),
                        float(inputs[param]["max"].text())
                    ) for param in inputs
                }

                # Calculer les points de la courbe
                t = np.linspace(0, 2 * np.pi, 1000)
                x = params["A"] * np.sin(params["p"] * t + params["delta"])
                y = params["B"] * np.sin(params["q"] * t)

                # Créer un graphique
                fig, ax = plt.subplots(figsize=(6, 6))
                ax.set_aspect('equal')
                ax.plot(x, y, linewidth=2, color='blue')
                ax.set_facecolor('white')
                ax.axis('off')  # Pas d'axes
                

                # Générer un nom de fichier basé sur les paramètres
                filename = (
                    f"Lissajous2D_A{params['A']:.2f}_B{params['B']:.2f}_"
                    f"p{params['p']:.2f}_q{params['q']:.2f}_delta{params['delta']:.2f}.png"
                )
                filepath = os.path.join(output_folder, filename)

                # Sauvegarder l'image
                plt.savefig(filepath, dpi=300, bbox_inches='tight', pad_inches=0, facecolor='white')
                plt.close(fig)  # Fermer la figure pour économiser de la mémoire

                print(f"Image enregistrée : {filepath}")

            print(f"Toutes les courbes ont été enregistrées dans {output_folder}")

        except ValueError as ve:
            print(f"Erreur : {ve}")
        except Exception as e:
            print(f"Une erreur est survenue : {e}")
            
    def create_lissajous_3d_random_tab(self):
        import random  # Ajout de l'importation ici pour éviter les erreurs
        curve_widget = QWidget()
        main_layout = QVBoxLayout()

        # Title
        title = QLabel("Génération aléatoire : Lissajous 3D")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        # Scrollable area for parameters
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)

        # Nombre de courbes
        num_curves_layout = QHBoxLayout()
        num_curves_label = QLabel("Nombre de courbes à générer :")
        num_curves_input = QLineEdit("5")
        num_curves_layout.addWidget(num_curves_label)
        num_curves_layout.addWidget(num_curves_input)
        scroll_layout.addLayout(num_curves_layout)

        # Paramètres pour chaque courbe
        inputs = {}
        for param, default_range in {
            "A": 1, "B": 1, "C": 1,  # Constants
            "p": (1, 5), "q": (1, 5), "r": (1, 5),
            "delta": (0, 2 * np.pi), "phi": (0, 2 * np.pi),
            "couleur": "blue", "fond": "white", "épaisseur": 2
        }.items():
            if isinstance(default_range, tuple):
                label = QLabel(f"{param} (min/max):")
                min_input = QLineEdit(str(random.uniform(default_range[0], default_range[1])))
                max_input = QLineEdit(str(random.uniform(default_range[0], default_range[1])))
                param_layout = QHBoxLayout()
                param_layout.addWidget(label)
                param_layout.addWidget(min_input)
                param_layout.addWidget(max_input)
                scroll_layout.addLayout(param_layout)
                inputs[param] = {"min": min_input, "max": max_input}
            else:
                label = QLabel(f"{param}:")
                input_field = QLineEdit(str(default_range))
                param_layout = QHBoxLayout()
                param_layout.addWidget(label)
                param_layout.addWidget(input_field)
                scroll_layout.addLayout(param_layout)
                inputs[param] = input_field

        scroll_area.setWidget(scroll_widget)
        main_layout.addWidget(scroll_area)

        # Buttons
        button_layout = QHBoxLayout()

        # Generate and save button
        def save_lissajous_3d_random():
            try:
                num_curves = int(num_curves_input.text())
                if num_curves <= 0:
                    raise ValueError("Le nombre de courbes doit être supérieur à 0.")

                # Récupération des paramètres
                params = {}
                for param, widget in inputs.items():
                    if isinstance(widget, dict):  # For ranges
                        params[param] = {
                            "min": float(widget["min"].text()),
                            "max": float(widget["max"].text())
                        }
                    else:
                        params[param] = widget.text() if param in ["couleur", "fond"] else float(widget.text())

                # Enregistrement des courbes
                file_types = "PNG Files (*.png);;SVG Files (*.svg)"
                save_dir = QFileDialog.getExistingDirectory(self, "Sélectionnez un dossier pour enregistrer les courbes")
                if not save_dir:
                    return

                for i in range(num_curves):
                    # Génération des paramètres aléatoires pour chaque courbe
                    current_params = {
                        param: random.uniform(params[param]["min"], params[param]["max"])
                        if isinstance(params[param], dict) else params[param]
                        for param in params
                    }

                    # Génération des courbes
                    t = np.linspace(0, 2 * np.pi, 1000)
                    x = current_params["A"] * np.sin(current_params["p"] * t + current_params["delta"])
                    y = current_params["B"] * np.sin(current_params["q"] * t + current_params["phi"])
                    z = current_params["C"] * np.sin(current_params["r"] * t)

                    # Création de l'image
                    fig, ax = plt.subplots(figsize=(6, 6))
                    ax.set_aspect('equal')
                    ax = fig.add_subplot(111, projection='3d')
                    ax.plot(x, y, z, color=current_params["couleur"], linewidth=current_params["épaisseur"])
                    ax.set_facecolor(current_params["fond"])
                    ax.axis('off')

                    # Sauvegarde de l'image
                    file_name = os.path.join(
                        save_dir,
                        f"Lissajous3D_{i + 1}_p{current_params['p']:.2f}_q{current_params['q']:.2f}_r{current_params['r']:.2f}.png"
                    )
                    plt.savefig(file_name, facecolor=current_params["fond"], dpi=300)
                    plt.close(fig)

                print(f"{num_curves} courbes enregistrées dans {save_dir}")
            except Exception as e:
                print(f"Erreur lors de l'enregistrement : {e}")

        save_button = QPushButton("Enregistrer")
        save_button.clicked.connect(save_lissajous_3d_random)
        button_layout.addWidget(save_button)

        # Back button
        back_button = QPushButton("Retour")
        back_button.clicked.connect(lambda: self.close_tab(curve_widget))
        button_layout.addWidget(back_button)

        main_layout.addLayout(button_layout)
        curve_widget.setLayout(main_layout)

        return curve_widget


    def generate_lissajous_3d_random(self, num_curves_input, input_widgets, preview_area):
        """
        Fonction pour générer les courbes Lissajous 3D de manière aléatoire
        """
        try:
            # Récupérer le nombre de courbes à générer
            num_curves = num_curves_input.value()

            # Récupérer les paramètres pour chaque caractéristique
            A = float(input_widgets["A"]["min"].text())
            B = float(input_widgets["B"]["min"].text())
            C = float(input_widgets["C"]["min"].text())
            p = float(input_widgets["p"]["min"].text())
            q = float(input_widgets["q"]["min"].text())
            r = float(input_widgets["r"]["min"].text())
            delta = float(input_widgets["delta"]["min"].text())
            phi = float(input_widgets["phi"]["min"].text())

            # Calculer les valeurs de t
            t = np.linspace(0, 2 * np.pi, 1000)

            # Boucle pour générer chaque courbe
            for i in range(num_curves):
                # Générer des valeurs aléatoires dans les intervalles donnés
                A_val = np.random.uniform(A, float(input_widgets["A"]["max"].text()))
                B_val = np.random.uniform(B, float(input_widgets["B"]["max"].text()))
                C_val = np.random.uniform(C, float(input_widgets["C"]["max"].text()))
                p_val = np.random.uniform(p, float(input_widgets["p"]["max"].text()))
                q_val = np.random.uniform(q, float(input_widgets["q"]["max"].text()))
                r_val = np.random.uniform(r, float(input_widgets["r"]["max"].text()))
                delta_val = np.random.uniform(delta, float(input_widgets["delta"]["max"].text()))
                phi_val = np.random.uniform(phi, float(input_widgets["phi"]["max"].text()))

                # Calculer les coordonnées de la courbe
                x = A_val * np.sin(p_val * t + delta_val)
                y = B_val * np.sin(q_val * t)
                z = C_val * np.sin(r_val * t + phi_val)

                # Tracer la courbe
                fig, ax = plt.subplots(figsize=(6, 6), dpi=100, subplot_kw={"projection": "3d"})
                ax.set_aspect('equal')
                ax.plot(x, y, z, color='blue')
                ax.set_facecolor('white')
                ax.axis('off')

                # Mettre à jour l'aperçu
                buf = BytesIO()
                plt.savefig(buf, format='png', facecolor='white')
                buf.seek(0)
                img = QImage()
                img.loadFromData(buf.getvalue())
                pixmap = QPixmap.fromImage(img)
                preview_area.setPixmap(pixmap)
                preview_area.adjustSize()

                plt.close(fig)

        except Exception as e:
            print(f"Erreur lors de la génération : {e}")



    def create_superformule_random_tab(self):
        curve_widget = QWidget()
        main_layout = QVBoxLayout()

        # Title
        title = QLabel("Génération aléatoire : Superformule")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        # Number of curves to generate
        num_curves_layout = QHBoxLayout()
        num_curves_label = QLabel("Nombre de courbes :")
        num_curves_input = QLineEdit("5")
        num_curves_layout.addWidget(num_curves_label)
        num_curves_layout.addWidget(num_curves_input)
        main_layout.addLayout(num_curves_layout)

        # Parameters section
        parameters_layout = QVBoxLayout()
        inputs = {}

        for param, default_range in {
            "m": (1, 10), "a": (1, 5), "b": (1, 5),
            "n1": (0.1, 5), "n2": (0.1, 5), "n3": (0.1, 5)
        }.items():
            param_layout = QHBoxLayout()
            label = QLabel(f"{param} :")
            min_input = QLineEdit(str(default_range[0]))
            max_input = QLineEdit(str(default_range[1]))
            param_layout.addWidget(label)
            param_layout.addWidget(min_input)
            param_layout.addWidget(max_input)
            parameters_layout.addLayout(param_layout)

            inputs[param] = {"min": min_input, "max": max_input}

        main_layout.addLayout(parameters_layout)

        # Buttons
        button_layout = QHBoxLayout()

        # Generate and save button
        generate_button = QPushButton("Générer et enregistrer")
        generate_button.clicked.connect(
            lambda: self.generate_superformule_random(num_curves_input, inputs)
        )
        button_layout.addWidget(generate_button)

        # Back button
        back_button = QPushButton("Retour")
        back_button.clicked.connect(lambda: self.close_tab(curve_widget))
        button_layout.addWidget(back_button)

        main_layout.addLayout(button_layout)
        curve_widget.setLayout(main_layout)

        return curve_widget


    def generate_superformule_random(self, num_curves_input, inputs):
        import random  # Assurez-vous que le module random est importé

        try:
            # Nombre de courbes à générer
            num_curves = int(num_curves_input.text())
            if num_curves <= 0:
                raise ValueError("Le nombre de courbes doit être supérieur à 0.")

            # Extraction des paramètres et de leurs plages
            params = {}
            for param, widget in inputs.items():
                params[param] = {
                    "min": float(widget["min"].text()),
                    "max": float(widget["max"].text())
                }

            # Sélection du dossier de sauvegarde
            save_dir = QFileDialog.getExistingDirectory(self, "Sélectionnez un dossier pour enregistrer les courbes")
            if not save_dir:
                return

            # Génération et sauvegarde des courbes
            for i in range(num_curves):
                # Générer des valeurs aléatoires pour chaque paramètre
                current_params = {
                    param: random.uniform(params[param]["min"], params[param]["max"])
                    for param in params
                }

                # Calcul de la Superformule
                theta = np.linspace(0, 2 * np.pi, 1000)
                m, a, b = current_params["m"], current_params["a"], current_params["b"]
                n1, n2, n3 = current_params["n1"], current_params["n2"], current_params["n3"]
                r = (abs(np.cos(m * theta / 4) / a) ** n2 + abs(np.sin(m * theta / 4) / b) ** n3) ** (-1 / n1)
                x = r * np.cos(theta)
                y = r * np.sin(theta)

                # Création de la figure
                fig, ax = plt.subplots(figsize=(6, 6))
                ax.set_aspect('equal')
                ax.plot(x, y, linewidth=2)
                ax.axis('off')
                ax.set_aspect('equal')

                # Nom du fichier basé sur les paramètres
                file_name = os.path.join(
                    save_dir,
                    f"Superformule_{i + 1}_m{m:.2f}_a{a:.2f}_b{b:.2f}_n1{n1:.2f}_n2{n2:.2f}_n3{n3:.2f}.png"
                )
                plt.savefig(file_name, dpi=300, bbox_inches='tight', pad_inches=0)
                plt.close(fig)

            print(f"{num_curves} courbes Superformule enregistrées dans {save_dir}")

        except Exception as e:
            print(f"Erreur lors de la génération : {e}")





    def create_clelie_3d_random_tab(self):
        curve_widget = QWidget()
        main_layout = QVBoxLayout()

        # Title
        title = QLabel("Génération aléatoire : Clélie 3D")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        # Number of curves to generate
        num_curves_layout = QHBoxLayout()
        num_curves_label = QLabel("Nombre de courbes :")
        num_curves_input = QLineEdit("5")
        num_curves_layout.addWidget(num_curves_label)
        num_curves_layout.addWidget(num_curves_input)
        main_layout.addLayout(num_curves_layout)

        # Parameters section
        parameters_layout = QVBoxLayout()
        inputs = {}

        for param, default_range in {
            "a": (1, 5), "m": (1, 5), "theta max": (2 * np.pi, 10 * np.pi)
        }.items():
            param_layout = QHBoxLayout()
            label = QLabel(f"{param} :")
            min_input = QLineEdit(str(default_range[0]))
            max_input = QLineEdit(str(default_range[1]))
            param_layout.addWidget(label)
            param_layout.addWidget(min_input)
            param_layout.addWidget(max_input)
            parameters_layout.addLayout(param_layout)

            inputs[param] = {"min": min_input, "max": max_input}

        main_layout.addLayout(parameters_layout)

        # Buttons
        button_layout = QHBoxLayout()

        # Generate and save button
        generate_button = QPushButton("Générer et enregistrer")
        generate_button.clicked.connect(
            lambda: self.generate_clelie_3d_random(num_curves_input, inputs)
        )
        button_layout.addWidget(generate_button)

        # Back button
        back_button = QPushButton("Retour")
        back_button.clicked.connect(lambda: self.close_tab(curve_widget))
        button_layout.addWidget(back_button)

        main_layout.addLayout(button_layout)
        curve_widget.setLayout(main_layout)

        return curve_widget
    


    def generate_clelie_3d_random(self, num_curves_input, inputs):
        try:
            num_curves = int(num_curves_input.text())
            folder = QFileDialog.getExistingDirectory(
                self, "Sélectionnez un dossier pour enregistrer les courbes"
            )
            if not folder:
                return  # Ne rien faire si aucun dossier sélectionné

            for i in range(num_curves):
                params = {}
                for param, widget in inputs.items():
                    params[param] = np.random.uniform(
                        float(widget["min"].text()), float(widget["max"].text())
                    )

                # Génération de la courbe Clélie 3D
                a = params["a"]
                m = params["m"]
                theta_max = params["theta max"]
                theta = np.linspace(0, theta_max, 10000)

                x = a * np.cos(m * theta) * np.sin(theta)
                y = a * np.sin(m * theta) * np.sin(theta)
                z = a * np.cos(theta)

                # Enregistrer la courbe
                filename = os.path.join(
                    folder,
                    f"Clelie3D_a{a}_m{m}_theta_max{theta_max}.png"
                )
                fig, ax = plt.subplots(figsize=(6, 6))
                ax = fig.add_subplot(111, projection='3d')
                ax.plot(x, y, z)
                ax.set_axis_off()
                plt.savefig(filename, bbox_inches='tight', pad_inches=0)
                plt.close(fig)
            print(f"{num_curves} courbes Clélie 3D ont été enregistrées dans le dossier : {folder}")
        except Exception as e:
            print(f"Une erreur est survenue : {e}")

    def create_exponentielle_random_tab(self):
        curve_widget = QWidget()
        main_layout = QVBoxLayout()

        # Title
        title = QLabel("Génération aléatoire : Trajectoire Exponentielle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        # Number of curves to generate
        num_curves_layout = QHBoxLayout()
        num_curves_label = QLabel("Nombre de courbes :")
        num_curves_input = QLineEdit("5")
        num_curves_layout.addWidget(num_curves_label)
        num_curves_layout.addWidget(num_curves_input)
        main_layout.addLayout(num_curves_layout)

        # Parameters section
        parameters_layout = QVBoxLayout()
        inputs = {}

        for param, default_range in {
            "n": (1, 5), "theta_max": (np.pi, 10 * np.pi), "num_points": (1000, 5000)
        }.items():
            param_layout = QHBoxLayout()
            label = QLabel(f"{param} :")
            min_input = QLineEdit(str(default_range[0]))
            max_input = QLineEdit(str(default_range[1]))
            param_layout.addWidget(label)
            param_layout.addWidget(min_input)
            param_layout.addWidget(max_input)
            parameters_layout.addLayout(param_layout)
            inputs[param] = {"min": min_input, "max": max_input}

        main_layout.addLayout(parameters_layout)

        # Buttons
        button_layout = QHBoxLayout()

        # Generate and save button
        generate_button = QPushButton("Générer et enregistrer")
        generate_button.clicked.connect(
            lambda: self.generate_exponentielle_random(num_curves_input, inputs)
        )
        button_layout.addWidget(generate_button)

        # Back button
        back_button = QPushButton("Retour")
        back_button.clicked.connect(lambda: self.close_tab(curve_widget))
        button_layout.addWidget(back_button)

        main_layout.addLayout(button_layout)
        curve_widget.setLayout(main_layout)

        return curve_widget


    def generate_exponentielle_random(self, num_curves_input, inputs):
        try:
            num_curves = int(num_curves_input.text())
            folder = QFileDialog.getExistingDirectory(
                self, "Sélectionnez un dossier pour enregistrer les courbes"
            )
            if not folder:
                return  # Ne rien faire si aucun dossier sélectionné

            for i in range(num_curves):
                params = {}
                for param, widget in inputs.items():
                    params[param] = np.random.uniform(
                        float(widget["min"].text()), float(widget["max"].text())
                    )
                n = int(params["n"])
                theta_max = params["theta_max"]
                num_points = int(params["num_points"])

                # Génération de la trajectoire exponentielle
                theta = np.linspace(0, theta_max, num_points)
                x = sum(
                    np.exp(-j * theta) * np.cos(j * theta)
                    for j in range(1, n + 1)
                )
                y = sum(
                    np.exp(-j * theta) * np.sin(j * theta)
                    for j in range(1, n + 1)
                )

                # Enregistrer la courbe
                filename = os.path.join(
                    folder,
                    f"Exponentielle_n{n}_theta{theta_max:.2f}_points{num_points}.png"
                )
                fig, ax = plt.subplots(figsize=(6, 6))
                ax.set_aspect('equal')
                ax.plot(x, y)
                ax.axis("off")
                plt.savefig(filename, bbox_inches='tight', pad_inches=0)
                plt.close(fig)
            print(f"{num_curves} courbes exponentielles ont été enregistrées dans le dossier : {folder}")
        except Exception as e:
            print(f"Une erreur est survenue : {e}")




    def create_hypertrochoid_random_tab(self):
        curve_widget = QWidget()
        main_layout = QVBoxLayout()

        # Title
        title = QLabel("Génération aléatoire : Hypertrochoïde")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        # Number of curves to generate
        num_curves_layout = QHBoxLayout()
        num_curves_label = QLabel("Nombre de courbes :")
        num_curves_input = QLineEdit("5")
        num_curves_layout.addWidget(num_curves_label)
        num_curves_layout.addWidget(num_curves_input)
        main_layout.addLayout(num_curves_layout)

        # Parameters section
        parameters_layout = QVBoxLayout()
        inputs = {}

        for param, default_range in {
            "R": (5, 20), "r": (3, 10), "d": (1, 5), "num_points": (1000, 5000)
        }.items():
            param_layout = QHBoxLayout()
            label = QLabel(f"{param} :")
            min_input = QLineEdit(str(default_range[0]))
            max_input = QLineEdit(str(default_range[1]))
            param_layout.addWidget(label)
            param_layout.addWidget(min_input)
            param_layout.addWidget(max_input)
            parameters_layout.addLayout(param_layout)
            inputs[param] = {"min": min_input, "max": max_input}

        main_layout.addLayout(parameters_layout)

        # Buttons
        button_layout = QHBoxLayout()

        # Generate and save button
        generate_button = QPushButton("Générer et enregistrer")
        generate_button.clicked.connect(
            lambda: self.generate_hypertrochoid_random(num_curves_input, inputs)
        )
        button_layout.addWidget(generate_button)

        # Back button
        back_button = QPushButton("Retour")
        back_button.clicked.connect(lambda: self.close_tab(curve_widget))
        button_layout.addWidget(back_button)

        main_layout.addLayout(button_layout)
        curve_widget.setLayout(main_layout)

        return curve_widget



    def generate_hypertrochoid_random(self, num_curves_input, inputs):
        try:
            num_curves = int(num_curves_input.text())
            folder = QFileDialog.getExistingDirectory(
                self, "Sélectionnez un dossier pour enregistrer les courbes"
            )
            if not folder:
                return  # Ne rien faire si aucun dossier sélectionné

            for i in range(num_curves):
                params = {}
                for param, widget in inputs.items():
                    params[param] = np.random.uniform(
                        float(widget["min"].text()), float(widget["max"].text())
                    )
                R = params["R"]
                r = params["r"]
                d = params["d"]
                num_points = int(params["num_points"])

                # Génération de la courbe Hypertrochoïde
                t = np.linspace(0, 2 * np.pi, num_points)
                x = (R - r) * np.cos(t) + d * np.cos((R - r) / r * t)
                y = (R - r) * np.sin(t) - d * np.sin((R - r) / r * t)

                # Enregistrer la courbe
                filename = os.path.join(
                    folder,
                    f"Hypertrochoid_R{R:.2f}_r{r:.2f}_d{d:.2f}_points{num_points}.png"
                )
                fig, ax = plt.subplots()
                ax.plot(x, y)
                ax.axis("off")
                plt.savefig(filename, bbox_inches='tight', pad_inches=0)
                plt.close(fig)
            print(f"{num_curves} courbes Hypertrochoïdes ont été enregistrées dans le dossier : {folder}")
        except Exception as e:
            print(f"Une erreur est survenue : {e}")







# +++++++++++++++++++++++++++++++    NON HASARD     ++++++++++++++++++++++++++++++++++++





# +++++++++++++++++++++++++++++++       AU PAS      +++++++++++++++++++++++++++++++++++++ 





























    def create_lissajous_2d_step_tab(self):
        """
        Crée un onglet pour générer des courbes Lissajous 2D au pas.
        """
        curve_widget = QWidget()
        main_layout = QVBoxLayout()

        # Titre
        title = QLabel("Génération au pas : Lissajous 2D")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        # Ajouter une note
        note_label = QLabel("Indiquez les valeurs de début et de fin pour chaque paramètre (entiers).\n"
                            "Choisissez également le nombre total de frames.")
        note_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(note_label)

        # Section pour les paramètres
        parameters_layout = QVBoxLayout()
        inputs = {}

        for param in ["p", "q", "delta"]:
            param_layout = QHBoxLayout()
            label = QLabel(f"{param} (début et fin) :")
            start_input = QLineEdit("0")
            end_input = QLineEdit("10")
            param_layout.addWidget(label)
            param_layout.addWidget(start_input)
            param_layout.addWidget(end_input)
            parameters_layout.addLayout(param_layout)
            inputs[param] = {"start": start_input, "end": end_input}

        # Section pour le nombre de frames
        frame_count_layout = QHBoxLayout()
        frame_count_label = QLabel("Nombre de frames :")
        frame_count_input = QLineEdit("10")
        frame_count_layout.addWidget(frame_count_label)
        frame_count_layout.addWidget(frame_count_input)
        parameters_layout.addLayout(frame_count_layout)
        inputs["frame_count"] = frame_count_input

        main_layout.addLayout(parameters_layout)

        # Prévisualisation
        preview_label = QLabel("Aperçu de la première courbe :")
        preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(preview_label)

        preview_area = QLabel()
        preview_area.setFixedSize(600, 600)
        preview_area.setStyleSheet("background-color: white; border: 1px solid black;")
        main_layout.addWidget(preview_area)

        # Boutons
        button_layout = QHBoxLayout()

        # Bouton pour générer les courbes
        generate_button = QPushButton("Générer")
        generate_button.clicked.connect(lambda: self.generate_lissajous_2d_step(inputs, preview_area, main_layout))
        button_layout.addWidget(generate_button)

        # Bouton pour retourner à l'écran précédent
        back_button = QPushButton("Retour")
        back_button.clicked.connect(lambda: self.close_tab(curve_widget))
        button_layout.addWidget(back_button)

        main_layout.addLayout(button_layout)
        curve_widget.setLayout(main_layout)

        return curve_widget

    def generate_lissajous_2d_step(self, inputs, preview_area, preview_layout):
        """
        Génère des courbes Lissajous 2D avec un nombre fixe de frames et les enregistre.
        """
        try:
            # Choix du format de fichier
            chosen_format, _ = QFileDialog.getSaveFileName(
                self, "Choisissez le format de fichier", "", "PNG Files (*.png);;SVG Files (*.svg)"
            )
            file_format = "svg" if "svg" in chosen_format.lower() else "png"

            # Récupérer le répertoire pour enregistrer les courbes
            save_directory = QFileDialog.getExistingDirectory(self, "Choisissez un dossier pour enregistrer les courbes")
            if not save_directory:
                return

            # Récupérer les paramètres de début et de fin
            params = {}
            for param, bounds in inputs.items():
                if param == "frame_count":
                    continue
                start = float(bounds["start"].text())
                end = float(bounds["end"].text())
                params[param] = {"start": start, "end": end}

            # Récupérer le nombre de frames
            frame_count = int(inputs["frame_count"].text())
            if frame_count <= 0:
                raise ValueError("Le nombre de frames doit être un entier strictement positif.")

            # Calculer les incréments pour chaque paramètre
            increments = {param: (values["end"] - values["start"]) / (frame_count - 1) for param, values in params.items()}

            # Générer les images pour chaque étape
            for frame in range(1, frame_count + 1):
                # Récupérer les paramètres courants
                p = params["p"]["start"] + increments["p"] * (frame - 1)
                q = params["q"]["start"] + increments["q"] * (frame - 1)
                delta = params["delta"]["start"] + increments["delta"] * (frame - 1)

                # Générer la courbe
                t = np.linspace(0, 2 * np.pi, 1000)
                x = np.sin(p * t + delta)
                y = np.sin(q * t)

                # Création de la figure
                fig, ax = plt.subplots(figsize=(6, 6))
                ax.set_aspect('equal')
                ax.plot(x, y, linewidth=2)
                ax.axis("off")

                # Générer un nom de fichier unique avec les paramètres
                filename = f"lissajous2D_p{p:.2f}_q{q:.2f}_delta{delta:.2f}_frame{frame}.{file_format}"
                filepath = os.path.join(save_directory, filename)

                # Enregistrer l'image
                plt.savefig(filepath, dpi=300, format=file_format)
                plt.close(fig)

                # Aperçu de la première courbe
                if frame == 1:
                    buf = BytesIO()
                    plt.savefig(buf, format=file_format)
                    buf.seek(0)
                    img = QImage()
                    img.loadFromData(buf.getvalue())
                    pixmap = QPixmap.fromImage(img)
                    preview_area.setPixmap(pixmap)
                    preview_area.adjustSize()

            print(f"Toutes les courbes ont été enregistrées dans {save_directory}")

        except ValueError as ve:
            print(f"Erreur de validation : {ve}")
        except Exception as e:
            print(f"Erreur lors de la génération : {e}")


    def generate_lissajous_3d_step(self, inputs, preview_area, preview_layout):
        """
        Génère des courbes Lissajous 3D avec un nombre fixe de frames et les enregistre.
        """
        try:
            # Choix du format de fichier
            chosen_format, _ = QFileDialog.getSaveFileName(
                self, "Choisissez le format de fichier", "", "PNG Files (*.png);;SVG Files (*.svg);;PLY Files (*.ply)"
            )
            file_format = "svg" if "svg" in chosen_format.lower() else "png"

            # Récupérer le répertoire pour enregistrer les courbes
            save_directory = QFileDialog.getExistingDirectory(self, "Choisissez un dossier pour enregistrer les courbes")
            if not save_directory:
                return

            # Récupérer les paramètres de début et de fin
            params = {}
            for param, bounds in inputs.items():
                if param == "frame_count":
                    continue
                start = float(bounds["start"].text())
                end = float(bounds["end"].text())
                params[param] = {"start": start, "end": end}

            # Récupérer le nombre de frames
            frame_count = int(inputs["frame_count"].text())
            if frame_count <= 0:
                raise ValueError("Le nombre de frames doit être un entier strictement positif.")

            # Calculer les incréments pour chaque paramètre
            increments = {param: (values["end"] - values["start"]) / (frame_count - 1) for param, values in params.items()}

            # Générer les images pour chaque étape
            for frame in range(1, frame_count + 1):
                # Récupérer les paramètres courants
                p = params["p"]["start"] + increments["p"] * (frame - 1)
                q = params["q"]["start"] + increments["q"] * (frame - 1)
                r = params["r"]["start"] + increments["r"] * (frame - 1)
                delta = params["delta"]["start"] + increments["delta"] * (frame - 1)
                phi = params["phi"]["start"] + increments["phi"] * (frame - 1)

                # Générer la courbe
                t = np.linspace(0, 2 * np.pi, 1000)
                x = np.sin(p * t + delta)
                y = np.sin(q * t + phi)
                z = np.sin(r * t)

                # Création de la figure
                fig = plt.figure(figsize=(6, 6))
                ax = fig.add_subplot(111, projection='3d')
                ax.plot(x, y, z, linewidth=2)
                ax.axis("off")

                # Générer un nom de fichier unique avec les paramètres
                filename = f"lissajous3D_p{p:.2f}_q{q:.2f}_r{r:.2f}_delta{delta:.2f}_phi{phi:.2f}_frame{frame}.{file_format}"
                filepath = os.path.join(save_directory, filename)

                # Enregistrer l'image
                plt.savefig(filepath, dpi=300, format=file_format)
                plt.close(fig)

                # Aperçu de la première courbe
                if frame == 1:
                    buf = BytesIO()
                    plt.savefig(buf, format=file_format)
                    buf.seek(0)
                    img = QImage()
                    img.loadFromData(buf.getvalue())
                    pixmap = QPixmap.fromImage(img)
                    preview_area.setPixmap(pixmap)
                    preview_area.adjustSize()

            print(f"Toutes les courbes ont été enregistrées dans {save_directory}")

        except ValueError as ve:
            print(f"Erreur de validation : {ve}")
        except Exception as e:
            print(f"Erreur lors de la génération : {e}")


    def create_lissajous_3d_step_tab(self):
        """
        Crée un onglet pour générer des courbes Lissajous 3D au pas.
        """
        curve_widget = QWidget()
        main_layout = QVBoxLayout()

        # Titre
        title = QLabel("Génération au pas : Lissajous 3D")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        # Ajouter une note
        note_label = QLabel("Indiquez les valeurs de début et de fin pour chaque paramètre (entiers).\n"
                            "Choisissez également le nombre total de frames.")
        note_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(note_label)

        # Section pour les paramètres
        parameters_layout = QVBoxLayout()
        inputs = {}

        for param in ["p", "q", "r", "delta", "phi"]:
            param_layout = QHBoxLayout()
            label = QLabel(f"{param} (début et fin) :")
            start_input = QLineEdit("0")
            end_input = QLineEdit("10")
            param_layout.addWidget(label)
            param_layout.addWidget(start_input)
            param_layout.addWidget(end_input)
            parameters_layout.addLayout(param_layout)
            inputs[param] = {"start": start_input, "end": end_input}

        # Section pour le nombre de frames
        frame_count_layout = QHBoxLayout()
        frame_count_label = QLabel("Nombre de frames :")
        frame_count_input = QLineEdit("10")
        frame_count_layout.addWidget(frame_count_label)
        frame_count_layout.addWidget(frame_count_input)
        parameters_layout.addLayout(frame_count_layout)
        inputs["frame_count"] = frame_count_input

        main_layout.addLayout(parameters_layout)

        # Prévisualisation
        preview_label = QLabel("Aperçu de la première courbe :")
        preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(preview_label)

        preview_area = QLabel()
        preview_area.setFixedSize(600, 600)
        preview_area.setStyleSheet("background-color: white; border: 1px solid black;")
        main_layout.addWidget(preview_area)

        # Boutons
        button_layout = QHBoxLayout()

        # Bouton pour générer les courbes
        generate_button = QPushButton("Générer")
        generate_button.clicked.connect(lambda: self.generate_lissajous_3d_step(inputs, preview_area, main_layout))
        button_layout.addWidget(generate_button)

        # Bouton pour retourner à l'écran précédent
        back_button = QPushButton("Retour")
        back_button.clicked.connect(lambda: self.close_tab(curve_widget))
        button_layout.addWidget(back_button)

        main_layout.addLayout(button_layout)
        curve_widget.setLayout(main_layout)

        return curve_widget


    def generate_lissajous_3d_step(self, inputs, preview_area, preview_layout):
        """
        Génère des courbes Lissajous 3D avec un nombre fixe de frames et les enregistre.
        """
        try:
            # Choix du format de fichier
            chosen_file, chosen_format = QFileDialog.getSaveFileName(
                self, "Choisissez le format de fichier", "", "PNG Files (*.png);;SVG Files (*.svg);;PLY Files (*.ply)"
            )
            if "svg" in chosen_format.lower():
                file_format = "svg"
            elif "ply" in chosen_format.lower():
                file_format = "ply"
            else:
                file_format = "png"

            # Récupérer le répertoire pour enregistrer les courbes
            save_directory = QFileDialog.getExistingDirectory(self, "Choisissez un dossier pour enregistrer les courbes")
            if not save_directory:
                return

            # Récupérer les paramètres de début et de fin
            params = {}
            for param, bounds in inputs.items():
                if param == "frame_count":
                    continue
                start = float(bounds["start"].text())
                end = float(bounds["end"].text())
                params[param] = {"start": start, "end": end}

            # Récupérer le nombre de frames
            frame_count = int(inputs["frame_count"].text())
            if frame_count <= 0:
                raise ValueError("Le nombre de frames doit être un entier strictement positif.")

            # Calculer les incréments pour chaque paramètre
            increments = {param: (values["end"] - values["start"]) / (frame_count - 1) for param, values in params.items()}

            # Générer les images pour chaque étape
            for frame in range(1, frame_count + 1):
                # Récupérer les paramètres courants
                p = params["p"]["start"] + increments["p"] * (frame - 1)
                q = params["q"]["start"] + increments["q"] * (frame - 1)
                r = params["r"]["start"] + increments["r"] * (frame - 1)
                delta = params["delta"]["start"] + increments["delta"] * (frame - 1)
                phi = params["phi"]["start"] + increments["phi"] * (frame - 1)

                # Générer la courbe
                t = np.linspace(0, 2 * np.pi, 1000)
                x = np.sin(p * t + delta)
                y = np.sin(q * t + phi)
                z = np.sin(r * t)

                # Création de la figure
                fig = plt.figure(figsize=(6, 6))
                ax = fig.add_subplot(111, projection='3d')
                ax.plot(x, y, z, linewidth=2)
                ax.axis("off")

                # Générer un nom de fichier unique avec les paramètres
                filename = (
                    f"lissajous3D_p{p:.2f}_q{q:.2f}_r{r:.2f}_delta{delta:.2f}_phi{phi:.2f}_frame{frame}.{file_format}"
                )
                filepath = os.path.join(save_directory, filename)

                # Enregistrer l'image
                plt.savefig(filepath, dpi=300, format=file_format)
                plt.close(fig)

                # Aperçu de la première courbe
                if frame == 1:
                    buf = BytesIO()
                    plt.savefig(buf, format=file_format)
                    buf.seek(0)
                    img = QImage()
                    img.loadFromData(buf.getvalue())
                    pixmap = QPixmap.fromImage(img)
                    preview_area.setPixmap(pixmap)
                    preview_area.adjustSize()

            print(f"Toutes les courbes ont été enregistrées dans {save_directory}")

        except ValueError as ve:
            print(f"Erreur de validation : {ve}")
        except Exception as e:
            print(f"Erreur lors de la génération : {e}")



    def create_superformule_step_tab(self):
        """
        Crée un onglet pour générer des courbes Superformule avec un nombre fixe de frames.
        """
        curve_widget = QWidget()
        main_layout = QVBoxLayout()

        # Titre
        title = QLabel("Génération au pas : Superformule")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        # Ajouter une note
        note_label = QLabel("Indiquez les valeurs de début et de fin pour chaque paramètre (entiers, non zéro).\n"
                            "Choisissez également le nombre total de frames.")
        note_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(note_label)

        # Section pour les paramètres
        parameters_layout = QVBoxLayout()
        inputs = {}

        for param in ["m", "a", "b", "n1", "n2", "n3"]:
            param_layout = QHBoxLayout()
            label = QLabel(f"{param} (début et fin) :")
            start_input = QLineEdit("1")
            end_input = QLineEdit("10")
            param_layout.addWidget(label)
            param_layout.addWidget(start_input)
            param_layout.addWidget(end_input)
            parameters_layout.addLayout(param_layout)
            inputs[param] = {"start": start_input, "end": end_input}

        # Section pour le nombre de frames
        frame_count_layout = QHBoxLayout()
        frame_count_label = QLabel("Nombre de frames :")
        frame_count_input = QLineEdit("10")
        frame_count_layout.addWidget(frame_count_label)
        frame_count_layout.addWidget(frame_count_input)
        parameters_layout.addLayout(frame_count_layout)
        inputs["frame_count"] = frame_count_input

        main_layout.addLayout(parameters_layout)

        # Prévisualisation
        preview_label = QLabel("Aperçu de la première courbe :")
        preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(preview_label)

        preview_area = QLabel()
        preview_area.setFixedSize(600, 600)
        preview_area.setStyleSheet("background-color: white; border: 1px solid black;")
        main_layout.addWidget(preview_area)

        # Boutons
        button_layout = QHBoxLayout()

        # Bouton pour générer les courbes
        generate_button = QPushButton("Générer")
        generate_button.clicked.connect(lambda: self.generate_superformule_step(inputs, preview_area, main_layout))
        button_layout.addWidget(generate_button)

        # Bouton pour retourner à l'écran précédent
        back_button = QPushButton("Retour")
        back_button.clicked.connect(lambda: self.close_tab(curve_widget))
        button_layout.addWidget(back_button)

        main_layout.addLayout(button_layout)
        curve_widget.setLayout(main_layout)

        return curve_widget




    def generate_superformule_step(self, inputs, preview_area, preview_layout):
        """
        Génère des courbes Superformule avec un nombre fixe de frames et les enregistre.
        """
        try:
            # Choix du format de fichier
            chosen_format, _ = QFileDialog.getSaveFileName(
                self, "Choisissez le format de fichier", "", "PNG Files (*.png);;SVG Files (*.svg)"
            )
            file_format = "svg" if "svg" in chosen_format.lower() else "png"

            # Récupérer le répertoire pour enregistrer les courbes
            save_directory = QFileDialog.getExistingDirectory(self, "Choisissez un dossier pour enregistrer les courbes")
            if not save_directory:
                return

            # Récupérer les paramètres de début et de fin
            params = {}
            for param, bounds in inputs.items():
                if param == "frame_count":
                    continue
                start = float(bounds["start"].text())
                end = float(bounds["end"].text())
                if start == 0 or end == 0:
                    raise ValueError(f"Les valeurs de {param} ne peuvent pas être nulles.")
                params[param] = {"start": start, "end": end}

            # Récupérer le nombre de frames
            frame_count = int(inputs["frame_count"].text())
            if frame_count <= 0:
                raise ValueError("Le nombre de frames doit être un entier strictement positif.")

            # Calculer les incréments pour chaque paramètre
            increments = {param: (values["end"] - values["start"]) / (frame_count - 1) for param, values in params.items()}

            # Générer les images pour chaque étape
            for frame in range(1, frame_count + 1):
                # Récupérer les paramètres courants
                m = params["m"]["start"] + increments["m"] * (frame - 1)
                a = params["a"]["start"] + increments["a"] * (frame - 1)
                b = params["b"]["start"] + increments["b"] * (frame - 1)
                n1 = params["n1"]["start"] + increments["n1"] * (frame - 1)
                n2 = params["n2"]["start"] + increments["n2"] * (frame - 1)
                n3 = params["n3"]["start"] + increments["n3"] * (frame - 1)

                # Générer la superformule
                theta = np.linspace(0, 2 * np.pi, 1000)
                r = (abs(np.cos(m * theta / 4) / a) ** n2 + abs(np.sin(m * theta / 4) / b) ** n3) ** (-1 / n1)
                x = r * np.cos(theta)
                y = r * np.sin(theta)

                # Création de la figure
                fig, ax = plt.subplots(figsize=(6, 6))
                ax.set_aspect('equal')
                ax.plot(x, y, linewidth=2)
                ax.axis("off")

                # Générer un nom de fichier unique avec les paramètres
                filename = (
                    f"superformule_m{m:.2f}_a{a:.2f}_b{b:.2f}_n1{n1:.2f}_n2{n2:.2f}_n3{n3:.2f}_frame{frame}.{file_format}"
                )
                filepath = os.path.join(save_directory, filename)

                # Enregistrer l'image
                plt.savefig(filepath, dpi=300, format=file_format)
                plt.close(fig)

                # Aperçu de la première courbe
                if frame == 1:
                    buf = BytesIO()
                    plt.savefig(buf, format=file_format)
                    buf.seek(0)
                    img = QImage()
                    img.loadFromData(buf.getvalue())
                    pixmap = QPixmap.fromImage(img)
                    preview_area.setPixmap(pixmap)
                    preview_area.adjustSize()

            print(f"Toutes les courbes ont été enregistrées dans {save_directory}")

        except ValueError as ve:
            print(f"Erreur de validation : {ve}")
        except Exception as e:
            print(f"Erreur lors de la génération : {e}")






    def create_clelie_3d_step_tab(self):
        """
        Crée un onglet pour générer des courbes Clélie 3D au pas.
        """
        curve_widget = QWidget()
        main_layout = QVBoxLayout()

        # Titre
        title = QLabel("Génération au pas : Clélie 3D")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        # Ajouter une note
        note_label = QLabel("Indiquez les valeurs de début et de fin pour chaque paramètre (entiers).\n"
                            "Choisissez également le nombre total de frames.")
        note_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(note_label)

        # Section pour les paramètres
        parameters_layout = QVBoxLayout()
        inputs = {}

        for param in ["a", "m", "theta_max", "n_points"]:
            param_layout = QHBoxLayout()
            label = QLabel(f"{param} (début et fin) :")
            start_input = QLineEdit("1")
            end_input = QLineEdit("5")
            param_layout.addWidget(label)
            param_layout.addWidget(start_input)
            param_layout.addWidget(end_input)
            parameters_layout.addLayout(param_layout)
            inputs[param] = {"start": start_input, "end": end_input}

        # Section pour le nombre de frames
        frame_count_layout = QHBoxLayout()
        frame_count_label = QLabel("Nombre de frames :")
        frame_count_input = QLineEdit("10")
        frame_count_layout.addWidget(frame_count_label)
        frame_count_layout.addWidget(frame_count_input)
        parameters_layout.addLayout(frame_count_layout)
        inputs["frame_count"] = frame_count_input

        main_layout.addLayout(parameters_layout)

        # Prévisualisation
        preview_label = QLabel("Aperçu de la première courbe :")
        preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(preview_label)

        preview_area = QLabel()
        preview_area.setFixedSize(600, 600)
        preview_area.setStyleSheet("background-color: white; border: 1px solid black;")
        main_layout.addWidget(preview_area)

        # Boutons
        button_layout = QHBoxLayout()

        # Bouton pour générer les courbes
        generate_button = QPushButton("Générer")
        generate_button.clicked.connect(lambda: self.generate_clelie_3d_step(inputs, preview_area, main_layout))
        button_layout.addWidget(generate_button)

        # Bouton pour retourner à l'écran précédent
        back_button = QPushButton("Retour")
        back_button.clicked.connect(lambda: self.close_tab(curve_widget))
        button_layout.addWidget(back_button)

        main_layout.addLayout(button_layout)
        curve_widget.setLayout(main_layout)

        return curve_widget




    def generate_clelie_3d_step(self, inputs, preview_area, preview_layout):
        """
        Génère des courbes Clélie 3D avec un nombre fixe de frames et les enregistre.
        """
        try:
            # Choix du format de fichier
            chosen_file, chosen_format = QFileDialog.getSaveFileName(
                self, "Choisissez le format de fichier", "", "PNG Files (*.png);;SVG Files (*.svg);;PLY Files (*.ply)"
            )
            if "svg" in chosen_format.lower():
                file_format = "svg"
            elif "ply" in chosen_format.lower():
                file_format = "ply"
            else:
                file_format = "png"

            # Récupérer le répertoire pour enregistrer les courbes
            save_directory = QFileDialog.getExistingDirectory(self, "Choisissez un dossier pour enregistrer les courbes")
            if not save_directory:
                return

            # Récupérer les paramètres de début et de fin
            params = {}
            for param, bounds in inputs.items():
                if param == "frame_count":
                    continue
                start = float(bounds["start"].text())
                end = float(bounds["end"].text())
                params[param] = {"start": start, "end": end}

            # Récupérer le nombre de frames
            frame_count = int(inputs["frame_count"].text())
            if frame_count <= 0:
                raise ValueError("Le nombre de frames doit être un entier strictement positif.")

            # Calculer les incréments pour chaque paramètre
            increments = {param: (values["end"] - values["start"]) / (frame_count - 1) for param, values in params.items()}

            # Générer les images pour chaque étape
            for frame in range(1, frame_count + 1):
                # Récupérer les paramètres courants
                a = params["a"]["start"] + increments["a"] * (frame - 1)
                m = params["m"]["start"] + increments["m"] * (frame - 1)
                theta_max = params["theta max"]["start"] + increments["theta max"] * (frame - 1)
                n_points = int(params["n_points"]["start"] + increments["n_points"] * (frame - 1))

                # Générer la courbe
                theta = np.linspace(0, theta_max, n_points)
                x = a * np.cos(m * theta) * np.sin(theta)
                y = a * np.sin(m * theta) * np.sin(theta)
                z = a * np.cos(theta)

                # Création de la figure
                fig, ax = plt.subplots(figsize=(6, 6))
                ax.set_aspect('equal')
                ax = fig.add_subplot(111, projection='3d')
                ax.plot(x, y, z, linewidth=2)
                ax.axis("off")

                # Enregistrer l'image
                filepath = os.path.join(save_directory, f"frame_{frame}.{file_format}")
                plt.savefig(filepath, dpi=300, format=file_format)
                plt.close(fig)

                # Aperçu de la première courbe
                if frame == 1:
                    buf = BytesIO()
                    fig.savefig(buf, format=file_format)
                    buf.seek(0)
                    img = QImage()
                    img.loadFromData(buf.getvalue())
                    pixmap = QPixmap.fromImage(img)
                    preview_area.setPixmap(pixmap)
                    preview_area.adjustSize()

            print(f"Toutes les courbes ont été enregistrées dans {save_directory}")

        except ValueError as ve:
            print(f"Erreur de validation : {ve}")
        except Exception as e:
            print(f"Erreur lors de la génération : {e}")


    def create_exponentielle_step_tab(self):
        curve_widget = QWidget()
        main_layout = QVBoxLayout()

        # Title
        title = QLabel("Construction de la trajectoire exponentielle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        # Dynamic input fields for 'a' and 'b'
        inputs = {}

        def add_parameter_input(param):
            """Add input fields for a parameter."""
            layout = QHBoxLayout()  # Create a new layout every time to avoid reusing
            label = QLabel(f"{param} :")
            start_input = QLineEdit("1")
            end_input = QLineEdit("5")
            layout.addWidget(label)
            layout.addWidget(start_input)
            layout.addWidget(end_input)
            main_layout.addLayout(layout)

            inputs[param] = {"start": start_input, "end": end_input}

        # Add inputs for dynamic parameters
        for param in ["a1", "b1", "a2", "b2", "a3", "b3"]:  # Correct parameter names
            add_parameter_input(param)

        # Input for number of frames
        frames_layout = QHBoxLayout()
        frames_label = QLabel("Nombre de frames :")
        frames_input = QLineEdit("30")
        frames_layout.addWidget(frames_label)
        frames_layout.addWidget(frames_input)
        main_layout.addLayout(frames_layout)

        # Add a preview button
        preview_button = QPushButton("Prévisualiser")
        preview_button.clicked.connect(lambda: self.preview_exponentielle_step(inputs, frames_input))
        main_layout.addWidget(preview_button)

        # Add a save button
        save_button = QPushButton("Enregistrer")
        save_button.clicked.connect(lambda: self.save_exponentielle_step(inputs, frames_input))
        main_layout.addWidget(save_button)

        # Back button
        back_button = QPushButton("Retour")
        back_button.clicked.connect(lambda: self.close_tab(curve_widget))
        main_layout.addWidget(back_button)

        curve_widget.setLayout(main_layout)
        return curve_widget

    def save_exponentielle_step(self, inputs, frames_input):
        """
        Génère et enregistre une série d'images pour une trajectoire exponentielle.
        """
        try:
            # Demander le répertoire pour enregistrer les images
            save_directory = QFileDialog.getExistingDirectory(self, "Choisissez un dossier pour enregistrer les courbes")
            if not save_directory:
                return

            # Récupérer les paramètres des champs d'entrée
            params = {}
            for param, bounds in inputs.items():
                start = float(bounds["start"].text())
                end = float(bounds["end"].text())
                params[param] = {"start": start, "end": end}

            # Nombre de frames
            frame_count = int(frames_input.text())
            if frame_count <= 0:
                raise ValueError("Le nombre de frames doit être un entier strictement positif.")

            # Calculer les incréments
            increments = {param: (values["end"] - values["start"]) / (frame_count - 1) for param, values in params.items()}

            # Générer les courbes pour chaque frame
            for frame in range(1, frame_count + 1):
                # Récupérer les valeurs actuelles pour a et b
                a_values = [params[f"a{i + 1}"]["start"] + increments[f"a{i + 1}"] * (frame - 1) for i in range(3)]
                b_values = [params[f"b{i + 1}"]["start"] + increments[f"b{i + 1}"] * (frame - 1) for i in range(3)]

                # Générer les points
                t = np.linspace(0, 2 * np.pi, 1000)
                x = sum(a * np.cos(b * t) for a, b in zip(a_values, b_values))
                y = sum(a * np.sin(b * t) for a, b in zip(a_values, b_values))

                # Création de la figure
                fig, ax = plt.subplots(figsize=(6, 6))
                ax.set_aspect('equal')
                ax.plot(x, y, linewidth=2)
                ax.axis("off")

                # Générer un nom de fichier unique avec les paramètres
                filename = (
                    f"exponentielle_a{a_values[0]:.2f}_{a_values[1]:.2f}_{a_values[2]:.2f}_"
                    f"b{b_values[0]:.2f}_{b_values[1]:.2f}_{b_values[2]:.2f}_frame{frame}.png"
                )
                filepath = os.path.join(save_directory, filename)

                # Sauvegarder l'image
                plt.savefig(filepath, dpi=300, format="png")
                plt.close(fig)

            print(f"Toutes les courbes ont été enregistrées dans {save_directory}")

        except ValueError as ve:
            print(f"Erreur de validation : {ve}")
        except Exception as e:
            print(f"Erreur lors de la génération : {e}")



    def generate_exponentielle_step(self, inputs, preview_area, preview_layout):
        """
        Génère des courbes exponentielles avec un nombre fixe de frames et les enregistre.
        """
        try:
            # Choix du format de fichier
            chosen_format, _ = QFileDialog.getSaveFileName(
                self, "Choisissez le format de fichier", "", "PNG Files (*.png);;SVG Files (*.svg)"
            )
            file_format = "svg" if "svg" in chosen_format.lower() else "png"

            # Récupérer le répertoire pour enregistrer les courbes
            save_directory = QFileDialog.getExistingDirectory(self, "Choisissez un dossier pour enregistrer les courbes")
            if not save_directory:
                return

            # Récupérer les paramètres de début et de fin
            params = {}
            for param, bounds in inputs.items():
                if param == "frame_count":
                    continue
                start = float(bounds["start"].text())
                end = float(bounds["end"].text())
                params[param] = {"start": start, "end": end}

            # Récupérer le nombre de frames
            frame_count = int(inputs["frame_count"].text())
            if frame_count <= 0:
                raise ValueError("Le nombre de frames doit être un entier strictement positif.")

            # Calculer les incréments pour chaque paramètre
            increments = {param: (values["end"] - values["start"]) / (frame_count - 1) for param, values in params.items()}

            # Générer les images pour chaque étape
            for frame in range(1, frame_count + 1):
                # Récupérer les paramètres courants
                a_values = [params[f"a{i + 1}"]["start"] + increments[f"a{i + 1}"] * (frame - 1) for i in range(3)]
                b_values = [params[f"b{i + 1}"]["start"] + increments[f"b{i + 1}"] * (frame - 1) for i in range(3)]

                # Générer la courbe
                t = np.linspace(0, 2 * np.pi, 1000)
                x = sum(a * np.cos(b * t) for a, b in zip(a_values, b_values))
                y = sum(a * np.sin(b * t) for a, b in zip(a_values, b_values))

                # Création de la figure
                fig, ax = plt.subplots(figsize=(6, 6))
                ax.set_aspect('equal')
                ax.plot(x, y, linewidth=2)
                ax.axis("off")

                # Enregistrer l'image
                filepath = os.path.join(save_directory, f"frame_{frame}.{file_format}")
                plt.savefig(filepath, dpi=300, format=file_format)
                plt.close(fig)

                # Aperçu de la première courbe
                if frame == 1:
                    buf = BytesIO()
                    fig.savefig(buf, format=file_format)
                    buf.seek(0)
                    img = QImage()
                    img.loadFromData(buf.getvalue())
                    pixmap = QPixmap.fromImage(img)
                    preview_area.setPixmap(pixmap)
                    preview_area.adjustSize()

            print(f"Toutes les courbes ont été enregistrées dans {save_directory}")

        except ValueError as ve:
            print(f"Erreur de validation : {ve}")
        except Exception as e:
            print(f"Erreur lors de la génération : {e}")


    def preview_exponentielle_step(self, inputs, frames_input):
        """
        Prévisualise une courbe exponentielle pour la première frame.
        """
        try:
            # Récupérer les paramètres de début pour chaque paramètre dynamique
            params = {}
            for param, bounds in inputs.items():
                if "start" in bounds:  # Vérifier que la clé "start" existe
                    start = float(bounds["start"].text())
                    params[param] = start

            # Vérification des clés pour a1, a2, a3, b1, b2, b3 et générer les valeurs
            if "a1" not in params or "a2" not in params or "a3" not in params:
                raise ValueError("Les paramètres a1, a2, a3 doivent être définis.")
            if "b1" not in params or "b2" not in params or "b3" not in params:
                raise ValueError("Les paramètres b1, b2, b3 doivent être définis.")

            # Utiliser les paramètres définis
            a_values = [params[f"a{i + 1}"] for i in range(3)]
            b_values = [params[f"b{i + 1}"] for i in range(3)]

            # Calculer la courbe
            t = np.linspace(0, 2 * np.pi, 1000)
            x = sum(a * np.cos(b * t) for a, b in zip(a_values, b_values))
            y = sum(a * np.sin(b * t) for a, b in zip(a_values, b_values))

            # Afficher dans l'interface
            fig, ax = plt.subplots(figsize=(6, 6))
            ax.set_aspect('equal')
            ax.plot(x, y, linewidth=2)
            ax.axis("off")

            # Convertir la figure en image pour l'affichage
            buf = BytesIO()
            plt.savefig(buf, format="png")
            buf.seek(0)
            img = QImage()
            img.loadFromData(buf.getvalue())
            pixmap = QPixmap.fromImage(img)

            # Afficher dans une QLabel ou un espace prévu pour l'aperçu
            preview_area = QLabel()  # Ajoutez ou remplacez par votre zone de prévisualisation
            preview_area.setPixmap(pixmap)
            preview_area.adjustSize()
            plt.close(fig)

        except ValueError as ve:
            print(f"Erreur de validation : {ve}")
        except Exception as e:
            print(f"Erreur lors de la prévisualisation : {e}")



    def create_hypertrochoid_step_tab(self):
        """
        Crée un onglet pour générer des courbes Hypertrochoïdes au pas.
        """
        curve_widget = QWidget()
        main_layout = QVBoxLayout()

        # Titre
        title = QLabel("Génération au pas : Hypertrochoïde")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        # Ajouter une note
        note_label = QLabel("Indiquez les valeurs de début et de fin pour chaque paramètre (entiers).\n"
                            "Choisissez également le nombre total de frames.")
        note_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(note_label)

        # Section pour les paramètres
        parameters_layout = QVBoxLayout()
        inputs = {}

        # Paramètres pour Hypertrochoïde : R, r, d
        for param in ["R", "r", "d"]:
            param_layout = QHBoxLayout()
            label = QLabel(f"{param} (début et fin) :")
            start_input = QLineEdit("1")
            end_input = QLineEdit("5")
            param_layout.addWidget(label)
            param_layout.addWidget(start_input)
            param_layout.addWidget(end_input)
            parameters_layout.addLayout(param_layout)
            inputs[param] = {"start": start_input, "end": end_input}

        # Nombre de frames
        frame_count_layout = QHBoxLayout()
        frame_count_label = QLabel("Nombre de frames :")
        frame_count_input = QLineEdit("10")
        frame_count_layout.addWidget(frame_count_label)
        frame_count_layout.addWidget(frame_count_input)
        parameters_layout.addLayout(frame_count_layout)
        inputs["frame_count"] = frame_count_input

        main_layout.addLayout(parameters_layout)

        # Prévisualisation
        preview_label = QLabel("Aperçu de la première courbe :")
        preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(preview_label)

        preview_area = QLabel()
        preview_area.setFixedSize(600, 600)
        preview_area.setStyleSheet("background-color: white; border: 1px solid black;")
        main_layout.addWidget(preview_area)

        # Boutons
        button_layout = QHBoxLayout()

        # Bouton pour générer les courbes
        generate_button = QPushButton("Générer")
        generate_button.clicked.connect(lambda: self.generate_hypertrochoid_step(inputs, preview_area, main_layout))
        button_layout.addWidget(generate_button)

        # Bouton pour retourner à l'écran précédent
        back_button = QPushButton("Retour")
        back_button.clicked.connect(lambda: self.close_tab(curve_widget))
        button_layout.addWidget(back_button)

        main_layout.addLayout(button_layout)
        curve_widget.setLayout(main_layout)

        return curve_widget


    def generate_hypertrochoid_step(self, inputs, preview_area, preview_layout):
        """
        Génère des courbes Hypertrochoïdes avec un nombre fixe de frames et les enregistre.
        """
        try:
            # Choix du format de fichier
            chosen_format, _ = QFileDialog.getSaveFileName(
                self, "Choisissez le format de fichier", "", "PNG Files (*.png);;SVG Files (*.svg)"
            )
            file_format = "svg" if "svg" in chosen_format.lower() else "png"

            # Récupérer le répertoire pour enregistrer les courbes
            save_directory = QFileDialog.getExistingDirectory(self, "Choisissez un dossier pour enregistrer les courbes")
            if not save_directory:
                return

            # Récupérer les paramètres de début et de fin
            params = {}
            for param, bounds in inputs.items():
                if param == "frame_count":
                    continue
                start = float(bounds["start"].text())
                end = float(bounds["end"].text())
                params[param] = {"start": start, "end": end}

            # Récupérer le nombre de frames
            frame_count = int(inputs["frame_count"].text())
            if frame_count <= 0:
                raise ValueError("Le nombre de frames doit être un entier strictement positif.")

            # Calculer les incréments pour chaque paramètre
            increments = {param: (values["end"] - values["start"]) / (frame_count - 1) for param, values in params.items()}

            # Générer les images pour chaque étape
            for frame in range(1, frame_count + 1):
                # Récupérer les paramètres courants
                current_params = {param: values["start"] + increments[param] * (frame - 1) for param, values in params.items()}
                R, r, d = current_params["R"], current_params["r"], current_params["d"]

                # Générer la courbe Hypertrochoïde
                t = np.linspace(0, 2 * np.pi, 1000)
                x = (R - r) * np.cos(t) + d * np.cos((R - r) / r * t)
                y = (R - r) * np.sin(t) - d * np.sin((R - r) / r * t)

                # Création de la figure
                fig, ax = plt.subplots(figsize=(6, 6))
                ax.plot(x, y, linewidth=2)
                ax.axis("off")
                ax.set_aspect('equal')

                # Générer un nom de fichier unique avec les paramètres
                filename = f"hypertrochoid_R{R:.2f}_r{r:.2f}_d{d:.2f}_frame{frame}.{file_format}"
                filepath = os.path.join(save_directory, filename)

                # Enregistrer l'image
                plt.savefig(filepath, dpi=300, format=file_format)
                plt.close(fig)

                # Aperçu de la première courbe
                if frame == 1:
                    buf = BytesIO()
                    plt.savefig(buf, format=file_format)
                    buf.seek(0)
                    img = QImage()
                    img.loadFromData(buf.getvalue())
                    pixmap = QPixmap.fromImage(img)
                    preview_area.setPixmap(pixmap)
                    preview_area.adjustSize()

            print(f"Toutes les courbes ont été enregistrées dans {save_directory}")

        except ValueError as ve:
            print(f"Erreur de validation : {ve}")
        except Exception as e:
            print(f"Erreur lors de la génération : {e}")





















































# ====================== Explication visuelle ===========================

    def generate_lissajous_2d_construction(self, output_dir, p, q, num_frames, length, line_width=2, point_size=6):
        """
        Generate frames for the Lissajous 2D construction animation.

        Parameters:
            output_dir (str): Directory to save the frames.
            p (float): Frequency for x (can be a float).
            q (float): Frequency for y (can be a float).
            num_frames (int): Number of frames to generate.
            length (float): Length of the curve in multiples of π.
            line_width (int): Width of the lines.
            point_size (int): Size of the moving points.
        """


        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Generate time values
        t = np.linspace(0, length * np.pi, num_frames)
        x_t = np.sin(p * t)
        y_t = np.sin(q * t)

        # Circle settings
        circle_radius = 1
        top_circle_center = (0, 2.5)  # Adjusted to move the circle higher
        left_circle_center = (-2.5, 0)  # Adjusted to move the circle further left

        for i in tqdm(range(num_frames), desc="Generating frames"):
            fig, ax = plt.subplots(figsize=(7, 7))  # Increased figure size for better visibility
            ax.set_facecolor("black")
            ax.set_xlim(-3.7, 1.5)  # Adjusted limits to fit the larger circles
            ax.set_ylim(-1.5, 3.7)
            ax.set_aspect("equal")
            ax.axis("off")

            # Draw the fixed reference circles
            top_circle = Circle(top_circle_center, circle_radius, color="white", fill=False, lw=line_width)
            left_circle = Circle(left_circle_center, circle_radius, color="white", fill=False, lw=line_width)
            ax.add_patch(top_circle)
            ax.add_patch(left_circle)

            # Draw the curve up to the current frame
            ax.plot(x_t[:i + 1], y_t[:i + 1], "-", color="white", linewidth=line_width)

            # Calculate the positions of the moving points on the circles
            top_point_x = top_circle_center[0] + circle_radius * np.sin(p * t[i])
            top_point_y = top_circle_center[1] + circle_radius * np.cos(p * t[i])
            left_point_x = left_circle_center[0] + circle_radius * np.cos(q * t[i])
            left_point_y = left_circle_center[1] + circle_radius * np.sin(q * t[i])

            # Draw the moving points
            ax.plot(top_point_x, top_point_y, "o", color="white", markersize=point_size)  # Top circle moving point
            ax.plot(left_point_x, left_point_y, "o", color="white", markersize=point_size)  # Left circle moving point

            # Draw connecting lines
            ax.plot([x_t[i], x_t[i]], [top_circle_center[1], y_t[i]], linestyle="--", color="white", linewidth=line_width - 0.5)
            ax.plot([left_circle_center[0], x_t[i]], [y_t[i], y_t[i]], linestyle="--", color="white", linewidth=line_width - 0.5)

            # Save the frame
            frame_path = os.path.join(output_dir, f"frame_{i + 1:04d}.png")
            plt.savefig(frame_path, facecolor="black")
            plt.close(fig)

        print(f"Frames saved in: {output_dir}")


    def create_lissajous_2d_construction_tab(self):
            """
            Creates the tab for Lissajous 2D construction, allowing users to input parameters
            and generate animation frames.
            """
            construction_widget = QWidget()
            layout = QVBoxLayout()

            # Title
            title = QLabel("Construction de Lissajous 2D")
            title.setAlignment(Qt.AlignmentFlag.AlignCenter)
            title.setStyleSheet("font-size: 16px; font-weight: bold;")
            layout.addWidget(title)

            # Input fields for parameters
            param_layout = QVBoxLayout()
            inputs = {}
            for param, default in {"p": 1.0, "q": 1.0, "num_frames": 500, "length": 2.0}.items():
                param_label = QLabel(f"{param} :")
                param_input = QLineEdit(str(default))
                param_layout.addWidget(param_label)
                param_layout.addWidget(param_input)
                inputs[param] = param_input

            layout.addLayout(param_layout)

            # Add a button to generate frames
            generate_button = QPushButton("Générer les frames")
            layout.addWidget(generate_button)

            # Back button
            back_button = QPushButton("Retour")
            back_button.clicked.connect(lambda: self.close_tab(construction_widget))
            layout.addWidget(back_button)

            # Function to handle frame generation
            def generate_frames():
                try:
                    p = float(inputs["p"].text())
                    q = float(inputs["q"].text())
                    num_frames = int(inputs["num_frames"].text())
                    length = float(inputs["length"].text())

                    # Ask user for output directory
                    output_dir = QFileDialog.getExistingDirectory(self, "Choisissez un dossier pour enregistrer les frames")
                    if not output_dir:
                        return

                    # Generate the frames
                    self.generate_lissajous_2d_construction(
                        output_dir=output_dir,
                        p=p,
                        q=q,
                        num_frames=num_frames,
                        length=length,
                        line_width=2,
                        point_size=6
                    )

                    QMessageBox.information(self, "Succès", f"Frames enregistrées dans : {output_dir}")
                except Exception as e:
                    QMessageBox.critical(self, "Erreur", f"Erreur lors de la génération : {str(e)}")

            generate_button.clicked.connect(generate_frames)

            construction_widget.setLayout(layout)
            return construction_widget

    def generate_lissajous_3d_construction(self, output_dir, p, q, r, num_frames, length, line_width=2, point_size=6, show_axes=False):
        """
        Generate frames for the Lissajous 3D construction animation.

        Parameters:
            output_dir (str): Directory to save the frames.
            p (float): Frequency for x (can be a float).
            q (float): Frequency for y (can be a float).
            r (float): Frequency for z (can be a float).
            num_frames (int): Number of frames to generate.
            length (float): Length of the curve in multiples of π.
            line_width (int): Width of the lines.
            point_size (int): Size of the moving points.
        """
        import os
        import numpy as np
        import matplotlib.pyplot as plt
        from tqdm import tqdm

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Generate time values
        t = np.linspace(0, length * np.pi, num_frames)
        x_t = np.sin(p * t)
        y_t = np.sin(q * t)
        z_t = np.sin(r * t)

        # Circle settings
        circle_radius = 1
        left_circle_center = (0, -2.5, 0)  # Center of circle parallel to XZ
        top_circle_center = (0, 0, 2.5)   # Center of circle parallel to XY
        front_circle_center = (2.5, 0, 0)  # Center of circle parallel to YZ

        for i in tqdm(range(num_frames), desc="Generating frames"):
            fig = plt.figure(figsize=(10, 10))
            ax = fig.add_subplot(111, projection='3d', facecolor="black")
            ax.set_xlim(-3.5, 3.5)
            ax.set_ylim(-3.5, 3.5)
            ax.set_zlim(-3.5, 3.5)
            ax.set_box_aspect([1, 1, 1])  # Equal aspect ratio for 3D view
            
            if not show_axes:
                ax.axis("off")  # Hide axes if not checked

            # Draw the Lissajous curve up to the current frame
            ax.plot(x_t[:i + 1], y_t[:i + 1], z_t[:i + 1], "-", color="white", linewidth=line_width)

            # Calculate the positions of the moving points on the circles
            left_point_x = left_circle_center[0] + circle_radius * np.cos(r * t[i])
            left_point_z = left_circle_center[2] + circle_radius * np.sin(r * t[i])
            top_point_x = top_circle_center[0] + circle_radius * np.sin(p * t[i])
            top_point_y = top_circle_center[1] + circle_radius * np.cos(p * t[i])
            front_point_y = front_circle_center[1] + circle_radius * np.sin(q * t[i])
            front_point_z = front_circle_center[2] + circle_radius * np.cos(q * t[i])

            # Draw moving points
            ax.scatter(x_t[i], y_t[i], z_t[i], color="white", s=point_size ** 2)  # Current point on the curve
            ax.scatter(left_point_x, left_circle_center[1], left_point_z, color="red", s=point_size ** 2)  # Left circle moving point
            ax.scatter(top_point_x, top_point_y, top_circle_center[2], color="green", s=point_size ** 2)  # Top circle moving point
            ax.scatter(front_circle_center[0], front_point_y, front_point_z, color="blue", s=point_size ** 2)  # Front circle moving point

            # Draw reference circles
            u = np.linspace(0, 2 * np.pi, 100)
            ax.plot(
                left_circle_center[0] + circle_radius * np.cos(u),
                left_circle_center[1] * np.ones_like(u),
                left_circle_center[2] + circle_radius * np.sin(u),
                linestyle="--", color="red", linewidth=line_width - 1
            )  # Left circle (parallel to XZ)
            ax.plot(
                top_circle_center[0] + circle_radius * np.sin(u),
                top_circle_center[1] + circle_radius * np.cos(u),
                top_circle_center[2] * np.ones_like(u),
                linestyle="--", color="green", linewidth=line_width - 1
            )  # Top circle (parallel to XY)
            ax.plot(
                front_circle_center[0] * np.ones_like(u),
                front_circle_center[1] + circle_radius * np.sin(u),
                front_circle_center[2] + circle_radius * np.cos(u),
                linestyle="--", color="blue", linewidth=line_width - 1
            )  # Front circle (parallel to YZ)

            # Draw connecting lines
            ax.plot([x_t[i], left_point_x], [y_t[i], left_circle_center[1]], [z_t[i], left_point_z],
                    linestyle="--", color="white", linewidth=line_width - 0.5)  # Line to left circle
            ax.plot([x_t[i], top_point_x], [y_t[i], top_point_y], [z_t[i], top_circle_center[2]],
                    linestyle="--", color="white", linewidth=line_width - 0.5)  # Line to top circle
            ax.plot([x_t[i], front_circle_center[0]], [y_t[i], front_point_y], [z_t[i], front_point_z],
                    linestyle="--", color="white", linewidth=line_width - 0.5)  # Line to front circle

            # Save the frame
            frame_path = os.path.join(output_dir, f"frame_{i + 1:04d}.png")
            plt.savefig(frame_path, facecolor="black")
            plt.close(fig)

        print(f"Frames saved in: {output_dir}")



    def create_lissajous_3d_construction_tab(self):
        """
        Creates the tab for Lissajous 3D construction, allowing users to input parameters
        and generate animation frames with circles and segments.
        """
        construction_widget = QWidget()
        layout = QVBoxLayout()

        # Title
        title = QLabel("Construction de Lissajous 3D")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)

        # Input fields for parameters
        param_layout = QVBoxLayout()
        inputs = {}
        for param, default in {"p": 1.0, "q": 1.0, "r": 1.0, "num_frames": 500, "length": 2.0}.items():
            param_label = QLabel(f"{param} :")
            param_input = QLineEdit(str(default))
            param_layout.addWidget(param_label)
            param_layout.addWidget(param_input)
            inputs[param] = param_input

        layout.addLayout(param_layout)

        # Add a button to generate frames
        generate_button = QPushButton("Générer les frames")
        layout.addWidget(generate_button)

        # Back button
        back_button = QPushButton("Retour")
        back_button.clicked.connect(lambda: self.close_tab(construction_widget))
        layout.addWidget(back_button)

        # Checkbox for axes visibility
        axes_checkbox = QCheckBox("Afficher les axes")
        axes_checkbox.setChecked(False)  # Default: no axes
        layout.addWidget(axes_checkbox)


        # Function to handle frame generation
        def generate_frames():
            try:
                # Retrieve parameters from user inputs
                p = float(inputs["p"].text())
                q = float(inputs["q"].text())
                r = float(inputs["r"].text())
                num_frames = int(inputs["num_frames"].text())
                length = float(inputs["length"].text())

                # Ask user for output directory
                output_dir = QFileDialog.getExistingDirectory(self, "Choisissez un dossier pour enregistrer les frames")
                if not output_dir:
                    return

                # Generate the frames
                show_axes = axes_checkbox.isChecked()  # Get checkbox value

                self.generate_lissajous_3d_construction(
                    output_dir=output_dir,
                    p=p,
                    q=q,
                    r=r,
                    num_frames=num_frames,
                    length=length,
                    line_width=2,
                    point_size=6,
                    show_axes=show_axes
                )

                QMessageBox.information(self, "Succès", f"Frames enregistrées dans : {output_dir}")
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Erreur lors de la génération : {str(e)}")

        generate_button.clicked.connect(generate_frames)

        construction_widget.setLayout(layout)
        return construction_widget





    




# ====================== FIN Explication visuelle ===========================



    def create_lissajous_2d_tab(self):
        curve_widget = QWidget()
        main_layout = QHBoxLayout()  # Horizontal layout for parameters and preview

        # Parameters section (left)
        param_layout = QVBoxLayout()
        param_label = QLabel("Paramètres pour Lissajous 2D")
        param_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        param_layout.addWidget(param_label)

        inputs = {}
        for param, default in {
            "A": 1, "B": 1, "p": 1, "q": 1, "delta": 0, 
            "longueur": 2 * np.pi,"nombre de points": 1000, "couleur": "blue", "fond": "white", "épaisseur": 2
        }.items():
            label = QLabel(f"{param}:")
            input_field = QLineEdit(str(default))
            param_layout.addWidget(label)
            param_layout.addWidget(input_field)
            inputs[param] = input_field

        # Buttons for updating preview and saving
        button_layout = QHBoxLayout()

        def update_preview():
            try:
                # Fetch parameters
                A = float(inputs["A"].text())
                B = float(inputs["B"].text())
                p = float(inputs["p"].text())
                q = float(inputs["q"].text())
                delta = float(inputs["delta"].text())
                longueur = float(inputs["longueur"].text())
                couleur = inputs["couleur"].text()
                fond = inputs["fond"].text()
                epaisseur = float(inputs["épaisseur"].text())
                nombre_de_point = int(inputs["nombre de points"].text())

                # Generate Lissajous curve
                t = np.linspace(0, longueur, nombre_de_point)
                x = A * np.sin(p * t + delta)
                y = B * np.sin(q * t)

                # Plot
                fig, ax = plt.subplots(figsize=(6, 6))
                ax.set_aspect('equal')
                ax.plot(x, y, color=couleur, linewidth=epaisseur)
                ax.set_facecolor(fond)
                ax.axis('off')

                # Convert to image for preview
                buf = BytesIO()
                plt.savefig(buf, format='png', dpi=100, facecolor=fond)
                buf.seek(0)
                img = QImage()
                img.loadFromData(buf.getvalue())
                pixmap = QPixmap.fromImage(img)
                preview_area.setPixmap(pixmap)
                preview_area.adjustSize()
                plt.close(fig)
            except Exception as e:
                print(f"Error updating preview: {e}")

        update_button = QPushButton("Mettre à jour l'aperçu")
        update_button.clicked.connect(update_preview)
        button_layout.addWidget(update_button)

        def save_curve():
            try:
                


                # Generate Lissajous curve
                A = float(inputs["A"].text())
                B = float(inputs["B"].text())
                p = float(inputs["p"].text())
                q = float(inputs["q"].text())
                delta = float(inputs["delta"].text())
                longueur = float(inputs["longueur"].text())
                couleur = inputs["couleur"].text()
                fond = inputs["fond"].text()
                epaisseur = float(inputs["épaisseur"].text())
                nombre_de_point = int(inputs["nombre de points"].text())

                default_name = f"Lissajous2D_A{A}_B{B}_p{p}_q{q}_delta{delta}_longueur{longueur}_points{nombre_de_point}.svg"

                file_types = "PNG Files (*.png);;SVG Files (*.svg);;PLY Files (*.ply)"
                file_name, _ = QFileDialog.getSaveFileName(self, "Enregistrer la courbe", default_name, file_types)
                if not file_name:
                    return

                t = np.linspace(0, longueur, nombre_de_point)
                x = A * np.sin(p * t + delta)
                y = B * np.sin(q * t)

                fig, ax = plt.subplots(figsize=(6, 6))
                ax.set_aspect('equal')
                ax.plot(x, y, color=couleur, linewidth=epaisseur)
                ax.set_facecolor(fond)
                ax.axis('off')
                format = file_name.split('.')[-1].lower()

                # Save plot
                plt.savefig(file_name, facecolor=fond,format = format)
                plt.close(fig)
                print(f"Courbe enregistrée sous {file_name}")
            except Exception as e:
                print(f"Error saving curve: {e}")

        save_button = QPushButton("Enregistrer")
        save_button.clicked.connect(save_curve)
        button_layout.addWidget(save_button)
        
        def close_tab():
            current_index = self.tab_widget.indexOf(curve_widget)
            if current_index != -1:
                self.tab_widget.removeTab(current_index)
                del self.curve_tabs["Lissajous 2D"]

        back_button = QPushButton("Retour")
        back_button.clicked.connect(close_tab)
        button_layout.addWidget(back_button)
        param_layout.addLayout(button_layout)

        # Preview section (right)
        preview_layout = QVBoxLayout()
        preview_label = QLabel("Aperçu de la courbe :")
        preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        preview_layout.addWidget(preview_label)

        preview_area = QLabel()
        preview_area.setFixedSize(600, 600)
        preview_area.setStyleSheet("background-color: white; border: 1px solid black;")
        preview_layout.addWidget(preview_area)

        # Combine sections in the main layout
        main_layout.addLayout(param_layout)
        main_layout.addLayout(preview_layout)
        curve_widget.setLayout(main_layout)

        return curve_widget
    
    def create_lissajous_3d_tab(self):
        curve_widget = QWidget()
        main_layout = QHBoxLayout()

        # Parameters section (left)
        param_layout = QVBoxLayout()
        param_label = QLabel("Paramètres pour Lissajous 3D")
        param_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        param_layout.addWidget(param_label)

        inputs = {}
        for param, default in {
            "A": 1, "B": 1, "C": 1, "p": 1, "q": 1, "r": 1,
            "delta": 0, "phi": 0, "longueur": 2 * np.pi, "nombre de points": 1000,
            "couleur": "blue", "fond": "white", "épaisseur": 2
        }.items():
            label = QLabel(f"{param}:")
            input_field = QLineEdit(str(default))
            param_layout.addWidget(label)
            param_layout.addWidget(input_field)
            inputs[param] = input_field

        # Buttons for updating preview and saving
        button_layout = QHBoxLayout()

        def update_preview():
            try:
                # Fetch parameters
                A, B, C = float(inputs["A"].text()), float(inputs["B"].text()), float(inputs["C"].text())
                p, q, r = float(inputs["p"].text()), float(inputs["q"].text()), float(inputs["r"].text())
                delta, phi, longueur = float(inputs["delta"].text()), float(inputs["phi"].text()), float(inputs["longueur"].text())
                couleur, fond, epaisseur = inputs["couleur"].text(), inputs["fond"].text(), float(inputs["épaisseur"].text())
                nombre_de_point = int(inputs["nombre de points"].text())

                # Generate Lissajous 3D curve
                t = np.linspace(0, longueur, nombre_de_point)
                x = A * np.sin(p * t + delta)
                y = B * np.sin(q * t)
                z = C * np.sin(r * t + phi)

                fig = plt.figure(figsize=(6, 6))
                ax = fig.add_subplot(111, projection='3d')
                ax.plot(x, y, z, color=couleur, linewidth=epaisseur)
                ax.set_facecolor(fond)
                ax.axis('off')

                # Convert to image for preview
                buf = BytesIO()
                plt.savefig(buf, format='png', dpi=100, facecolor=fond)
                buf.seek(0)
                img = QImage()
                img.loadFromData(buf.getvalue())
                pixmap = QPixmap.fromImage(img)
                preview_area.setPixmap(pixmap)
                preview_area.adjustSize()
                plt.close(fig)
            except Exception as e:
                print(f"Error updating preview: {e}")

        update_button = QPushButton("Mettre à jour l'aperçu")
        update_button.clicked.connect(update_preview)
        button_layout.addWidget(update_button)

        def save_curve():
            try:


                # Fetch parameters
                A, B, C = float(inputs["A"].text()), float(inputs["B"].text()), float(inputs["C"].text())
                p, q, r = float(inputs["p"].text()), float(inputs["q"].text()), float(inputs["r"].text())
                delta, phi, longueur = float(inputs["delta"].text()), float(inputs["phi"].text()), float(inputs["longueur"].text())
                couleur, fond, epaisseur = inputs["couleur"].text(), inputs["fond"].text(), float(inputs["épaisseur"].text())
                nombre_de_point = int(inputs["nombre de points"].text())

                # Generate Lissajous 3D curve
                t = np.linspace(0, longueur, nombre_de_point)
                x = A * np.sin(p * t + delta)
                y = B * np.sin(q * t)
                z = C * np.sin(r * t + phi)

                fig = plt.figure(figsize=(6, 6))
                ax = fig.add_subplot(111, projection='3d')
                ax.set_aspect('equal')
                ax.plot(x, y, z, color=couleur, linewidth=epaisseur)
                ax.set_facecolor(fond)
                ax.axis('off')

                default_name = f"Lissajous3D_A{A}_B{B}_C{C}_p{p}_q{q}_r{r}_delta{delta}_phi{phi}_longueur{longueur}_nombre_de_point{nombre_de_point}.svg"
                file_types = "PNG Files (*.png);;SVG Files (*.svg);;PLY Files (*.ply)"
                file_name, _ = QFileDialog.getSaveFileName(self, "Enregistrer la courbe", default_name, file_types)
                if not file_name:
                    return
                # Save plot
                format = file_name.split('.')[-1].lower()
                plt.savefig(file_name, facecolor=fond, format = format)
                plt.close(fig)
                print(f"Courbe enregistrée sous {file_name}")
            except Exception as e:
                print(f"Error saving curve: {e}")

        save_button = QPushButton("Enregistrer")
        save_button.clicked.connect(save_curve)
        button_layout.addWidget(save_button)
        
        def close_tab():
            current_index = self.tab_widget.indexOf(curve_widget)
            if current_index != -1:
                self.tab_widget.removeTab(current_index)
                del self.curve_tabs["Lissajous 3D"]

        back_button = QPushButton("Retour")
        back_button.clicked.connect(close_tab)
        button_layout.addWidget(back_button)

        param_layout.addLayout(button_layout)

        # Preview section (right)
        preview_layout = QVBoxLayout()
        preview_label = QLabel("Aperçu de la courbe :")
        preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        preview_layout.addWidget(preview_label)

        preview_area = QLabel()
        preview_area.setFixedSize(600, 600)
        preview_area.setStyleSheet("background-color: white; border: 1px solid black;")
        preview_layout.addWidget(preview_area)

        # Combine sections in the main layout
        main_layout.addLayout(param_layout)
        main_layout.addLayout(preview_layout)
        curve_widget.setLayout(main_layout)

        return curve_widget
    
    def create_superformula_tab(self):
        curve_widget = QWidget()
        main_layout = QHBoxLayout()  # Horizontal layout for parameters and preview

        # Parameters section (left)
        param_layout = QVBoxLayout()
        param_label = QLabel("Paramètres pour Superformule")
        param_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        param_layout.addWidget(param_label)

        inputs = {}
        for param, default in {
            "m": 5, "a": 1, "b": 1,
            "n1": 2, "n2": 2, "n3": 2,
            "couleur": "blue", "fond": "white", "épaisseur": 2, "longueur": 2 * np.pi, "nombre de points": 1000,
        }.items():
            label = QLabel(f"{param}:")
            input_field = QLineEdit(str(default))
            param_layout.addWidget(label)
            param_layout.addWidget(input_field)
            inputs[param] = input_field

        # Buttons for updating preview and saving
        button_layout = QHBoxLayout()

        def update_preview():
            try:
                # Fetch parameters
                m = float(inputs["m"].text())
                a = float(inputs["a"].text())
                b = float(inputs["b"].text())
                n1 = float(inputs["n1"].text())
                n2 = float(inputs["n2"].text())
                n3 = float(inputs["n3"].text())
                couleur = inputs["couleur"].text()
                fond = inputs["fond"].text()
                epaisseur = float(inputs["épaisseur"].text())
                longueur = float(inputs["longueur"].text())
                nombre_de_point = int(inputs["nombre de points"].text())

                # Generate Superformula curve
                theta = np.linspace(0, longueur, nombre_de_point)
                r = (abs(np.cos(m * theta / 4) / a) ** n2 + abs(np.sin(m * theta / 4) / b) ** n3) ** (-1 / n1)
                x = r * np.cos(theta)
                y = r * np.sin(theta)

                # Plot
                fig, ax = plt.subplots(figsize=(6, 6))
                ax.plot(x, y, color=couleur, linewidth=epaisseur)
                ax.set_facecolor(fond)
                ax.axis('off')

                # Convert to image for preview
                buf = BytesIO()
                plt.savefig(buf, format='png', dpi=100, facecolor=fond)
                buf.seek(0)
                img = QImage()
                img.loadFromData(buf.getvalue())
                pixmap = QPixmap.fromImage(img)
                preview_area.setPixmap(pixmap)
                preview_area.adjustSize()
                plt.close(fig)
            except Exception as e:
                print(f"Error updating preview: {e}")

        update_button = QPushButton("Mettre à jour l'aperçu")
        update_button.clicked.connect(update_preview)
        button_layout.addWidget(update_button)

        def save_curve():
            try:

                # Fetch parameters
                m = float(inputs["m"].text())
                a = float(inputs["a"].text())
                b = float(inputs["b"].text())
                n1 = float(inputs["n1"].text())
                n2 = float(inputs["n2"].text())
                n3 = float(inputs["n3"].text())
                couleur = inputs["couleur"].text()
                fond = inputs["fond"].text()
                epaisseur = float(inputs["épaisseur"].text())
                longueur = float(inputs["longueur"].text())
                nombre_de_point = int(inputs["nombre de points"].text())

                default_name = f"Superformule_m{m}_a{a}_b{b}_n1{n1}_n2{n2}_n3{n3}_{longueur:.2f}_points{nombre_de_point}.svg"

                file_types = "PNG Files (*.png);;SVG Files (*.svg);;PLY Files (*.ply)"
                file_name, _ = QFileDialog.getSaveFileName(self, "Enregistrer la courbe", default_name, file_types)
                if not file_name:
                    return

                # Generate Superformula curve
                theta = np.linspace(0, longueur, nombre_de_point)
                r = (abs(np.cos(m * theta / 4) / a) ** n2 + abs(np.sin(m * theta / 4) / b) ** n3) ** (-1 / n1)
                x = r * np.cos(theta)
                y = r * np.sin(theta)

                # Plot and save
                fig, ax = plt.subplots(figsize=(6, 6))
                ax.plot(x, y, color=couleur, linewidth=epaisseur)
                ax.set_facecolor(fond)
                ax.axis('off')

                # Save plot
                format = file_name.split('.')[-1].lower()
                plt.savefig(file_name, facecolor=fond, format = format)
                plt.close(fig)
                print(f"Courbe enregistrée sous {file_name}")
            except Exception as e:
                print(f"Error saving curve: {e}")

        save_button = QPushButton("Enregistrer")
        save_button.clicked.connect(save_curve)
        button_layout.addWidget(save_button)

        def close_tab():
            current_index = self.tab_widget.indexOf(curve_widget)
            if current_index != -1:
                self.tab_widget.removeTab(current_index)
                del self.curve_tabs["Superformule"]

        back_button = QPushButton("Retour")
        back_button.clicked.connect(close_tab)
        button_layout.addWidget(back_button)

        param_layout.addLayout(button_layout)

        # Preview section (right)
        preview_layout = QVBoxLayout()
        preview_label = QLabel("Aperçu de la courbe :")
        preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        preview_layout.addWidget(preview_label)

        preview_area = QLabel()
        preview_area.setFixedSize(600, 600)
        preview_area.setStyleSheet("background-color: white; border: 1px solid black;")
        preview_layout.addWidget(preview_area)

        # Combine sections in the main layout
        main_layout.addLayout(param_layout)
        main_layout.addLayout(preview_layout)
        curve_widget.setLayout(main_layout)

        return curve_widget
    
    def create_clelie_3d_tab(self):
        curve_widget = QWidget()
        main_layout = QHBoxLayout()  # Horizontal layout for parameters and preview

        # Parameters section (left)
        param_layout = QVBoxLayout()
        param_label = QLabel("Paramètres pour Clélie 3D")
        param_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        param_layout.addWidget(param_label)

        inputs = {}
        for param, default in {
            "a": 1, "m": 1, "theta max": 2*np.pi, "nombre de points": 1000,
            "couleur": "blue", "fond": "white", "épaisseur": 2
        }.items():
            label = QLabel(f"{param}:")
            input_field = QLineEdit(str(default))
            param_layout.addWidget(label)
            param_layout.addWidget(input_field)
            inputs[param] = input_field

        # Buttons for updating preview, saving, and returning
        button_layout = QHBoxLayout()

        def update_preview():
            try:
                # Fetch parameters
                a = float(inputs["a"].text())
                m = float(inputs["m"].text())
                theta_max = float(inputs["theta max"].text())
                couleur = inputs["couleur"].text()
                fond = inputs["fond"].text()
                epaisseur = float(inputs["épaisseur"].text())
                nombre_de_point = int(inputs["nombre de points"].text())

                # Generate Clélie 3D curve
                theta = np.linspace(0, theta_max, nombre_de_point)
                x = a * np.cos(m * theta) * np.sin(theta)
                y = a * np.sin(m * theta) * np.sin(theta)
                z = a * np.cos(theta)

                fig = plt.figure(figsize=(6, 6))
                ax = fig.add_subplot(111, projection='3d')
                ax.plot(x, y, z, color=couleur, linewidth=epaisseur)
                ax.set_facecolor(fond)
                ax.axis('off')

                # Convert to image for preview
                buf = BytesIO()
                plt.savefig(buf, format='svg', dpi=100, facecolor=fond)
                buf.seek(0)
                img = QImage()
                img.loadFromData(buf.getvalue())
                pixmap = QPixmap.fromImage(img)
                preview_area.setPixmap(pixmap)
                preview_area.adjustSize()
                plt.close(fig)
            except Exception as e:
                print(f"Error updating preview: {e}")

        update_button = QPushButton("Mettre à jour l'aperçu")
        update_button.clicked.connect(update_preview)
        button_layout.addWidget(update_button)

        def save_curve():
            try:
                file_types = "PNG Files (*.png);;SVG Files (*.svg);;PLY Files (*.ply)"
                file_name, _ = QFileDialog.getSaveFileName(self, "Enregistrer la courbe", "", file_types)
                if not file_name:
                    return

                # Fetch parameters
                a = float(inputs["a"].text())
                m = float(inputs["m"].text())
                theta_max = float(inputs["theta max"].text())
                couleur = inputs["couleur"].text()
                fond = inputs["fond"].text()
                epaisseur = float(inputs["épaisseur"].text())
                nombre_de_point = int(inputs["nombre de points"].text())

                default_name = f"Clelie3D_a{a}_m{m}_theta_max{theta_max}_points{nombre_de_point}.svg"

                file_types = "PNG Files (*.png);;SVG Files (*.svg);;PLY Files (*.ply)"
                file_name, _ = QFileDialog.getSaveFileName(self, "Enregistrer la courbe", default_name, file_types)
                if not file_name:
                    return

                # Generate Clélie 3D curve
                theta = np.linspace(0, theta_max, nombre_de_point)
                x = a * np.cos(m * theta) * np.sin(theta)
                y = a * np.sin(m * theta) * np.sin(theta)
                z = a * np.cos(theta)

                fig = plt.figure(figsize=(6, 6))
                ax = fig.add_subplot(111, projection='3d')
                ax.plot(x, y, z, color=couleur, linewidth=epaisseur)
                ax.set_facecolor(fond)
                ax.axis('off')

                format = file_name.split('.')[-1].lower()

                # Save plot
                plt.savefig(file_name, facecolor=fond, format = format)
                plt.close(fig)
                print(f"Courbe enregistrée sous {file_name}")
            except Exception as e:
                print(f"Error saving curve: {e}")

        save_button = QPushButton("Enregistrer")
        save_button.clicked.connect(save_curve)
        button_layout.addWidget(save_button)

        def close_tab():
            current_index = self.tab_widget.indexOf(curve_widget)
            if current_index != -1:
                self.tab_widget.removeTab(current_index)
                del self.curve_tabs["Clelie 3D"]

        back_button = QPushButton("Retour")
        back_button.clicked.connect(close_tab)
        button_layout.addWidget(back_button)

        param_layout.addLayout(button_layout)

        # Preview section (right)
        preview_layout = QVBoxLayout()
        preview_label = QLabel("Aperçu de la courbe :")
        preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        preview_layout.addWidget(preview_label)

        preview_area = QLabel()
        preview_area.setFixedSize(600, 600)
        preview_area.setStyleSheet("background-color: white; border: 1px solid black;")
        preview_layout.addWidget(preview_area)

        # Combine sections in the main layout
        main_layout.addLayout(param_layout)
        main_layout.addLayout(preview_layout)
        curve_widget.setLayout(main_layout)

        return curve_widget
    
    def create_exponentielle_tab(self):
        curve_widget = QWidget()
        main_layout = QHBoxLayout()  # Horizontal layout for parameters and preview

        # Scrollable area for parameters
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)

        # Parameters section (left)
        param_label = QLabel("Paramètres pour Trajectoire Exponentielle")
        param_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        scroll_layout.addWidget(param_label)

        # Input for number of terms (n)
        scroll_layout.addWidget(QLabel('Nombre de termes (n):'))
        n_input = QSpinBox()
        n_input.setMinimum(1)
        n_input.setValue(3)
        scroll_layout.addWidget(n_input)

        # Dynamic input fields for 'a' and 'b'
        a_inputs = []
        b_inputs = []
        a_labels = []
        b_labels = []

        def update_parameters_inputs():
            # Clear existing inputs and labels
            for widget in a_labels + a_inputs + b_labels + b_inputs:
                scroll_layout.removeWidget(widget)
                widget.deleteLater()

            a_labels.clear()
            b_labels.clear()
            a_inputs.clear()
            b_inputs.clear()

            # Add new inputs and labels based on n
            n = n_input.value()
            for i in range(n):
                a_label = QLabel(f"Longueur de la barre a_{i+1}:")
                a_input = QLineEdit("1")
                scroll_layout.addWidget(a_label)
                scroll_layout.addWidget(a_input)
                a_labels.append(a_label)
                a_inputs.append(a_input)

                b_label = QLabel(f"Vitesse de rotation b_{i+1}:")
                b_input = QLineEdit("1")
                scroll_layout.addWidget(b_label)
                scroll_layout.addWidget(b_input)
                b_labels.append(b_label)
                b_inputs.append(b_input)

        n_input.valueChanged.connect(update_parameters_inputs)
        update_parameters_inputs()

        # Input fields for other parameters
        scroll_layout.addWidget(QLabel('Theta max:'))
        theta_max_input = QLineEdit("2")
        scroll_layout.addWidget(theta_max_input)

        scroll_layout.addWidget(QLabel('Nombre de points:'))
        num_points_input = QLineEdit("5000")
        scroll_layout.addWidget(num_points_input)

        scroll_layout.addWidget(QLabel('Couleur de la courbe:'))
        color_input = QLineEdit("blue")
        scroll_layout.addWidget(color_input)

        scroll_layout.addWidget(QLabel('Couleur du fond:'))
        background_input = QLineEdit("white")
        scroll_layout.addWidget(background_input)

        scroll_layout.addWidget(QLabel('Épaisseur de la courbe:'))
        line_width_input = QLineEdit("2")
        scroll_layout.addWidget(line_width_input)

        # Place the scrollable widget in the scroll area
        scroll_area.setWidget(scroll_widget)
        main_layout.addWidget(scroll_area)

        # Preview and save buttons
        preview_layout = QVBoxLayout()
        preview_label = QLabel("Aperçu de la courbe :")
        preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        preview_layout.addWidget(preview_label)

        preview_area = QLabel()
        preview_area.setFixedSize(600, 600)
        preview_area.setStyleSheet("background-color: white; border: 1px solid black;")
        preview_layout.addWidget(preview_area)

        main_layout.addLayout(preview_layout)

        # Buttons
        button_layout = QHBoxLayout()

        def update_preview():
            try:
                
                n = n_input.value()
                a = [float(a_input.text()) for a_input in a_inputs]
                b = [float(b_input.text()) for b_input in b_inputs]
                theta_max = float(theta_max_input.text()) * np.pi
                num_points = int(num_points_input.text())
                color = color_input.text()
                background = background_input.text()
                line_width = float(line_width_input.text())

                fig = self.plot_trajectory(n, a, b, (0, theta_max), color, background, line_width, num_points)

                buf = BytesIO()
                fig.savefig(buf, format='png', facecolor=background)
                plt.close(fig)

                buf.seek(0)
                img = QImage()
                img.loadFromData(buf.getvalue())
                pixmap = QPixmap.fromImage(img)
                preview_area.setPixmap(pixmap)
                preview_area.adjustSize()
            except Exception as e:
                print(f"Error updating preview: {e}")

        update_button = QPushButton("Mettre à jour l'aperçu")
        update_button.clicked.connect(update_preview)
        button_layout.addWidget(update_button)

        def save_curve():
            try:
                n = n_input.value()
                a = [float(a_input.text()) for a_input in a_inputs]
                b = [float(b_input.text()) for b_input in b_inputs]
                theta_max = float(theta_max_input.text()) * np.pi
                num_points = int(num_points_input.text())
                color = color_input.text()
                background = background_input.text()
                line_width = float(line_width_input.text())

                default_name = f"Exponentielle_n{n}_theta{theta_max:.2f}.svg"

                file_types = "PNG Files (*.png);;SVG Files (*.svg);;PLY Files (*.ply)"
                file_name, _ = QFileDialog.getSaveFileName(self, "Enregistrer la courbe", default_name, file_types)
                if not file_name:
                    return

                fig = self.plot_trajectory(n, a, b, (0, theta_max), color, background, line_width, num_points)
                format = file_name.split('.')[-1].lower()
                fig.savefig(file_name, format=format, facecolor=background)
                plt.close(fig)
                print(f"Courbe enregistrée sous {file_name}")
            except Exception as e:
                print(f"Error saving curve: {e}")

        save_button = QPushButton("Enregistrer")
        save_button.clicked.connect(save_curve)
        button_layout.addWidget(save_button)

        def close_tab():
            current_index = self.tab_widget.indexOf(curve_widget)
            if current_index != -1:
                self.tab_widget.removeTab(current_index)
                del self.curve_tabs["Exponentielle"]

        back_button = QPushButton("Retour")
        back_button.clicked.connect(close_tab)
        button_layout.addWidget(back_button)

        preview_layout.addLayout(button_layout)
        curve_widget.setLayout(main_layout)

        return curve_widget

    def create_hypertrochoid_tab(self):
        curve_widget = QWidget()
        main_layout = QHBoxLayout()  # Horizontal layout for parameters and preview

        # Scrollable area for parameters
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)

        # Parameters section (left)
        param_label = QLabel("Paramètres pour Hypertrochoïde")
        param_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        scroll_layout.addWidget(param_label)

        # Input fields for parameters
        scroll_layout.addWidget(QLabel('Rayon principal (R):'))
        R_input = QLineEdit("5")
        scroll_layout.addWidget(R_input)

        scroll_layout.addWidget(QLabel('Rayon secondaire (r):'))
        r_input = QLineEdit("3")
        scroll_layout.addWidget(r_input)

        scroll_layout.addWidget(QLabel('Distance (d):'))
        d_input = QLineEdit("5")
        scroll_layout.addWidget(d_input)

        scroll_layout.addWidget(QLabel('Nombre de points:'))
        num_points_input = QLineEdit("1000")
        scroll_layout.addWidget(num_points_input)

        scroll_layout.addWidget(QLabel('Couleur de la courbe:'))
        color_input = QLineEdit("blue")
        scroll_layout.addWidget(color_input)

        scroll_layout.addWidget(QLabel('Couleur du fond:'))
        background_input = QLineEdit("white")
        scroll_layout.addWidget(background_input)

        scroll_layout.addWidget(QLabel('Épaisseur de la courbe:'))
        line_width_input = QLineEdit("2")
        scroll_layout.addWidget(line_width_input)

        scroll_layout.addWidget(QLabel('Longueur de la courbe:'))
        longueur_input = QLineEdit("6.28")
        scroll_layout.addWidget(longueur_input)

        # Place the scrollable widget in the scroll area
        scroll_area.setWidget(scroll_widget)
        main_layout.addWidget(scroll_area)

        # Preview and save buttons
        preview_layout = QVBoxLayout()
        preview_label = QLabel("Aperçu de la courbe :")
        preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        preview_layout.addWidget(preview_label)

        preview_area = QLabel()
        preview_area.setFixedSize(600, 600)
        preview_area.setStyleSheet("background-color: white; border: 1px solid black;")
        preview_layout.addWidget(preview_area)

        main_layout.addLayout(preview_layout)

        # Buttons
        button_layout = QHBoxLayout()

        def plot_hypertrochoid(R, r, d,longueur, num_points, color, background, line_width):
            t = np.linspace(0, longueur, num_points)
            x = (R - r) * np.cos(t) + d * np.cos((R - r) / r / t)
            y = (R - r) * np.sin(t) - d * np.sin((R - r) / r * t)

            fig, ax = plt.subplots(figsize = (6,6))
            ax.plot(x, y, color=color, linewidth=line_width)
            ax.set_facecolor(background)
            ax.axis('off')

            return fig

        def update_preview():
            try:
                R = float(R_input.text())
                r = float(r_input.text())
                d = float(d_input.text())
                num_points = int(num_points_input.text())
                color = color_input.text()
                background = background_input.text()
                line_width = float(line_width_input.text())
                longueur = float(longueur_input.text())

                fig = plot_hypertrochoid(R, r, d,longueur, num_points, color, background, line_width)

                buf = BytesIO()
                fig.savefig(buf, format='png', facecolor=background)
                plt.close(fig)

                buf.seek(0)
                img = QImage()
                img.loadFromData(buf.getvalue())
                pixmap = QPixmap.fromImage(img)
                preview_area.setPixmap(pixmap)
                preview_area.adjustSize()
            except Exception as e:
                print(f"Error updating preview: {e}")

        update_button = QPushButton("Mettre à jour l'aperçu")
        update_button.clicked.connect(update_preview)
        button_layout.addWidget(update_button)

        def save_curve():
            try:
                R = float(R_input.text())
                r = float(r_input.text())
                d = float(d_input.text())
                num_points = int(num_points_input.text())
                longueur = float(longueur_input.text())
                color = color_input.text()
                background = background_input.text()
                line_width = float(line_width_input.text())

                default_name = f"Hypertrochoide_R{R}_r{r}_d{d}_num_points{num_points}_longueur{longueur}.svg"

                file_types = "PNG Files (*.png);;SVG Files (*.svg);;PLY Files (*.ply)"
                file_name, _ = QFileDialog.getSaveFileName(self, "Enregistrer la courbe", default_name, file_types)
                if not file_name:
                    return

                fig = plot_hypertrochoid(R, r, d, num_points, color, background, line_width)
                format = file_name.split('.')[-1].lower()
                fig.savefig(file_name, format=format, facecolor=background)
                plt.close(fig)
                print(f"Courbe enregistrée sous {file_name}")
            except Exception as e:
                print(f"Error saving curve: {e}")

        save_button = QPushButton("Enregistrer")
        save_button.clicked.connect(save_curve)
        button_layout.addWidget(save_button)

        def close_tab():
            current_index = self.tab_widget.indexOf(curve_widget)
            if current_index != -1:
                self.tab_widget.removeTab(current_index)
                del self.curve_tabs["Hypertrochoïde"]

        back_button = QPushButton("Retour")
        back_button.clicked.connect(close_tab)
        button_layout.addWidget(back_button)

        preview_layout.addLayout(button_layout)
        curve_widget.setLayout(main_layout)

        return curve_widget


def main():
    app = QApplication([])
    window = AlgemaApp()
    window.show()
    app.exec()



if __name__ == "__main__":
    main()
