import re

# 1 ABSORVENTE HOSPITALAR PACOTE - UNIDADE R$ 0,97

def process(text):
    # Padrão: Texto seguido de R$ e o valor
    pattern = r'(.*?)\s+R\$\s*([\d\.]+,\d{2})'
    matches = re.findall(pattern, text)
    return [{"Procedimento": m[0].strip().replace('.', ''), "Valor": f"R$ {m[1]}"} for m in matches]