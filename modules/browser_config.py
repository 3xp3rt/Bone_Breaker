# modules/browser_config.py

from seleniumwire import webdriver as wire_webdriver  # Importer Selenium Wire WebDriver pour Firefox
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import os
import platform
import logging

def find_firefox_path():
    """
    Détecte le chemin de l'exécutable Firefox en fonction du système d'exploitation.
    """
    system = platform.system()
    firefox_path = None

    if system == "Windows":
        possible_paths = [
            os.path.join(os.getenv('PROGRAMFILES'), 'Mozilla Firefox', 'firefox.exe'),
            os.path.join(os.getenv('PROGRAMFILES(X86)'), 'Mozilla Firefox', 'firefox.exe'),
            os.path.join(os.getenv('LOCALAPPDATA'), 'Mozilla Firefox', 'firefox.exe')
        ]
    elif system == "Darwin":  # macOS
        possible_paths = [
            "/Applications/Firefox.app/Contents/MacOS/firefox",
            "/usr/local/bin/firefox"
        ]
    elif system == "Linux":
        possible_paths = [
            "/usr/bin/firefox",
            "/snap/bin/firefox",
            "/usr/local/bin/firefox"
        ]
    else:
        possible_paths = []

    for path in possible_paths:
        if os.path.exists(path):
            firefox_path = path
            break

    if firefox_path and os.path.exists(firefox_path):
        logging.info(f"Firefox trouvé à l'emplacement : {firefox_path}")
        return firefox_path
    else:
        logging.error("Firefox n'a pas été trouvé sur ce système.")
        raise FileNotFoundError("Firefox n'a pas été trouvé sur ce système.")

def launch_selenium_browser(browser_name='firefox', mode='automatique', proxy=None, mobile=False):
    """
    Lance le navigateur spécifié avec Selenium Wire.

    Args:
        browser_name (str): Nom du navigateur ('firefox').
        mode (str): Mode de navigation ('automatique' ou 'manuel').
        proxy (str): Adresse du serveur proxy (optionnel).
        mobile (bool): Activer l'émulation mobile si True.

    Returns:
        webdriver.Firefox: Instance du navigateur lancé.
    """
    if browser_name.lower() == 'firefox':
        options = FirefoxOptions()
        if mode == 'automatique':
            options.headless = True
        elif mode == 'manuel':
            options.headless = False
        else:
            raise ValueError("Mode non supporté. Choisissez 'automatique' ou 'manuel'.")

        if proxy:
            options.set_preference('network.proxy.type', 1)
            options.set_preference('network.proxy.http', proxy)
            options.set_preference('network.proxy.ssl', proxy)
        if mobile:
            # Ajuster la taille de la fenêtre pour simuler un appareil mobile
            options.add_argument('--width=375')
            options.add_argument('--height=667')

        seleniumwire_options = {
            'verify_ssl': False,
        }

        service = FirefoxService()

        try:
            driver = wire_webdriver.Firefox(
                options=options,
                seleniumwire_options=seleniumwire_options,
                service=service
            )
            logging.info("WebDriver Firefox initialisé avec succès.")
            if mobile:
                driver.set_window_size(375, 667)
            return driver
        except Exception as e:
            logging.error(f"Erreur lors de l'initialisation de Firefox : {e}")
            raise
    else:
        raise ValueError("Navigateur non supporté. Choisissez 'firefox'.")

def detect_mobile_version_selenium(driver, url):
    """
    Détecte si la page actuelle est en mode mobile.

    Args:
        driver (webdriver.Firefox): Instance du navigateur Selenium.
        url (str): URL de la page à vérifier.

    Returns:
        bool: True si la page est en mode mobile, False sinon.
    """
    # Vérifier la taille de la fenêtre ou des éléments spécifiques
    width = driver.get_window_size()['width']
    # Définir un seuil, par exemple, moins de 800 pixels de largeur pour mobile
    return width < 800
