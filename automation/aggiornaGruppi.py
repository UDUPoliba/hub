import json
import sys

def aggiorna_gruppi():
    print("🚀 Aggiornamento gruppi WhatsApp in corso...")
    
    try:
        # Caricamento database gruppi e file di produzione
        with open('gruppi.json', 'r', encoding='utf-8') as f:
            database_wz = json.load(f)['gruppi_wz']
        
        with open('../info.json', 'r', encoding='utf-8') as f:
            info = json.load(f)
            
    except FileNotFoundError as e:
        print(f"❌ Errore: File mancante ({e.filename}). Verifica la cartella 'automation'.")
        sys.exit(1)

    # Scansione dei dipartimenti in info.json
    for dip_name, dip_data in info['data'].items():
        if "courses" not in dip_data:
            continue
            
        for corso in dip_data['courses']:
            nome_corso = corso['name']
            
            # --- 1. LOGICA CORSI COMUNI ---
            if dip_name == "CORSI COMUNI":
                if nome_corso in database_wz.get("CORSI COMUNI", {}):
                    link = database_wz["CORSI COMUNI"][nome_corso]
                    for anno in corso.get('years', []):
                        etichetta = nome_corso.replace("Ins.COMUNI Classe", "")
                        anno['groups'] = [{"name": etichetta, "link": link}]

            # --- 2. LOGICA CORSI STANDARD ---
            else:
                # Gestione specifica per Taranto per evitare conflitti con Bari
                chiave_ricerca = nome_corso
                if dip_name == "TARANTO":
                    # Mappatura nomi info.json -> chiavi gruppi.json specifiche per TA
                    mapping_taranto = {
                        "LT Ing. Informatica e Automazione": "LT Ing. Informatica e Automazione (TA)",
                        "LT Ing. Civile e Ambientale": "LT Ing. Civile e Ambientale (TA)"
                    }
                    chiave_ricerca = mapping_taranto.get(nome_corso, nome_corso)

                if chiave_ricerca in database_wz:
                    lista_gruppi_totale = database_wz[chiave_ricerca]
                    
                    for anno_udu in corso.get('years', []):
                        id_anno = str(anno_udu.get('id')) # "1", "2", "3" o "FC"
                        gruppi_pertinenti = []
                        
                        for g in lista_gruppi_totale:
                            nome_g = g['name']
                            
                            # Filtro per Anno (es. "1" in "1° AK" o "Design 1")
                            if id_anno.isdigit() and id_anno in nome_g:
                                gruppi_pertinenti.append(g)
                            
                            # Logica Fuori Corso (FC) -> Inseriti anche al 3° anno
                            if (id_anno == "3" or id_anno == "FC") and "FC" in nome_g:
                                gruppi_pertinenti.append(g)
                            
                            # Logica Speciale Taranto (PTECH e link TA generici)
                            if dip_name == "TARANTO":
                                if "PTECH" in nome_g or "TA" in nome_g:
                                    # Evitiamo duplicati se già aggiunti dal filtro anno
                                    if g not in gruppi_pertinenti:
                                        gruppi_pertinenti.append(g)

                        if gruppi_pertinenti:
                            anno_udu['groups'] = gruppi_pertinenti

    # Salvataggio finale
    try:
        with open('../info.json', 'w', encoding='utf-8') as f:
            json.dump(info, f, indent=2, ensure_ascii=False)
        print("✅ info.json aggiornato con successo!")
    except Exception as e:
        print(f"❌ Errore nel salvataggio: {e}")
        sys.exit(1)

if __name__ == "__main__":
    aggiorna_gruppi()