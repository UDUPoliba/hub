document.addEventListener("DOMContentLoaded", () => {
    const dataScript = document.getElementById('courseData');
    const contentArea = document.getElementById('contentArea');
    const mainHeader = document.getElementById('mainHeader');

    if (!dataScript) {
        contentArea.innerHTML = `<p style="color: #d92d28; text-align: center;">Dati del corso non trovati.</p>`;
        return;
    }

    let data;
    try {
        data = JSON.parse(dataScript.textContent);
    } catch (e) {
        contentArea.innerHTML = `<p style="color: #d92d28; text-align: center;">Errore nel formato dei dati.</p>`;
        return;
    }

    // Imposta i titoli: Nome del corso in alto, con firma UDU più piccola
    document.title = `UDU Hub - ${data.courseName}`;
    mainHeader.innerHTML = `${data.courseName.toUpperCase()}<br><span style="font-size: 0.5em; font-weight: normal; color: #555;">by UDU ☀️</span>`;

    // Svuota l'area contenuti
    contentArea.innerHTML = '';

    // 1. Rappresentanti (Supporta sia array 'representatives' sia oggetto singolo 'representative')
    let reps = [];
    if (Array.isArray(data.representatives)) {
        reps = data.representatives;
    } else if (data.representative && data.representative.name) {
        reps = [data.representative];
    }

    if (reps.length > 0) {
        const repContainer = document.createElement('div');
        repContainer.style.textAlign = 'center';
        // Margine inferiore quasi azzerato per avvicinarlo a "LINK TEAMS"
        repContainer.style.marginBottom = '0.2em'; 
        repContainer.style.fontSize = '1.1em';
        
        // Plurale o singolare dinamico
        const title = document.createElement('div');
        title.innerHTML = reps.length > 1 ? "Rappresentanti:" : "Rappresentante:";
        repContainer.appendChild(title);

        reps.forEach(rep => {
            const waLink = `https://wa.me/${rep.phone.replace(/\+/g, '')}`;
            const repLink = document.createElement('div');
            repLink.style.marginTop = '0.25em';
            repLink.innerHTML = `<strong><a href="${waLink}" target="_blank" style="color: #10A350; text-decoration: none;">📞 ${rep.name}</a></strong>`;
            repContainer.appendChild(repLink);
        });

        contentArea.appendChild(repContainer);
    }

    // Helper per creare pulsanti link
    function createLinkButton(text, url, variantClass = '') {
        const a = document.createElement('a');
        a.href = url;
        a.target = '_blank';
        a.style.textDecoration = 'none';
        a.style.width = '100%';

        const btn = document.createElement('button');
        btn.innerHTML = `${text} <span aria-hidden="true" style="margin-left:0.5em;">🔗</span>`;
        if (variantClass) btn.classList.add(variantClass);
        
        a.appendChild(btn);
        return a;
    }

    // Helper per creare le etichette delle sezioni
    function createSectionLabel(text) {
        const label = document.createElement('h3');
        label.textContent = text;
        label.style.textAlign = "center";
        label.style.color = "#333";
        label.style.fontSize = "1.3em"; 
        // Margine superiore dimezzato (da 1em a 0.5em) per ridurre il padding
        label.style.margin = "0.5em 0 0.5em 0";
        return label;
    }

    // 2. Link Teams (1 a 1)
    if (data.teams && data.teams.length > 0) {
        contentArea.appendChild(createSectionLabel("LINK TEAMS"));

        data.teams.forEach(team => {
            contentArea.appendChild(createLinkButton(team.name, team.link, "btn-teams"));
        });
    }

    // 3. Materiali / Dispense (1 a 1)
    if (data.materials && data.materials.length > 0) {
        contentArea.appendChild(createSectionLabel("MATERIALE DIDATTICO"));

        data.materials.forEach(mat => {
            contentArea.appendChild(createLinkButton(mat.name, mat.link));
        });
    }

    // 4. Pulsante per tornare all'indice principale
    const hr = document.createElement('hr');
    hr.style.width = "100%";
    hr.style.border = "none";
    hr.style.borderTop = "1px solid #ccc";
    hr.style.marginTop = "1em";
    hr.style.marginBottom = "0.75em";
    contentArea.appendChild(hr);

    const homeBtn = document.createElement('button');
    // Testo del pulsante modificato
    homeBtn.textContent = "Torna a UDU Hub"; 
    homeBtn.classList.add("btn-back");
    homeBtn.onclick = () => {
        window.location.href = "../index.html";
    };
    contentArea.appendChild(homeBtn);
});