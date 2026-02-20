import json

def aggiorna_orari_udu():
    # 1. Carica i file JSON (assicurati che si chiamino così e siano nella stessa cartella)
    try:
        with open('poliba.json', 'r', encoding='utf-8') as f:
            poliba = json.load(f)
            
        with open('info.json', 'r', encoding='utf-8') as f:
            udu = json.load(f)
    except FileNotFoundError:
        print("Errore: Assicurati di avere i file 'poliba.json' e 'info.json' nella cartella.")
        return

    # 2. Navighiamo nel file dell'UDU per aggiornare i link
    for dipartimento, info_dip in udu['data'].items():
        # Se il dipartimento non esiste nel file Poliba (es. ARCOD), saltalo
        if dipartimento not in poliba:
            continue
            
        lista_corsi_poliba = poliba[dipartimento]

        # Controlliamo ogni corso dell'UDU
        for corso_udu in info_dip.get('courses', []):
            nome_corso = corso_udu.get('name')

            # Controlliamo ogni anno di quel corso
            for anno_udu in corso_udu.get('years', []):
                id_anno = anno_udu.get('id') # Es: "1", "2", "3"
                
                # Cerchiamo le corrispondenze nel file Poliba
                # Regola: Il nome del corso deve essere identico e l'anno deve iniziare col numero giusto (es. "1°")
                match_trovati = [
                    p for p in lista_corsi_poliba 
                    if p['name'] == nome_corso and p['year'].startswith(f"{id_anno}°")
                ]

                # Se non c'è nessun orario, passiamo oltre (ECCO IL FIX QUI SOTTO!)
                if not match_trovati:
                    continue
                
                # Se c'è UN SOLO orario per quell'anno (es. canale unico)
                if len(match_trovati) == 1:
                    anno_udu['time_table'] = match_trovati[0]['link']
                
                # Se ci sono PIÙ orari (es. divisi per cognome o percorso)
                else:
                    # Creiamo un sotto-menu per l'UDU (il JS dell'UDU sa già leggerlo!)
                    dict_orari = {}
                    for match in match_trovati:
                        # Usiamo la stringa originale del Poliba (es. "2° - Cognome AL") come nome del bottone
                        dict_orari[match['year']] = match['link']
                    
                    anno_udu['time_table'] = dict_orari

    # 3. Salva il nuovo file aggiornato
    with open('info.json', 'w', encoding='utf-8') as f:
        json.dump(udu, f, indent=2, ensure_ascii=False)

    print("🎉 Aggiornamento completato! Esci dall’ombra, scegli il sole!☀️")

# Avvia lo script
aggiorna_orari_udu()
