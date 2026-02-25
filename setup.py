import os
import zipfile

# Estrutura de arquivos e conteúdos
project_name = "conversor_tabelas"
files = {
    "requirements.txt": "flask\npandas\nopenpyxl",
    
    "README.md": """# Conversor de Tabelas Hospitalares
Aplicação local para conversão de textos não estruturados em Excel.

## Como usar:
1. Instale as dependências: `pip install -r requirements.txt`
2. Inicie a aplicação: `python app.py`
3. Acesse no navegador: `http://localhost:5000`

## Estrutura:
- `processors/`: Lógica de extração (Regex/Texto).
- `services/`: Geração de arquivos Excel.
- `static/`: Interface visual (CSS/JS).
""",

    "app.py": """from flask import Flask, render_template, request, jsonify, send_file
import os
from processors import table1, table2, table3, table4, detector
from services import excel_service

app = Flask(__name__)
OUTPUT_FOLDER = 'output'
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_data():
    content = request.json
    text = content.get('text', '')
    table_type = content.get('type', 'auto')

    if table_type == 'auto':
        table_type = detector.identify(text)

    processors = {
        'tipo1': table1.process, 'tipo2': table2.process,
        'tipo3': table3.process, 'tipo4': table4.process
    }

    process_func = processors.get(table_type)
    if not process_func:
        return jsonify({"error": "Tipo de tabela inválido"}), 400

    data = process_func(text)
    return jsonify({"type": table_type, "data": data})

@app.route('/download', methods=['POST'])
def download_excel():
    data = request.json.get('data')
    filepath = os.path.join(OUTPUT_FOLDER, 'tabela_exportada.xlsx')
    excel_service.save_to_excel(data, filepath)
    return send_file(filepath, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
""",

    "processors/__init__.py": "",
    
    "processors/detector.py": """def identify(text):
    if "R$" in text:
        return 'tipo2' if any(len(w) >= 6 and w.isdigit() for w in text.split()) else 'tipo4'
    return 'tipo1'
""",

    "processors/table1.py": """import re
def process(text):
    # Regex: Item (digito) | Descrição | Valor (0,00)
    pattern = r'^(\\d+)\\s+(.*?)\\s+(\\d+,\\d{2})$'
    data = []
    for line in text.strip().split('\\n'):
        match = re.match(pattern, line.strip())
        if match:
            data.append({"Item": match.group(1), "Descrição": match.group(2), "Valor": match.group(3)})
    return data
""",

    "processors/table2.py": """import re
def process(text):
    # Simulação da lógica do txt_excl2.py (Código 6-8 digitos + R$)
    pattern = r'(\\d{6,8})\\s+(.*?)\\s+R\\$\\s*(\\d+,\\d{2})'
    matches = re.findall(pattern, text, re.DOTALL)
    return [{"Código": m[0], "Procedimento": m[1].strip(), "Valor": m[2]} for m in matches]
""",

    "processors/table3.py": """import re
def process(text):
    # Código (8 dígitos) | Descrição (sem valor)
    pattern = r'(\\d{8})\\s+(.*?)(?=\\d{8}|$)'
    matches = re.findall(pattern, text, re.DOTALL)
    return [{"Código": m[0], "Descrição": m[1].strip()} for m in matches]
""",

    "processors/table4.py": """import re
def process(text):
    # Item numérico | Descrição | Valor com R$
    pattern = r'^(\\d+)\\s+(.*?)\\s+R\\$\\s*(\\d+,\\d{2})$'
    data = []
    for line in text.strip().split('\\n'):
        match = re.match(pattern, line.strip())
        if match:
            data.append({"Item": match.group(1), "Descrição": match.group(2), "Valor": match.group(3)})
    return data
""",

    "services/excel_service.py": """import pandas as pd
def save_to_excel(data, filepath):
    df = pd.DataFrame(data)
    df.to_excel(filepath, index=False)
""",

    "templates/index.html": """<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Conversor Hospitalar</title>
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
    <div class="container">
        <header>
            <h1>📄 Conversor de Tabelas</h1>
            <p>Transforme textos brutos em arquivos Excel estruturados</p>
        </header>
        
        <textarea id="rawText" placeholder="Cole o texto do PDF ou sistema aqui..."></textarea>
        
        <div class="controls">
            <select id="tableType">
                <option value="auto">Detecção Automática</option>
                <option value="tipo1">Tipo 1 (Item/Desc/Valor)</option>
                <option value="tipo2">Tipo 2 (Código/Proc/R$)</option>
                <option value="tipo3">Tipo 3 (Código/Desc)</option>
                <option value="tipo4">Tipo 4 (Item/Desc/R$)</option>
            </select>
            <button onclick="processText()" class="btn-primary">Processar Dados</button>
        </div>

        <div id="resultArea" class="hidden">
            <div class="table-header">
                <h3>Pré-visualização</h3>
                <button onclick="downloadExcel()" class="btn-success">📥 Baixar Excel</button>
            </div>
            <div class="table-wrapper">
                <table id="previewTable"></table>
            </div>
        </div>
    </div>
    <script src="/static/js/main.js"></script>
</body>
</html>
""",

    "static/css/style.css": """body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f4f7f6; color: #333; margin: 0; padding: 20px; }
.container { max-width: 1000px; margin: 0 auto; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); }
header { text-align: center; margin-bottom: 30px; }
textarea { width: 100%; height: 200px; padding: 15px; border: 2px solid #ddd; border-radius: 8px; resize: vertical; box-sizing: border-box; }
.controls { display: flex; gap: 15px; margin: 20px 0; }
select, button { padding: 12px 20px; border-radius: 6px; border: 1px solid #ddd; cursor: pointer; }
.btn-primary { background: #007bff; color: white; border: none; flex-grow: 1; font-weight: bold; }
.btn-success { background: #28a745; color: white; border: none; font-weight: bold; }
.hidden { display: none; }
.table-wrapper { overflow-x: auto; margin-top: 20px; border: 1px solid #eee; }
table { width: 100%; border-collapse: collapse; }
th, td { padding: 12px; text-align: left; border-bottom: 1px solid #eee; }
th { background: #f8f9fa; }
""",

    "static/js/main.js": """let currentData = [];
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
"""
}

# Criar pastas e arquivos
print("Iniciando criação do projeto...")
for path, content in files.items():
    full_path = os.path.join(project_name, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Criado: {path}")

# Criar ZIP
zip_name = "projeto_conversor.zip"
with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files_in_dir in os.walk(project_name):
        for file in files_in_dir:
            zipf.write(os.path.join(root, file), 
                       os.path.relpath(os.path.join(root, file), os.path.join(project_name, '..')))

print(f"\\n✅ Sucesso! Projeto criado na pasta '{project_name}'.")
print(f"📦 Arquivo '{zip_name}' gerado.")