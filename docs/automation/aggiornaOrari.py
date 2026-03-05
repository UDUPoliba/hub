import json

def aggiorna_orari_udu():
    print("☀️ Benvenuto nell'aggiornamento orari UDU!")
    
    # --- NUOVA LOGICA INTERATTIVA ---
    # Chiediamo all'utente quale semestre aggiornare e controlliamo che l'input sia corretto
    while True:
        scelta = input("👉 Quale semestre vuoi aggiornare? (Inserisci 1 o 2): ").strip()
        if scelta in ['1', '2']:
            semestre_scelto = f"{scelta}S" # Trasforma "1" in "1S" o "2" in "2S"
            break
        else:
            print("❌ Input non valido. Per favore, digita solo il numero 1 o il numero 2 e premi Invio.")

    print(f"⏳ Ottimo! Procedo con la mappatura per il semestre: {semestre_scelto}...")

    # 1. Carica i file JSON
    try:
        with open('poliba.json', 'r', encoding='utf-8') as f:
            poliba = json.load(f)
            
        with open('../info.json', 'r', encoding='utf-8') as f:
            udu = json.load(f)
    except FileNotFoundError:
        print("❌ Errore: Assicurati di avere i file 'poliba.json' e 'info.json' nella cartella.")
        return

    # 2. Navighiamo nel file dell'UDU per aggiornare i link
    for dipartimento, info_dip in udu['data'].items():
        if dipartimento not in poliba:
            continue
            
        lista_corsi_poliba = poliba[dipartimento]

        for corso_udu in info_dip.get('courses', []):
            nome_corso = corso_udu.get('name')

            for anno_udu in corso_udu.get('years', []):
                id_anno = str(anno_udu.get('id'))
                
                # Cerchiamo le corrispondenze usando il semestre scelto dall'utente!
                match_trovati = [
                    p for p in lista_corsi_poliba 
                    if p['name'] == nome_corso 
                    and str(p['year']).startswith(f"{id_anno}°")
                    and p.get('semester') == semestre_scelto
                ]

                # Se non c'è nessun orario, passiamo oltre
                if not match_trovati:
                    continue
                
                # Se c'è UN SOLO orario per quell'anno
                if len(match_trovati) == 1:
                    anno_udu['time_table'] = match_trovati[0]['link']
                
                # Se ci sono PIÙ orari (es. canali AL-MZ)
                else:
                    dict_orari = {}
                    for match in match_trovati:
                        dict_orari[match['year']] = match['link']
                    
                    anno_udu['time_table'] = dict_orari

    # ---Iniettiamo il semestre attivo per index.html ---
    # Se hai digitato '1' imposta 'I', altrimenti 'II'
    udu['semestre_attivo'] = "I" if scelta == "1" else "II"

    # 3. Salva il nuovo file aggiornato
    with open('../info.json', 'w', encoding='utf-8') as f:
        json.dump(udu, f, indent=2, ensure_ascii=False)

    print(f"🎉 Aggiornamento completato! Esci dall’ombra, scegli il sole!☀️")

# Avvia lo script (Aggiunto il blocco main per le buone pratiche Python)
if __name__ == "__main__":
    aggiorna_orari_udu()