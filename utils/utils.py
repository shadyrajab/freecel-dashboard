def formatar_cnpj(cnpj):
    cnpj = cnpj.zfill(14)

    cnpj_formatado = '{}.{}.{}/{}-{}'.format(cnpj[:2], cnpj[2:5], cnpj[5:8], cnpj[8:12], cnpj[12:])
    return cnpj_formatado

def formatar_telefone(telefone):
    telefone = telefone.replace('.0','')
    return telefone

def remover_ponto(string):
    string = string.replace('.', '')
    return string