import re 

# 01 ETER UMBIILICAL ARGYLE (3,5FR/5,0FR/8,0FR) 298,76 


def process(text):
    # Divide por linhas e remove as vazias
    linhas = [l.strip() for l in text.splitlines() if l.strip()]
    registros = []

    buffer_descricao = []
    
    # Regex para o valor: Aceita R$ (opcional), pontos de milhar e centavos
    regex_valor = r'(?:R\$\s*)?(\d{1,3}(?:\.\d{3})*,\d{2})$'

    for linha in linhas:
        # 1. Ignora se a linha for APENAS o número do índice (ex: "01." ou "02.")
        if re.match(r'^\d{1,3}\.?$', linha):
            continue

        match_valor = re.search(regex_valor, linha)

        # 2. Se a linha contém o valor (fim do item)
        if match_valor:
            valor_texto = match_valor.group(1)
            
            # Pega o texto que veio antes do valor na mesma linha
            texto_antes = re.sub(r'(?:R\$\s*)?' + re.escape(valor_texto) + r'$', '', linha).strip()
            
            # Remove pontos extras ou hífens que ficam entre o texto e o preço
            texto_antes = re.sub(r'[\.\-\s]+$', '', texto_antes).strip()
            
            # Remove o índice do início se ele estiver grudado no texto (ex: "01. CATETER")
            texto_antes = re.sub(r'^\d{1,3}\.?\s*', '', texto_antes)
            
            if texto_antes:
                buffer_descricao.append(texto_antes)

            # Se temos descrição acumulada, salvamos o registro
            if buffer_descricao:
                registros.append({
                    "Descrição": " ".join(buffer_descricao).strip(),
                    "Valor R$": valor_texto
                })

            # Reseta o balde para o próximo item
            buffer_descricao = []
            continue

        # 3. Se não é índice nem valor, é o meio da descrição
        # Remove o índice do início da linha se ele aparecer aqui também
        linha_limpa = re.sub(r'^\d{1,3}\.?\s*', '', linha)
        if linha_limpa:
            buffer_descricao.append(linha_limpa)

    return registros