import re


# 1.01.01.01-2  Consulta eletiva  94,75 


def process(text):
    linhas = [l.strip() for l in text.splitlines() if l.strip()]
    registros = []

    codigo_atual = None
    buffer_descricao = []

    # Regex do Código (Ex: 1.01.01.01-2)
    regex_codigo = r'(\d\.\d{2}\.\d{2}\.\d{2}-\d)'
    
    # Regex do Valor ajustada:
    # (?:R\$\s*)?  -> Procura por R$ e espaços seguidos (opcional, não captura)
    # ([\d\.]*,\d{2}) -> Captura o número com pontos e vírgula
    regex_valor = r'(?:R\$\s*)?(\d{1,3}(?:\.\d{3})*,\d{2})$'

    for linha in linhas:
        match_codigo = re.search(regex_codigo, linha)
        match_valor = re.search(regex_valor, linha)

        # 1. Identificou um código
        if match_codigo:
            codigo_atual = match_codigo.group(1)
            buffer_descricao = []
            resto_linha = linha.replace(codigo_atual, "").strip()
            if resto_linha:
                buffer_descricao.append(resto_linha)
            continue

        # 2. Identificou um valor (pode ter R$ ou não)
        if match_valor and codigo_atual:
            valor_texto = match_valor.group(1) # Aqui vem apenas o número, ex: 1.467,37
            
            # Limpa a linha de toda a parte do valor (incluindo o R$ se houver)
            # para não sobrar "sujeira" na descrição
            texto_antes_valor = re.sub(r'(?:R\$\s*)?' + re.escape(valor_texto) + r'$', '', linha).strip()
            
            if texto_antes_valor:
                buffer_descricao.append(texto_antes_valor)

            registros.append({
                "Código": codigo_atual,
                "Descrição": " ".join(buffer_descricao).replace("  ", " ").strip(),
                "Valor R$": valor_texto
            })

            codigo_atual = None
            buffer_descricao = []
            continue

        # 3. Acúmulo de descrição
        if codigo_atual:
            buffer_descricao.append(linha)

    return registros