import json
import urllib.request
import re
import ssl

def estrai_json_poliba():
    url = "https://www.poliba.it/it/content/orari-delle-lezioni-20252026"
    print(f"⏳ Sto scaricando la pagina: {url}")
    
    # Ignoriamo eventuali errori di certificato SSL (comuni quando si fa scraping)
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    # Ci travestiamo da "Chrome" per non farci bloccare dai firewall del Poliba
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req, context=ctx) as response:
            html = response.read().decode('utf-8')
            
        # MAGIA REGEX: Cerchiamo esattamente la variabile 'const data = { ... };'
        pattern = re.compile(r'const\s+data\s*=\s*(\{.*?\});\s*(?:console\.log|const\s+departmentSelect)', re.DOTALL)
        match = pattern.search(html)
        
        if match:
            json_string = match.group(1) # Estrae solo il testo del JSON
            
            # Lo carichiamo in Python per assicurarci che la sintassi sia perfetta
            dati_json = json.loads(json_string)
            
            # Lo salviamo formattato e ordinato nel file 'poliba.json'
            with open('poliba.json', 'w', encoding='utf-8') as f:
                json.dump(dati_json, f, indent=4, ensure_ascii=False)
                
            print("✅ Successo! Il file 'poliba.json' è stato creato e aggiornato con i dati ufficiali.")
        else:
            print("❌ Errore: Non sono riuscito a trovare la variabile 'data' nella pagina HTML. Forse hanno cambiato il codice del sito?")
            
    except Exception as e:
        print(f"❌ Si è verificato un errore di connessione o lettura: {e}")

# Eseguiamo la funzione
if __name__ == "__main__":
    estrai_json_poliba()
