# modules/dom_analyzer.py

from bs4 import BeautifulSoup
import requests
import logging

# Configuration de base pour BeautifulSoup
def parse_dom(html_content):
    """
    Parse le contenu HTML avec BeautifulSoup.
    
    Args:
        html_content (str): Contenu HTML de la page.
    
    Returns:
        BeautifulSoup: Objet BeautifulSoup pour l'analyse du DOM.
    """
    soup = BeautifulSoup(html_content, 'lxml')
    return soup

def detect_technologies(soup):
    """
    Détecte les technologies utilisées sur la page web en analysant le DOM.
    
    Args:
        soup (BeautifulSoup): Objet BeautifulSoup du DOM.
    
    Returns:
        dict: Dictionnaire des technologies détectées avec leurs versions si disponibles.
    """
    technologies = {}
    
    # Détection des frameworks JavaScript via les balises <script>
    scripts = soup.find_all('script')
    for script in scripts:
        src = script.get('src', '').lower()
        
        # Exemple de détection de React
        if 'react' in src:
            technologies['React'] = extract_version(src, 'react')
        
        # Exemple de détection de Angular
        if 'angular' in src:
            technologies['Angular'] = extract_version(src, 'angular')
        
        # Exemple de détection de Vue.js
        if 'vue' in src:
            technologies['Vue.js'] = extract_version(src, 'vue')
        
        # Ajouter d'autres détections selon les besoins
    
    # Détection via les meta tags
    meta_tags = soup.find_all('meta')
    for meta in meta_tags:
        if meta.get('name') == 'generator':
            technologies['CMS'] = meta.get('content', 'Unknown')
    
    # Détection des frameworks CSS via les balises <link>
    links = soup.find_all('link')
    for link in links:
        href = link.get('href', '').lower()
        if 'bootstrap' in href:
            technologies['Bootstrap'] = extract_version(href, 'bootstrap')
        if 'tailwind' in href:
            technologies['Tailwind CSS'] = extract_version(href, 'tailwind')
    
    return technologies

def extract_version(url, technology):
    """
    Extrait la version d'une technologie à partir de l'URL du script ou du lien.
    
    Args:
        url (str): URL du script ou du lien.
        technology (str): Nom de la technologie.
    
    Returns:
        str: Version détectée ou 'Unknown'.
    """
    import re
    version = 'Unknown'
    patterns = {
        'react': r'react(?:\.min)?\.js(?:\?.*version=)?(\d+\.\d+\.\d+)',
        'angular': r'angular(?:\.min)?\.js(?:\?.*v=)?(\d+\.\d+\.\d+)',
        'vue': r'vue(?:\.min)?\.js(?:\?.*version=)?(\d+\.\d+\.\d+)',
        'bootstrap': r'bootstrap(?:\.min)?\.css(?:\?.*v=)?(\d+\.\d+\.\d+)',
        'tailwind': r'tailwind(?:\.min)?\.css(?:\?.*v=)?(\d+\.\d+\.\d+)'
    }
    
    pattern = patterns.get(technology.lower())
    if pattern:
        match = re.search(pattern, url)
        if match:
            version = match.group(1)
    
    return version

def analyze_page(url, html_content):
    """
    Analyse la page web pour détecter les technologies utilisées.
    
    Args:
        url (str): URL de la page web.
        html_content (str): Contenu HTML de la page.
    
    Returns:
        dict: Dictionnaire contenant l'URL et les technologies détectées.
    """
    soup = parse_dom(html_content)
    technologies = detect_technologies(soup)
    return {
        'url': url,
        'technologies': technologies
    }

def get_html_content(url):
    """
    Récupère le contenu HTML de la page web.
    
    Args:
        url (str): URL de la page web.
    
    Returns:
        str: Contenu HTML de la page.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        logging.error(f"Erreur lors de la récupération de {url} : {e}")
        return ""

