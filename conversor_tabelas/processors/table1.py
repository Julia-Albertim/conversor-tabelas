import re


# Vídeolaparoscópio Cirúrgico 60024380 | Incluso: Gás carbônico, água destilada | R$ 3.000,12

def process(text):
    # 1. Limpa espaços extras e quebras de linha para facilitar a busca
    text_clean = " ".join(text.split())
    
    # 2. Regex Mágica:
    # (.*?)          -> Pega o Título (Vídeolaparoscópio...) no começo
    # (\b\d{8}\b)    -> Procura exatamente o Código de 8 dígitos
    # .*?            -> Pula toda a "sujeira" (Incluso: Gás, trocáteres, etc)
    # (R\$\s*[\d\.]+,\d{2}) -> Pega o Valor final com R$
    pattern = r'(.*?)\s*(\b\d{8}\b).*?(R\$\s*[\d\.]+,\d{2})'
    
    matches = re.findall(pattern, text_clean)
    
    results = []
    for m in matches:
        # m[0] = Título, m[1] = Código, m[2] = Valor
        results.append({
            "Código": m[1].strip(),
            "Descrição": m[0].strip(),
            "Valor": m[2].strip()
        })
        
    return results