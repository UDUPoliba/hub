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
                    
                    # TROVIAMO DOVE INSERIRE I FUORI CORSO:
                    # Estrae tutti i numeri degli anni presenti per questo corso
                    anni_numerici = [int(a['id']) for a in corso.get('years', []) if str(a['id']).isdigit()]
                    # Trova l'ultimo anno assoluto (es. "2" per le LM, "3" per LT, "5" per Architettura)
                    ultimo_anno = str(max(anni_numerici)) if anni_numerici else "3"
                    # Controlla se esiste esplicitamente l'anno "FC" creato a mano
                    ha_anno_fc = any(str(a.get('id')) == "FC" for a in corso.get('years', []))
                    
                    # Decidiamo il target: se esiste la voce FC vanno lì, altrimenti nell'ultimo anno
                    target_fc = "FC" if ha_anno_fc else ultimo_anno
                    
                    for anno_udu in corso.get('years', []):
                        id_anno = str(anno_udu.get('id'))
                        gruppi_pertinenti = []
                        
                        for g in lista_gruppi_totale:
                            nome_g = g['name']
                            
                            # Rimuoviamo l'anno accademico (es. 25/26) per non confondere la lettura dei numeri
                            nome_pulito = re.sub(r'\d{2}/\d{2}', '', nome_g)
                            
                            # A) LOGICA FUORI CORSO: Se il nome contiene "FC"
                            if "FC" in nome_g:
                                if id_anno == target_fc:
                                    if g not in gruppi_pertinenti:
                                        gruppi_pertinenti.append(g)
                            
                            # B) LOGICA ANNI NORMALI: Se NON è Fuori Corso
                            else:
                                if id_anno.isdigit() and id_anno in nome_pulito:
                                    if g not in gruppi_pertinenti:
                                        gruppi_pertinenti.append(g)
                            
                            # C) LOGICA SPECIALE TARANTO (I gruppi PTECH e TA si spalmano su tutti gli anni)
                            if dip_name == "TARANTO":
                                if "PTECH" in nome_g or "TA" in nome_g:
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