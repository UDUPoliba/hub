import json
import sys
import re

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
                chiave_ricerca = nome_corso
                # Separazione Taranto-Bari per evitare omonimie
                if dip_name == "TARANTO":
                    mapping_taranto = {
                        "LT Ing. Informatica e Automazione": "LT Ing. Informatica e Automazione (TA)",
                        "LT Ing. Civile e Ambientale": "LT Ing. Civile e Ambientale (TA)"
                    }
                    chiave_ricerca = mapping_taranto.get(nome_corso, nome_corso)

                if chiave_ricerca in database_wz:
                    lista_gruppi_totale = database_wz[chiave_ricerca]
                    
                    # TROVIAMO GLI ANNI TARGET
                    anni_numerici = [int(a['id']) for a in corso.get('years', []) if str(a['id']).isdigit()]
                    ultimo_anno = str(max(anni_numerici)) if anni_numerici else "3"
                    ha_anno_fc = any(str(a.get('id')) == "FC" for a in corso.get('years', []))
                    target_fc = "FC" if ha_anno_fc else ultimo_anno
                    
                    for anno_udu in corso.get('years', []):
                        id_anno = str(anno_udu.get('id'))
                        gruppi_pertinenti = []
                        
                        for g in lista_gruppi_totale:
                            nome_g = g['name']
                            
                            # Rimuoviamo l'anno accademico (es. 25/26) per non confondere la lettura dei numeri
                            nome_pulito = re.sub(r'\d{2}/\d{2}', '', nome_g)
                            
                            # Identikit del gruppo
                            is_fc = "FC" in nome_g
                            has_number = any(str(num) in nome_pulito for num in range(1, 7))
                            is_taranto_special = (dip_name == "TARANTO" and ("PTECH" in nome_g or "TA" in nome_g))
                            
                            # A) LOGICA FUORI CORSO
                            if is_fc:
                                if id_anno == target_fc:
                                    if g not in gruppi_pertinenti:
                                        gruppi_pertinenti.append(g)
                            
                            # B) LOGICA ANNI NORMALI
                            elif has_number:
                                if id_anno.isdigit() and id_anno in nome_pulito:
                                    if g not in gruppi_pertinenti:
                                        gruppi_pertinenti.append(g)
                            
                            # C) LOGICA "CV/SENZA NOME" (Senza numero e senza FC -> Curriculum/Indirizzo)
                            elif not is_taranto_special:
                                if id_anno == ultimo_anno:
                                    if g not in gruppi_pertinenti:
                                        gruppi_pertinenti.append(g)
                            
                            # D) LOGICA SPECIALE TARANTO (PTECH e TA si spalmano su tutti gli anni)
                            if is_taranto_special:
                                if g not in gruppi_pertinenti:
                                    gruppi_pertinenti.append(g)

                        # Sovrascrive i gruppi di quell'anno pulendo quelli vecchi/sbagliati
                        anno_udu['groups'] = gruppi_pertinenti

    # Salvataggio finale
    try:
        with open('../info.json', 'w', encoding='utf-8') as f:
            json.dump(info, f, indent=2, ensure_ascii=False)
        print("✅ info.json aggiornato con successo! I gruppi sono al loro posto.")
    except Exception as e:
        print(f"❌ Errore nel salvataggio: {e}")
        sys.exit(1)

if __name__ == "__main__":
    aggiorna_gruppi()