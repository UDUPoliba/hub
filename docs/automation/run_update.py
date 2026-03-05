import subprocess
import sys

def run_step(script_name):
    print(f"🚀 Avvio {script_name}...")
    try:
        # Esegue lo script e attende che finisca
        subprocess.run([sys.executable, script_name], check=True)
        return True
    except subprocess.CalledProcessError:
        print(f"❌ Errore durante l'esecuzione di {script_name}. Processo interrotto.")
        return False

if __name__ == "__main__":
    print("☀️ --- UDU HUB: AGGIORNAMENTO COMPLETO --- ☀️\n")
    
    # Sequenza di esecuzione
    steps = [
        "scraperPoliba.py",  # Scarica poliba.json
        "aggiornaOrari.py",   # Aggiorna Cineca in info.json
        "aggiornaGruppi.py"   # Aggiorna WhatsApp in info.json
    ]
    
    for step in steps:
        if not run_step(step):
            sys.exit(1) # Esce se uno dei passaggi fallisce
            
    print("\n✨ TUTTO SISTEMATO! L'Hub è aggiornato e pronto. ☀️")