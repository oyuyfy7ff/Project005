// web/script.js
async function initSystem() {
    try {
        const res = await fetch('../data/report.json');
        if (!res.ok) throw new Error("FILE_NOT_FOUND");
        const data = await res.json();
        renderTerminal(data);
        document.getElementById('update-time').innerText = `[ LAST SYNC: ${new Date().toLocaleTimeString()} ]`;
    } catch (err) {
        document.getElementById('data-grid').innerHTML = `<p class="alert">[!] FATAL: UNABLE TO MOUNT DATA PORT (${err.message})</p>`;
    }
}

function renderTerminal(nodes) {
    const grid = document.getElementById('data-grid');
    grid.innerHTML = '';
    
    nodes.forEach(node => {
        let status = node.is_private ? "PRIVATE" : "PUBLIC";
        let matchUI = "";
        
        if (node.matches && node.matches.length > 0) {
            matchUI = `<div class="row alert">[ WARNING: TARGET DETECTED ]</div>`;
            node.matches.forEach(img => {
                matchUI += `<img src="${img}" class="img-evidence">`;
            });
        }

        grid.innerHTML += `
            <div class="card">
                <h2>@${node.username}</h2>
                <div class="row"><span class="label">ID:</span> ${node.full_name || 'UNKNOWN'}</div>
                <div class="row"><span class="label">SEC:</span> ${status}</div>
                <div class="row"><span class="label">BIO:</span> ${node.bio || 'BLANK'}</div>
                ${matchUI}
            </div>
        `;
    });
}

initSystem();

