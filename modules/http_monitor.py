# modules/http_monitor.py

import json
import os

def intercept_requests_selenium(driver):
    """
    Capture les requêtes HTTP/HTTPS interceptées par Selenium Wire.

    Args:
        driver (webdriver.Firefox): Instance du navigateur Selenium.

    Returns:
        list: Liste des requêtes capturées avec leurs détails.
    """
    intercepted_requests = []
    for request in driver.requests:
        if request.response:
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
            intercepted_requests.append(data)
    return intercepted_requests

def save_requests(project_path, requests_data):
    """
    Sauvegarde les données des requêtes capturées dans un fichier JSON.

    Args:
        project_path (str): Chemin du dossier du projet utilisateur.
        requests_data (list): Liste des requêtes capturées.
    """
    with open(os.path.join(project_path, 'requests.log'), 'w', encoding='utf-8') as f:
        json.dump(requests_data, f, indent=4, ensure_ascii=False)
