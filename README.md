# UDU Hub☀️
---
## Come aggiornare gli orari
Prima di iniziare, assicurati di avere Python installato sul tuo computer. Gli script fanno tutto da soli.

Il sistema si basa su 5 file principali suddivisi tra dati e logica di automazione.

### Script Python
| File | Funzione |
| :--- | :--- |
| **`scraperPoliba.py`**  | Lo script principale da lanciare. Scarica i dati e avvia l'aggiornamento. Richiama in automatico `aggiornaOrari.py`.|
| **`aggiornaOrari.py`** | Smista i link da `poliba.json` a `info.json` incrociando corsi e anni. |
| **`onlyScrape.py`** | Esegue solo il download dei dati grezzi senza modificare l'applicazione. |

### File JSON
| File | Contenuto | Note |
| :--- | :--- | :--- |
| **`info.json`** | **Dati per HUB** | Contiene Drive, Gruppi WhatsApp e Orari. È l'unico file letto dal sito. |
| **`poliba.json`** | **Dati Grezzi** | Contiene solo i link Cineca appena scaricati. Viene sovrascritto a ogni avvio. |

### Procedura di Aggiornamento Orari
```bash
python3 scraperPoliba.py
```

Durante l'esecuzione, il terminale andrà in pausa e ti farà una domanda: 
`👉 Quale semestre vuoi aggiornare? (Inserisci 1 o 2): `

Ti basterà digitare il numero corrispondente al semestre in corso e premere **Invio**. Lo script confermerà la scelta e concluderà l'operazione in automatico.

### Cosa succede tecnicamente

Il processo di aggiornamento è automatizzato per garantire precisione e velocità. Ecco i passaggi eseguiti dal sistema:

1. **Connessione**: `scraperPoliba.py` si connette all'URL ufficiale del Politecnico di Bari.
2. **Estrazione**: Lo script scansiona il codice sorgente HTML alla ricerca della variabile JavaScript `data` e ne estrae il contenuto.
3. **Caching**: I dati grezzi appena prelevati vengono salvati nel file locale `poliba.json`.
4. **Esecuzione a catena**: Se lo scraping ha successo, viene chiamato internamente il comando `python3 aggiornaOrari.py`.
5. **Interazione**: L'esecuzione si mette in pausa chiedendo all'operatore di selezionare il semestre da filtrare (1S o 2S).
6. **Merge Dati**: `aggiornaOrari.py` confronta `poliba.json` con `info.json`, filtra i corsi in base al semestre scelto e sovrascrive **solo** i campi relativi ai link degli orari.

### Esito e Risultati

Al termine della procedura, il file `info.json` risulterà modificato e ottimizzato per la Web App:

* **Conservazione Dati Statici**: I link alle cartelle **Drive** e ai **Gruppi WhatsApp** (inseriti manualmente) non vengono mai toccati, modificati o cancellati.
* **Update Orari**: I vecchi link Cineca vengono sostituiti con i nuovi URL del semestre corrente in modo chirurgico.
* **Stato Finale**: Una volta terminato lo script, l'applicazione è immediatamente aggiornata e pronta per essere caricata sul server web o consultata localmente.

