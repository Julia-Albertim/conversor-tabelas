import re

# Descrição do Material ... 12345678
#

def process(text):
    # Padrão: Pega o texto e termina quando acha um código de 8 dígitos
    pattern = r'(.*?)\s+(\d{8})(?=\s|$)'
    matches = re.findall(pattern, text, re.DOTALL)
    return [{"Descrição": m[0].strip().replace('\n', ' '), "Código": m[1]} for m in matches]