import re

# 40601293 PROCEDIMENTO DIAGNÓSTICO POR CAPTURA HÍBRIDA

def process(text):
    # Padrão: Código de 8 dígitos seguido de texto até o próximo código ou fim da página
    pattern = r'(\d{8})\s+(.*?)(?=\d{8}|$)'
    
    matches = re.findall(pattern, text, re.DOTALL)
    results = []
    for m in matches:
        results.append({
            "Código": m[0],
            "Descrição": m[1].strip().replace('\n', ' ')
        })
    return results