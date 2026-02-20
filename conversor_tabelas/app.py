from flask import Flask, render_template, request, jsonify, send_file
import os
from processors import table1, table3, table4, table5, table6, table7, detector
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
    'tipo3': table3.process, 'tipo4': table4.process,
    'tipo5': table5.process, 'tipo6': table6.process,
    'tipo7': table7.process
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
