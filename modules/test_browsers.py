# modules/test_browsers.py

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
import sys
import os
import json

def test_selenium_firefox_automatic():
    try:
        print("Lancement de Selenium Firefox en mode automatique...")
        driver = launch_selenium_browser(browser_name='firefox', mode='automatique', mobile=False)
        print(f"Naviguer vers l'URL : https://www.google.com")
        driver.get('https://www.google.com')
        title = driver.title
        print(f"Titre de la page : {title}")
        assert title == "Google", "Selenium Firefox : Titre incorrect"
        
        # Analyse du DOM
        html_content = driver.page_source
        dom_analysis = analyze_page('https://www.google.com', html_content)
        technologies_detected = dom_analysis['technologies']
        print(f"Technologies détectées : {technologies_detected}")
        assert isinstance(technologies_detected, dict), "Les technologies détectées doivent être un dictionnaire"

        # Sauvegarder l'analyse du DOM
        test_project_path_dom = os.path.join('test_projects', 'test_project_firefox_dom')
        os.makedirs(test_project_path_dom, exist_ok=True)
        dom_analysis_file = os.path.join(test_project_path_dom, 'dom_analysis.json')
        with open(dom_analysis_file, 'w', encoding='utf-8') as f:
            json.dump(dom_analysis, f, indent=4, ensure_ascii=False)
        print("Analyse du DOM sauvegardée.")
        
        print("Simuler des interactions utilisateur...")
        simulate_user_interaction(driver)
        simulate_navigation(driver)

        print("Capture des requêtes HTTP/HTTPS...")
        requests_data = intercept_requests_selenium(driver)
        assert isinstance(requests_data, list), "Les requêtes capturées doivent être une liste"
        print(f"{len(requests_data)} requêtes capturées.")

        # Sauvegarder les requêtes capturées
        test_project_path_requests = os.path.join('test_projects', 'test_project_firefox_requests')
        os.makedirs(test_project_path_requests, exist_ok=True)
        save_requests(test_project_path_requests, requests_data)
        print("Requêtes HTTP/HTTPS sauvegardées.")

        driver.quit()
        print("Test Selenium Firefox Automatique réussi.\n")
    except Exception as e:
        print(f"Test Selenium Firefox Automatique échoué : {e}")
        sys.exit(1)

def test_selenium_firefox_manual():
    try:
        print("Lancement de Selenium Firefox en mode manuel...")
        driver = launch_selenium_browser(browser_name='firefox', mode='manuel', mobile=True)
        print(f"Naviguer vers l'URL : https://www.google.com")
        driver.get('https://www.google.com')
        is_mobile = detect_mobile_version_selenium(driver, 'https://www.google.com')
        print(f"Mode mobile détecté : {is_mobile}")
        assert is_mobile, "Selenium Mobile Firefox : Détection mobile échouée"
        
        # Analyse du DOM
        html_content = driver.page_source
        dom_analysis = analyze_page('https://www.google.com', html_content)
        technologies_detected = dom_analysis['technologies']
        print(f"Technologies détectées : {technologies_detected}")
        assert isinstance(technologies_detected, dict), "Les technologies détectées doivent être un dictionnaire"

        # Sauvegarder l'analyse du DOM
        test_project_path_dom = os.path.join('test_projects', 'test_project_manual_firefox_dom')
        os.makedirs(test_project_path_dom, exist_ok=True)
        dom_analysis_file = os.path.join(test_project_path_dom, 'dom_analysis.json')
        with open(dom_analysis_file, 'w', encoding='utf-8') as f:
            json.dump(dom_analysis, f, indent=4, ensure_ascii=False)
        print("Analyse du DOM sauvegardée.")
        
        print("Simuler des interactions utilisateur...")
        simulate_user_interaction(driver)
        simulate_navigation(driver)

        print("Capture des requêtes HTTP/HTTPS...")
        requests_data = intercept_requests_selenium(driver)
        assert isinstance(requests_data, list), "Les requêtes capturées doivent être une liste"
        print(f"{len(requests_data)} requêtes capturées.")

        # Sauvegarder les requêtes capturées
        test_project_path_requests = os.path.join('test_projects', 'test_project_manual_firefox_requests')
        os.makedirs(test_project_path_requests, exist_ok=True)
        save_requests(test_project_path_requests, requests_data)
        print("Requêtes HTTP/HTTPS sauvegardées.")

        driver.quit()
        print("Test Selenium Firefox Manuel réussi.\n")
    except Exception as e:
        print(f"Test Selenium Firefox Manuel échoué : {e}")
        sys.exit(1)

def main():
    """
    Fonction principale orchestrant l'exécution des audits Selenium.
    """
    # Créer le répertoire des projets de test si nécessaire
    os.makedirs('test_projects', exist_ok=True)

    # Exécuter les tests synchrones
    test_selenium_firefox_automatic()
    test_selenium_firefox_manual()

if __name__ == "__main__":
    main()
