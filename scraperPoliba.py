import json
import urllib.request
import re
import ssl
import subprocess  # <-- Aggiungi questo all'inizio!

def estrai_json_poliba():
    url = "https://www.poliba.it/it/content/orari-delle-lezioni-20252026"
    print(f"⏳ Sto scaricando la pagina: {url}")
    
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36'
    }
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req, context=ctx) as response:
            html = response.read().decode('utf-8')
            
        pattern = re.compile(r'const\s+data\s*=\s*(\{.*?\});\s*(?:console\.log|const\s+departmentSelect)', re.DOTALL)
        match = pattern.search(html)
        
        if match:
            json_string = match.group(1)
            dati_json = json.loads(json_string)
            
            with open('poliba.json', 'w', encoding='utf-8') as f:
                json.dump(dati_json, f, indent=4, ensure_ascii=False)
                
            print("✅ Successo! Il file 'poliba.json' è stato aggiornato.")
            return True  # <-- Aggiungiamo questo: comunica al sistema che è andato tutto bene
        else:
            print("❌ Errore: Non sono riuscito a trovare la variabile 'data'.")
            return False # <-- Comunica che c'è stato un problema
            
    except Exception as e:
        print(f"❌ Si è verificato un errore: {e}")
        return False

# === NUOVA LOGICA DI AVVIO AUTOMATICO ===
if __name__ == "__main__":
    # Se la funzione restituisce True (lo scraping è andato bene)
    if estrai_json_poliba():
        print("🚀 Scraping completato! Avvio aggiornaOrari.py...")
        try:
            # Lancia il secondo script come se lo scrivessi tu nel terminale
            subprocess.run(["python3", "aggiornaOrari.py"], check=True)
        except Exception as e:
            # NOTA: Se usi Mac o Linux, potresti dover usare "python3" invece di "python"
            print(f"⚠️ Errore nell'avvio del secondo script. Se sei su Mac, prova a cambiare 'python' con 'python3' nel codice: {e}")
    else:
        print("🛑 Scraping fallito. L'aggiornamento di info.json è stato annullato per sicurezza.")
