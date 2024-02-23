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

years = ['Todos', 2024, 2023, 2022]
meses_numeros = {
    1: "Janeiro",
    2: "Fevereiro",
    3: "Março",
    4: "Abril",
    5: "maio",
    6: "junho",
    7: "julho",
    8: "agosto",
    9: "setembro",
    10: "Outubro",
    11: "Novembro",
    12: "Dezembro"
}

months = [
    'Todos',
    'Janeiro', 
    'Fevereiro', 
    'Março', 
    'Abril',
    'Maio', 
    'Junho',
    'Julho',
    'Agosto',
    'Setembro',
    'Outubro',
    'Novembro',
    'Dezembro'
]