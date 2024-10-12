# bone_breaker.py

import argparse
import os
import sys
import json
from datetime import datetime
from modules.browser_config import (
    launch_selenium_browser,
    detect_mobile_version_selenium
)
from modules.http_monitor import (
    intercept_requests_selenium,
    save_requests
)
from modules.dom_analyzer import (
    analyze_page,
    get_html_content
)
from modules.user_interactions import (
    simulate_user_interaction,
    simulate_navigation
)
import threading
import time
import logging

# Configuration de base pour les logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def parse_arguments():
    """
    Analyse les arguments en ligne de commande fournis par l'utilisateur.

    Returns:
        argparse.Namespace: Les arguments analysés.
    """
    parser = argparse.ArgumentParser(description='Bone Brocker - Web Auditor')
    parser.add_argument('--url', required=True, help='URL à auditer (ex: https://www.google.com)')
    parser.add_argument('--browser', choices=['firefox'], default='firefox', help='Navigateur à utiliser (seulement Firefox est supporté)')
    parser.add_argument('--mode', choices=['automatique', 'manuel'], default='automatique', help='Mode de navigation (automatique ou manuel)')
    parser.add_argument('--mobile', action='store_true', help='Activer l\'émulation mobile')
    args = parser.parse_args()
    return args

def create_project_directory():
    """
    Crée un répertoire unique pour stocker les résultats de l'audit.

    Returns:
        str: Le chemin du répertoire créé.
    """
    base_dir = 'users'
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    project_dir = os.path.join(base_dir, f'user_project_{timestamp}')
    os.makedirs(project_dir, exist_ok=True)
    return project_dir

def update_state_json(project_dir, audit_info):
    """
    Sauvegarde les informations de l'audit dans un fichier state.json.

    Args:
        project_dir (str): Chemin du répertoire du projet utilisateur.
        audit_info (dict): Informations de l'audit à sauvegarder.
    """
    state_file = os.path.join(project_dir, 'state.json')
    with open(state_file, 'w', encoding='utf-8') as f:
        json.dump(audit_info, f, indent=4, ensure_ascii=False)

def monitor_requests(driver, requests_file, stop_event):
    """
    Surveille les requêtes HTTP/HTTPS en temps réel et les sauvegarde dans un fichier JSON.

    Args:
        driver (webdriver.Firefox): Instance du navigateur Selenium.
        requests_file (str): Chemin du fichier JSON pour sauvegarder les requêtes.
        stop_event (threading.Event): Événement pour signaler l'arrêt de la surveillance.
    """
    print("Début de la surveillance des requêtes HTTP/HTTPS...")
    logging.info("Début de la surveillance des requêtes HTTP/HTTPS...")
    processed_requests = set()

    while not stop_event.is_set():
        try:
            for request in driver.requests:
                if request.response and request.url not in processed_requests:
                    processed_requests.add(request.url)
                    # Tenter d'accéder aux cookies via 'cookies' attribut
                    try:
                        cookies = request.response.cookies
                    except AttributeError:
                        # Si 'cookies' n'existe pas, récupérer via 'Set-Cookie' header
                        set_cookie = request.response.headers.get('Set-Cookie', '')
                        cookies = set_cookie if set_cookie else ''
                    data = {
                        'url': request.url,
                        'method': request.method,
                        'status_code': request.response.status_code,
                        'request_headers': dict(request.headers),
                        'response_headers': dict(request.response.headers),
                        'cookies': cookies
                    }

                    # Lire les requêtes déjà sauvegardées
                    with open(requests_file, 'r', encoding='utf-8') as f:
                        try:
                            existing_data = json.load(f)
                        except json.JSONDecodeError:
                            existing_data = []

                    # Ajouter la nouvelle requête
                    existing_data.append(data)

                    # Sauvegarder les requêtes mises à jour
                    with open(requests_file, 'w', encoding='utf-8') as f:
                        json.dump(existing_data, f, indent=4, ensure_ascii=False)

                    print(f"Nouvelle requête capturée : {request.url}")
                    logging.info(f"Nouvelle requête capturée : {request.url}")
            time.sleep(1)  # Pause pour éviter une surcharge CPU
        except Exception as e:
            print(f"Erreur lors de la surveillance des requêtes : {e}")
            logging.error(f"Erreur lors de la surveillance des requêtes : {e}")
            break
    print("Fin de la surveillance des requêtes.")
    logging.info("Fin de la surveillance des requêtes.")

def run_selenium_audit(url, mode, mobile, project_dir):
    """
    Exécute l'audit web en utilisant Selenium avec Firefox.

    Args:
        url (str): URL à auditer.
        mode (str): Mode de navigation ('automatique' ou 'manuel').
        mobile (bool): Activer l'émulation mobile si True.
        project_dir (str): Chemin du répertoire du projet utilisateur.
    """
    try:
        print(f"Lancement de Selenium Firefox en mode {mode}...")
        logging.info(f"Lancement de Selenium Firefox en mode {mode}...")
        # Lancer Firefox via Selenium
        driver = launch_selenium_browser(browser_name='firefox', mode=mode, mobile=mobile)
        print(f"Naviguer vers l'URL : {url}")
        logging.info(f"Naviguer vers l'URL : {url}")
        driver.get(url)
        title = driver.title
        print(f"Titre de la page : {title}")
        logging.info(f"Titre de la page : {title}")
        
        # **Suppression de l'assertion rigide sur le titre**
        # assert title == "Google", "Selenium Firefox : Titre incorrect"

        # Optionnel : Vérifier que la page a bien été chargée
        if not title:
            logging.warning("Le titre de la page est vide.")
        else:
            logging.info(f"Page chargée avec le titre : {title}")

        # Analyse du DOM et détection des technologies
        logging.info("Analyse du DOM et détection des technologies utilisées...")
        html_content = driver.page_source
        dom_analysis = analyze_page(url, html_content)
        technologies_detected = dom_analysis['technologies']
        logging.info(f"Technologies détectées : {technologies_detected}")

        # Sauvegarder les résultats de l'analyse du DOM
        dom_analysis_file = os.path.join(project_dir, 'dom_analysis.json')
        with open(dom_analysis_file, 'w', encoding='utf-8') as f:
            json.dump(dom_analysis, f, indent=4, ensure_ascii=False)
        logging.info("Analyse du DOM sauvegardée dans dom_analysis.json.")

        if mode == 'automatique':
            print("Simuler des interactions utilisateur...")
            logging.info("Simuler des interactions utilisateur...")
            # Simuler des interactions utilisateur
            simulate_user_interaction(driver)
            simulate_navigation(driver)

            print("Capture des requêtes HTTP/HTTPS...")
            logging.info("Capture des requêtes HTTP/HTTPS...")
            # Capturer les requêtes HTTP/HTTPS
            requests_data = intercept_requests_selenium(driver)
            assert isinstance(requests_data, list), "Les requêtes capturées doivent être une liste"
            print(f"{len(requests_data)} requêtes capturées.")
            logging.info(f"{len(requests_data)} requêtes capturées.")

            print("Sauvegarde des requêtes dans un fichier JSON...")
            logging.info("Sauvegarde des requêtes dans un fichier JSON...")
            # Sauvegarder les requêtes dans un fichier JSON
            save_requests(project_dir, requests_data)

            # Fermer le navigateur
            driver.quit()
            print("Test Selenium Firefox réussi.")
            logging.info("Test Selenium Firefox réussi.")

            # Sauvegarder les informations de l'audit
            audit_info = {
                'url': url,
                'browser': 'firefox',
                'mode': mode,
                'mobile': mobile,
                'timestamp': datetime.now().isoformat(),
                'technologies_detected': technologies_detected,
                'interactions': 'Simulées automatiquement'
            }
            update_state_json(project_dir, audit_info)
            print("Informations de l'audit sauvegardées dans state.json.")
            logging.info("Informations de l'audit sauvegardées dans state.json.")

        elif mode == 'manuel':
            print("Mode manuel activé. Vous pouvez maintenant interagir avec le navigateur.")
            logging.info("Mode manuel activé. Vous pouvez maintenant interagir avec le navigateur.")
            print("La capture des requêtes commencera en arrière-plan.")
            logging.info("La capture des requêtes commencera en arrière-plan.")

            # Créer un fichier pour les requêtes
            requests_file = os.path.join(project_dir, 'requests.log')
            with open(requests_file, 'w', encoding='utf-8') as f:
                json.dump([], f, indent=4, ensure_ascii=False)

            # Démarrer un thread pour surveiller les requêtes
            stop_event = threading.Event()
            monitor_thread = threading.Thread(target=monitor_requests, args=(driver, requests_file, stop_event))
            monitor_thread.start()

            try:
                # Attendre que le navigateur soit fermé manuellement
                while True:
                    # Méthode 1 : Vérification de driver.session_id
                    if driver.session_id is None:
                        print("Navigateur fermé par l'utilisateur.")
                        logging.info("Navigateur fermé par l'utilisateur.")
                        break

                    # Méthode 2 : Vérification de l'état du processus
                    if hasattr(driver.service, 'process') and driver.service.process.poll() is not None:
                        print("Navigateur fermé par l'utilisateur.")
                        logging.info("Navigateur fermé par l'utilisateur.")
                        break

                    time.sleep(1)
            except KeyboardInterrupt:
                print("Interruption par l'utilisateur.")
                logging.info("Interruption par l'utilisateur.")
            finally:
                # Signaler au thread de surveiller d'arrêter
                stop_event.set()
                monitor_thread.join()

                # Fermer le navigateur si ce n'est pas déjà fait
                if hasattr(driver.service, 'process') and driver.service.process.poll() is None:
                    driver.quit()
                    logging.info("Navigateur fermé par le script.")
                print("Audit manuel terminé.")
                logging.info("Audit manuel terminé.")

                # Sauvegarder les informations de l'audit
                audit_info = {
                    'url': url,
                    'browser': 'firefox',
                    'mode': mode,
                    'mobile': mobile,
                    'timestamp': datetime.now().isoformat(),
                    'technologies_detected': technologies_detected,
                    'interactions': 'Simulées manuellement'
                }
                update_state_json(project_dir, audit_info)
                print("Informations de l'audit sauvegardées dans state.json.")
                logging.info("Informations de l'audit sauvegardées dans state.json.")

    except Exception as e:
        logging.error(f"Erreur lors de l'audit Selenium : {e}")
        print(f"Erreur lors de l'audit Selenium : {e}")
        # Optionnel : sauvegarder les informations d'audit en cas d'échec
        audit_info = {
            'url': url,
            'browser': 'firefox',
            'mode': mode,
            'mobile': mobile,
            'timestamp': datetime.now().isoformat(),
            'technologies_detected': technologies_detected if 'technologies_detected' in locals() else {},
            'interactions': 'Erreur durant l\'audit'
        }
        update_state_json(project_dir, audit_info)
        print("Informations de l'audit sauvegardées dans state.json malgré l'erreur.")
        logging.info("Informations de l'audit sauvegardées dans state.json malgré l'erreur.")

def main():
    """
    Fonction principale orchestrant l'exécution des audits Selenium.
    """
    # Analyser les arguments en ligne de commande
    args = parse_arguments()

    # Créer un répertoire de projet unique
    project_dir = create_project_directory()
    print(f"Répertoire de projet créé : {project_dir}")
    logging.info(f"Répertoire de projet créé : {project_dir}")

    # Exécuter l'audit Selenium
    run_selenium_audit(args.url, args.mode, args.mobile, project_dir)

if __name__ == "__main__":
    main()
