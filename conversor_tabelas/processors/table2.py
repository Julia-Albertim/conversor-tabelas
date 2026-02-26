import re
 
# OK !!
 
# Almoço e jantar - 60033533 Acompanhante para pacientes menores de 18 ou maiores de 65 anos
# R$ 100,00
#
# 60033533 | Almoço e jantar | R$ 100,00
import re

def process(text):
    pattern = r'(\d{8})\s+(.*?)\s+(?:R\$\s*)?([\d\.]+,\d{2})'
    
    
    matches = re.findall(pattern, text, re.DOTALL)
    
    results = []
    for m in matches:
        results.append({
            "Código": m[0].strip(),
            "Procedimento": m[1].strip().replace('\n', ' '),
            "Valor": f"R$ {m[2]}" # Mantém o R$ no resultado final para a tabela
        })
        
    return results