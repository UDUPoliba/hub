import json
import urllib.request
import re
import ssl
import sys # <--- Necessario per segnalare errori al Master Script

def estrai_json_poliba():
    url = "https://www.poliba.it/it/content/orari-delle-lezioni-20252026"
    print(f"⏳ Sto scaricando la pagina: {url}")
    
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req, context=ctx) as response:
            html = response.read().decode('utf-8')
            
        # La tua Regex è ottima, la manteniamo!
        pattern = re.compile(r'const\s+data\s*=\s*(\{.*?\});\s*(?:console\.log|const\s+departmentSelect)', re.DOTALL)
        match = pattern.search(html)
        
        if match:
            json_string = match.group(1)
            dati_json = json.loads(json_string)
            
            # Salvataggio locale nella cartella automation
            with open('poliba.json', 'w', encoding='utf-8') as f:
                json.dump(dati_json, f, indent=4, ensure_ascii=False)
                
            print("✅ Successo! Il file 'poliba.json' è stato aggiornato.")
            return True # <--- Segnala il successo
        else:
            print("❌ Errore: Variabile 'data' non trovata.")
            return False # <--- Segnala il fallimento
            
    except Exception as e:
        print(f"❌ Errore di connessione: {e}")
        return False

if __name__ == "__main__":
    # Se la funzione fallisce, usciamo con un codice di errore (1)
    # così run_update.py capisce che deve interrompere tutto.
    if not estrai_json_poliba():
        sys.exit(1)