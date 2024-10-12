# modules/user_interactions.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

def simulate_user_interaction(driver):
    """
    Simule des interactions utilisateur sur la page web.
    
    Args:
        driver (webdriver.Firefox): Instance du navigateur Selenium.
    """
    try:
        # Exemple 1 : Remplir un champ de recherche et soumettre
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'q'))  # Modifier le sélecteur selon la page
        )
        search_box.send_keys('Selenium WebDriver')
        search_box.submit()
        logging.info("Recherche effectuée avec succès.")
        
        # Attendre que les résultats de la recherche soient chargés
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'result-stats'))  # Modifier le sélecteur selon la page
        )
        logging.info("Résultats de la recherche chargés.")
        
        # Exemple 2 : Cliquer sur le premier résultat de recherche
        first_result = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'h3'))
        )
        first_result.click()
        logging.info("Navigation vers le premier résultat réussie.")
        
        # Attendre que la nouvelle page soit chargée
        WebDriverWait(driver, 10).until(
            EC.title_contains('Selenium')
        )
        logging.info("Nouvelle page chargée avec succès.")
        
        # Exemple 3 : Remplir un formulaire de contact (si disponible)
        # Ceci est un exemple générique. Adaptez-le selon la structure de la page.
        try:
            contact_form = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'contact-form'))  # Modifier le sélecteur selon la page
            )
            name_field = contact_form.find_element(By.NAME, 'name')
            email_field = contact_form.find_element(By.NAME, 'email')
            message_field = contact_form.find_element(By.NAME, 'message')
            
            name_field.send_keys('John Doe')
            email_field.send_keys('john.doe@example.com')
            message_field.send_keys('Ceci est un message de test.')
            
            submit_button = contact_form.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
            submit_button.click()
            logging.info("Formulaire de contact soumis avec succès.")
            
            # Attendre une confirmation
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.thank-you-message'))  # Modifier le sélecteur selon la page
            )
            logging.info("Confirmation de soumission du formulaire reçue.")
        except Exception as e:
            logging.warning(f"Aucun formulaire de contact trouvé ou erreur lors de la soumission : {e}")
        
    except Exception as e:
        logging.error(f"Erreur lors de la simulation des interactions utilisateur : {e}")

def simulate_navigation(driver):
    """
    Simule une navigation conditionnelle entre les pages.
    
    Args:
        driver (webdriver.Firefox): Instance du navigateur Selenium.
    """
    try:
        # Exemple : Naviguer vers une page spécifique via le menu
        menu_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, 'About'))  # Modifier le texte du lien selon la page
        )
        menu_link.click()
        logging.info("Navigation vers la page 'About' réussie.")
        
        # Attendre que la nouvelle page soit chargée
        WebDriverWait(driver, 10).until(
            EC.title_contains('About')
        )
        logging.info("Page 'About' chargée avec succès.")
        
    except Exception as e:
        logging.error(f"Erreur lors de la simulation de navigation : {e}")
