let currentData = [];
async function processText() {
    const text = document.getElementById('rawText').value;
    const type = document.getElementById('tableType').value;
    if(!text) return alert("Cole algum texto!");

    const response = await fetch('/process', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ text, type })
    });
    const result = await response.json();
    currentData = result.data;
    renderTable(currentData);
}

function renderTable(data) {
    const table = document.getElementById('previewTable');
    const area = document.getElementById('resultArea');
    if(!data || data.length === 0) return alert("Nenhum dado encontrado no padrão selecionado.");

    let html = '<thead><tr>' + Object.keys(data[0]).map(k => `<th>${k}</th>`).join('') + '</tr></thead>';
    html += '<tbody>' + data.map(row => '<tr>' + Object.values(row).map(v => `<td>${v}</td>`).join('') + '</tr>').join('') + '</tbody>';
    
    table.innerHTML = html;
    area.classList.remove('hidden');
}

async function downloadExcel() {
    const response = await fetch('/download', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ data: currentData })
    });
    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'tabela_extraida.xlsx';
    a.click();
}
