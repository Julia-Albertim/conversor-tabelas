import re

 # 60033533 | Aompanhante de paciente menor de 18 anos e maior de 60 anos | R$ 100,00


import re

def process(text):
    # Regex para: Código (8 dígitos) -> Descrição (texto) -> Valor (R$)
    # m[0] = Código, m[1] = Descrição, m[2] = Valor
    pattern = r'(\d{8})\s+(.*?)\s+R\$\s*([\d\.]+,\d{2})'
    
    # re.DOTALL para pegar descrições que pulam linha
    matches = re.findall(pattern, text, re.DOTALL)
    
    results = []
    for m in matches:
        results.append({
            "Código": m[0].strip(),
            "Procedimento": m[1].strip().replace('\n', ' '),
            "Valor": f"R$ {m[2]}"
        })
        
    return results