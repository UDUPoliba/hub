# UDU Hub☀️
---
## Come aggiornare orari e gruppi
Prima di iniziare, assicurati di avere Python installato sul tuo computer. Gli script fanno tutto da soli.

Il sistema si basa su 6 file principali racchiusi nella cartella di automazione, più il database principale.

```bash
automation/
├── gruppi.json        # Database sorgente link WhatsApp
├── poliba.json        # Cache dati grezzi Cineca (auto-generato)
├── run_update.py      # Master Script
├── scraperPoliba.py   # Script di scaricamento dati
├── aggiornaOrari.py   # Script logica Orari
└── aggiornaGruppi.py  # Script logica WhatsApp
```

### Script Python
| File | Funzione |
| :--- | :--- |
| **`run_update.py`** | Lo script principale (Master) da lanciare. Richiama in automatico e in sequenza tutti gli altri script. |
| **`scraperPoliba.py`** | Si connette al Poliba ed esegue il download dei dati grezzi salvandoli in `poliba.json`. |
| **`aggiornaOrari.py`** | Smista i link degli orari da `poliba.json` a `../info.json` incrociando corsi, anni e semestre. |
| **`aggiornaGruppi.py`**| Sincronizza i link WhatsApp da `gruppi.json` a `../info.json`, gestendo in automatico i canali (AL/MZ), la sede di Taranto e i Fuori Corso. |

### File JSON
| File | Contenuto | Note |
| :--- | :--- | :--- |
| **`info.json`** | **Dati per HUB** | Situato nella cartella principale (fuori da automation). Contiene Drive, WhatsApp e Orari. È l'unico file letto dal sito. |
| **`poliba.json`** | **Dati Grezzi Orari** | Contiene i link Cineca appena scaricati. Viene sovrascritto a ogni avvio. |
| **`gruppi.json`** | **Dati Grezzi WhatsApp**| Contiene l'elenco aggiornato dei gruppi WhatsApp diviso per corso. |

### Procedura di Aggiornamento
Apri il terminale ed esegui:

```bash
cd automation
python3 run_update.py
```

Durante l'esecuzione, il terminale andrà in pausa e ti farà una domanda: 
`👉 Quale semestre vuoi aggiornare? (Inserisci 1 o 2): `

Ti basterà digitare il numero corrispondente al semestre in corso e premere **Invio**. Lo script confermerà la scelta e concluderà l'operazione in automatico sia per gli orari che per i gruppi.

### Cosa succede tecnicamente

Il processo di aggiornamento è automatizzato per garantire precisione e velocità. Ecco i passaggi eseguiti dal sistema a catena:

1. **Avvio**: `run_update.py` prende il controllo e avvia la sequenza.
2. **Estrazione e Caching**: `scraperPoliba.py` si connette all'URL ufficiale del Politecnico, estrae la variabile JavaScript `data` e salva i dati grezzi nel file locale `poliba.json`.
3. **Interazione**: `aggiornaOrari.py` si mette in pausa chiedendo all'operatore di selezionare il semestre da filtrare (1S o 2S).
4. **Merge Orari**: `aggiornaOrari.py` confronta `poliba.json` con `../info.json`, filtra i corsi in base al semestre scelto e sovrascrive **solo** i campi relativi ai link degli orari (creando in automatico i sottomenu per i canali A-L/M-Z se necessari).
5. **Merge Gruppi WhatsApp**: `aggiornaGruppi.py` legge `gruppi.json` e inietta i link corretti in `../info.json`, smistandoli per anno di corso, separando la sede di Taranto e aggiungendo i link "FC" nel 3° anno.

### Esito e Risultati

Al termine della procedura, il file `info.json` nella cartella principale risulterà modificato e ottimizzato per la Web App:

* **Conservazione Dati Statici**: I link alle cartelle **Drive** non vengono mai toccati, modificati o cancellati.
* **Update Orari e Gruppi**: I vecchi link Cineca e WhatsApp vengono sostituiti con i nuovi in modo chirurgico.
* **Stato Finale**: Una volta terminato lo script, l'applicazione è immediatamente aggiornata e pronta per essere caricata sul server web o consultata localmente.