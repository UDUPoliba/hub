import json
import urllib.request
import ssl
import time
import re

def verifica_link_whatsapp():
    print("🔍 Avvio scansione con il 'Trick' del titolo... (potrebbe volerci un minuto)\n")
    
    # Ignora errori di certificato
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    # Fingiamo di essere un browser reale
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7'
    }

    try:
        with open('gruppi.json', 'r', encoding='utf-8') as f:
            dati = json.load(f)['gruppi_wz']
    except FileNotFoundError:
        print("❌ Errore: file 'gruppi.json' non trovato.")
        return

    link_scaduti = []
    totali = 0

    # Regex per catturare esattamente il titolo della pagina / anteprima
    pattern_titolo = re.compile(r'<meta property="og:title"\s+content="([^"]+)"', re.IGNORECASE)

    # Naviga nel database dei gruppi
    for categoria, gruppi in dati.items():
        if isinstance(gruppi, dict):
            da_controllare = [{"name": k, "link": v} for k, v in gruppi.items()]
        else:
            da_controllare = gruppi

        for gruppo in da_controllare:
            nome = gruppo['name']
            link = gruppo['link']
            totali += 1
            
            try:
                req = urllib.request.Request(link, headers=headers)
                with urllib.request.urlopen(req, context=ctx, timeout=10) as response:
                    html = response.read().decode('utf-8')
                    
                    # Estraiamo il titolo nascosto nella pagina
                    match = pattern_titolo.search(html)
                    titolo_trovato = match.group(1).strip() if match else ""
                    titolo_lower = titolo_trovato.lower()
                    
                    # IL TUO TRICK: Se il titolo è vuoto, o è SOLO la frase generica, allora è scaduto!
                    if not titolo_trovato or "invito alla chat di gruppo" in titolo_lower or "whatsapp group invite" in titolo_lower:
                        print(f"❌ SCADUTO: {categoria} -> {nome}")
                        link_scaduti.append(f"{categoria} - {nome}\n      Link: {link}")
                    else:
                        print(f"✅ OK: {categoria} -> {nome} (Rilevato: {titolo_trovato})")
            
            except urllib.error.HTTPError as e:
                print(f"⚠️ ATTENZIONE: WhatsApp ha bloccato la richiesta per {nome} (Errore {e.code})")
            except Exception as e:
                print(f"⚠️ ERRORE DI RETE per {nome}: ({e})")
            
            # Pausa per non sembrare uno spam bot
            time.sleep(0.5)

    print("\n" + "="*50)
    print(f"📊 REPORT FINALE: Controllati {totali} link.")
    if link_scaduti:
        print(f"🚨 Trovati {len(link_scaduti)} link SCADUTI/NON VALIDI:")
        for l in link_scaduti:
            print(f"   - {l}")
    else:
        print("🎉 TUTTI I LINK SONO FUNZIONANTI!")
    print("="*50)

if __name__ == "__main__":
    verifica_link_whatsapp()
