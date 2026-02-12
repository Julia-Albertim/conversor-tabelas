import re

# 01 MATERIAIS HOSPITALARES R$ 150,00

def process(text):
    # Padrão: Item, Descrição, Valor com R$
    pattern = r'^(\d+)\s+(.*?)\s+R\$\s*([\d\.]+,\d{2})$'
    data = []
    for line in text.strip().split('\n'):
        match = re.match(pattern, line.strip())
        if match:
            data.append({
                "Item": match.group(1),
                "Descrição": match.group(2).strip(),
                "Valor": f"R$ {match.group(3)}"
            })
    return data