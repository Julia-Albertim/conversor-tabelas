import re

# 10101012 CONSULTA CLÍNICA MÉDICA 94,75

def process(text):
    linhas = [l.strip() for l in text.splitlines() if l.strip()]
    registros = []

    buffer_nome = []
    codigo_atual = None

    for linha in linhas:
        match_codigo = re.search(r'\b(\d{8})\b', linha)
        match_valor = re.search(r'(\d+,\d{2})$', linha)

        # Se encontrou código
        if match_codigo:
            codigo_atual = match_codigo.group(1)
            linha_sem_codigo = linha.replace(codigo_atual, "").strip()

            # Se também tiver valor na mesma linha
            if match_valor:
                valor_texto = match_valor.group(1)
                descricao = linha_sem_codigo.replace(valor_texto, "").strip()

                registros.append({
                    "Código": codigo_atual,
                    "Descrição": descricao,
                    "Valor": f"R$ {valor_texto}"
                })

                codigo_atual = None
                buffer_nome = []
                continue
            else:
                # Não tem valor ainda, começa buffer
                if linha_sem_codigo:
                    buffer_nome.append(linha_sem_codigo)
                continue

        # Se encontrou valor (em outra linha)
        if match_valor and codigo_atual:
            valor_texto = match_valor.group(1)
            parte_nome_final = linha[:linha.rfind(valor_texto)].strip()
            if parte_nome_final:
                buffer_nome.append(parte_nome_final)

            registros.append({
                "Código": codigo_atual,
                "Descrição": " ".join(buffer_nome).strip(),
                "Valor": f"R$ {valor_texto}"
            })

            buffer_nome = []
            codigo_atual = None
            continue

        # Continuação de descrição
        if codigo_atual:
            buffer_nome.append(linha)

    return registros