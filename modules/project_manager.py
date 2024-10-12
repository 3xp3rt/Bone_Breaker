# modules/project_manager.py

import json
import os
from datetime import datetime

def save_project(project_path, data):
    """
    Sauvegarde l'état actuel du projet dans un fichier JSON.

    Args:
        project_path (str): Chemin du dossier du projet.
        data (dict): Données à sauvegarder.
    """
    with open(os.path.join(project_path, 'state.json'), 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def load_project(project_path):
    """
    Charge l'état actuel du projet à partir d'un fichier JSON.

    Args:
        project_path (str): Chemin du dossier du projet.

    Returns:
        dict: Données du projet.
    """
    state_file = os.path.join(project_path, 'state.json')
    if not os.path.exists(state_file):
        raise FileNotFoundError(f"Aucun état trouvé pour le projet à {project_path}.")

    with open(state_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def initialize_project(project_path):
    """
    Initialise un nouveau projet en créant les dossiers nécessaires et un fichier d'état initial.

    Args:
        project_path (str): Chemin du dossier du projet.
    """
    os.makedirs(project_path, exist_ok=True)
    initial_state = {
        'project_name': os.path.basename(project_path),
        'start_time': datetime.utcnow().isoformat() + 'Z',
        'pages': [],
        'requests': [],
        'files': {},
        'mobile': False,
        'status': 'initialized'
    }
    save_project(project_path, initial_state)

def update_project(project_path, key, value):
    """
    Met à jour une clé spécifique dans l'état du projet.

    Args:
        project_path (str): Chemin du dossier du projet.
        key (str): Clé à mettre à jour (ex: 'pages', 'requests').
        value (any): Valeur à ajouter ou mettre à jour.
    """
    state = load_project(project_path)
    if key in state:
        if isinstance(state[key], list):
            if isinstance(value, list):
                state[key].extend(value)
            else:
                state[key].append(value)
        elif isinstance(state[key], dict):
            if isinstance(value, dict):
                state[key].update(value)
            else:
                raise ValueError(f"La clé '{key}' attend un dictionnaire comme valeur.")
        else:
            state[key] = value
    else:
        state[key] = value
    save_project(project_path, state)

def finalize_project(project_path):
    """
    Finalise le projet en enregistrant l'heure de fin et en mettant à jour le statut.

    Args:
        project_path (str): Chemin du dossier du projet.
    """
    state = load_project(project_path)
    state['end_time'] = datetime.utcnow().isoformat() + 'Z'
    state['status'] = 'completed'
    save_project(project_path, state)

def list_projects(users_dir='users'):
    """
    Liste tous les projets disponibles dans le répertoire des utilisateurs.

    Args:
        users_dir (str): Répertoire contenant les dossiers des projets utilisateurs.

    Returns:
        list: Liste des chemins des projets.
    """
    if not os.path.exists(users_dir):
        return []
    return [os.path.join(users_dir, project) for project in os.listdir(users_dir) if os.path.isdir(os.path.join(users_dir, project))]

def delete_project(project_path):
    """
    Supprime un projet et tous ses fichiers.

    Args:
        project_path (str): Chemin du dossier du projet.
    """
    if not os.path.exists(project_path):
        raise FileNotFoundError(f"Le projet {project_path} n'existe pas.")
    for root, dirs, files in os.walk(project_path, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(project_path)
