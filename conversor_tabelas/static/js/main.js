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
    const rowCountSpan = document.getElementById('rowCount');
    
    if(!data || data.length === 0) return alert("Nenhum dado encontrado no padrão selecionado.");

    let html = '<thead><tr>' + Object.keys(data[0]).map(k => `<th>${k}</th>`).join('') + '</tr></thead>';
    html += '<tbody>' + data.map(row => '<tr>' + Object.values(row).map(v => `<td>${v}</td>`).join('') + '</tr>').join('') + '</tbody>';
    
    table.innerHTML = html;
    
    // Atualiza o contador de linhas (excluindo cabeçalho)
    if(rowCountSpan) {
        rowCountSpan.innerText = `Total de linhas: ${data.length}`;
    }
    
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

function copyTable() {
    const table = document.getElementById('previewTable');
    if (!table) return;

    // Seleciona apenas o tbody para copiar sem o cabeçalho
    const tbody = table.querySelector('tbody');
    if (!tbody) return;

    const range = document.createRange();
    range.selectNode(tbody);
    window.getSelection().removeAllRanges();
    window.getSelection().addRange(range);

    try {
        document.execCommand('copy');
        alert("Dados copiados para a área de transferência!");
    } catch (err) {
        alert("Erro ao copiar os dados.");
    }

    window.getSelection().removeAllRanges();
}
