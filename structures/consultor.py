import pandas as pd
from dataframes.objects import dataframe_geral, meses

class Consultor:

    def __init__(self, name):

        self.name = name
        self.__dataframe__ = dataframe_geral[
            (dataframe_geral['CONSULTOR'] == name)
        ]

        self.__add_static_values__()
        self.__formatar_nomes__()

    def __formatar_nomes__(self) -> None:

        # Função para formatar o nome dos consultores 
        def formatar_nome(nome):
            try:
                nome_splited = nome.split(' ')
                if nome_splited[1] == 'DE' or nome_splited[1] == 'DOS':
                    nome = nome_splited[0] + ' ' + nome_splited[1] + ' ' + nome_splited[2]
                else:
                    nome = nome_splited[0] + ' ' + nome_splited[1]
            except:
                pass

            return nome
        
        self.__dataframe__['CONSULTOR'] = self.__dataframe__['CONSULTOR'].apply(lambda nome: formatar_nome(nome))

    @property
    def dias_trabalhados(self) -> int:
        """
            Retorna quantos dias determinado consultor trabalhou aproximadamente. Valor é utilizado como
            métrica para o cálculo de certas médias

        """

        dataframe = self.__dataframe__

        # Concatena as colunas ``MÊS`` e ``ANO`` em uma única
        dataframe['DATA'] = dataframe['MÊS'] + '/' + dataframe['ANO']

        meses_trabalhados = list(dataframe['DATA'].unique())

        # Soma a quantidade de meses tabalhados com a quantidade de dias úteis de um mês
        dias_trabalhados = len(meses_trabalhados) * 22

        return dias_trabalhados

    def __add_static_values__(self) -> None:
        """
            Adiciona vendas estáticas ao dataframe de determinado consultor.
            A função foi criada para ajudar na plotagem dos gráficos, fazendo com 
            que fique visível os meses cujo consultor não tenha vendido produtos.
        """

        # Retorna o último ano que o consultor realizou uma venda.
        ultimo_ano = max(self.years)

        for mes in meses:
            static = pd.DataFrame({
                'UF': [None],
                'CNPJ': [None],
                'MÊS': [mes],
                'ANO': [ultimo_ano],
                'PLANO': [None],
                'TIPO': [None],
                'VALOR DO PLANO': [0],
                'QUANTIDADE DE PRODUTOS': [0],
                'VALOR ACUMULADO': [0],
                'CONSULTOR': [None],
                'GESTOR': [None],
                'REVENDA': [None],
                'CNAE': [None],
                'FATURAMENTO': [None],
                'COLABORADORES': [None]
            })

            # Concatena o dataframe original com o dataframe estático.
            self.__dataframe__ = pd.concat([static, self.__dataframe__])

    def __get_receita_ou_quantidade__(self, retorno, ano: int = None, mes: str = None) -> int:

        """
            Função privada para retornar a soma de certas colunas do dataframe.
            Irá somar todos os valores da coluna ``<retorno>``

            Parâmetros
            ---------

            retorno: str

                A coluna que deseja somar os valores. Deve ser ``VALOR ACUMULADO``ou 
                ``QUANTIDADE DE PRODUTOS`` 

            ano: int | None

                Filtra o dataframe por ano

            mes: str | None

                Filtra o dataframe por mês

        """

        dataframe = self.__dataframe__

        if ano:
            dataframe = dataframe[
                (dataframe['ANO'] == ano)
            ]
        
        if ano and mes:
            dataframe = dataframe[
                (dataframe['ANO'] == ano) &
                (dataframe['MÊS'] == mes)
            ]
            
        receita_total = dataframe[retorno].sum()

        return receita_total
    
    def __get_media_mensal_receita_ou_quantidade__(self, retorno) -> int:

        """
            Função privada para retornar a média mensal da receita ou quantidade vendida 
            por determinado consultor

            Parâmetros 
            ----------

            retorno: str

                O nome da coluna que deseja retornar a média, deve ser 
                ``RECEITA`` ou ``QUANTIDADE``

        """

        quantidade_ou_receita = ''

        if retorno == 'RECEITA':
            quantidade_ou_receita = self.receita()

        if retorno == 'QUANTIDADE':
            quantidade_ou_receita = self.quantidade()

        media_mensal = quantidade_ou_receita / len(meses)

        return int(media_mensal)

    @property
    def years(self) -> list:
        """
            Retorna em formato de lista todos os anos em que 
            determinado consultor concluiu vendas.
        """
        years = list(self.__dataframe__['ANO'].unique())

        return years
    
    def receita(self, ano: int = None, mes: str = None) -> int:

        """
            Retorna a receita total vendida pelo consultor

            Parâmetros
            ----------

            ano: int

                Parâmetro opcional, caso informado, irá retornar a
                receita total daquele ano
            
            mes: string

                Parâmetro opcional, caso informado, irá retornar a receita
                total daquele mês. Deve informar o ano caso utilize-o.
        """
            
        receita_total = self.__get_receita_ou_quantidade__(
            'VALOR ACUMULADO', ano, mes
        )

        return receita_total

    def quantidade(self, ano: int = None, mes: str = None) -> int:

        """
            Retorna a quantidade de produtos vendida pelo consultor

            Parâmetros
            ----------

            ano: int

                Parâmetro opcional, caso informado, irá retornar a
                quantidade total daquele ano
            
            mes: string

                Parâmetro opcional, caso informado, irá retornar a quantidade
                total daquele mês. Deve informar o ano caso utilize-o.
        """
            
        quantidade_total = self.__get_receita_ou_quantidade__(
            'QUANTIDADE DE PRODUTOS', ano, mes
        )

        return quantidade_total
    
    @property
    def ticket_medio(self) -> int:

        """
            Retorna o ticket médio de vendas de determinado consultor

            Cálculo utilizado
            -------

            ``receita_total / quantidade_de_vendas ``
        """

        receita_total = self.receita()
        quantidade_de_vendas = self.__dataframe__.shape[0]

        ticket_medio = receita_total / quantidade_de_vendas

        return ticket_medio
    
    @property
    def receita_media_mensal(self) -> int:

        """
            Retorna a média de vendas mensal de determinado consultor

            Cálculo utilizado
            -------

            ``receita_total / (anos * 12)
        """

        receita_media_mensal = self.__get_media_mensal_receita_ou_quantidade__('RECEITA')

        return receita_media_mensal
    
    @property
    def quantidade_media_mensal(self) -> int:

        """
            Retorna a média da quantidade de vendas mensal de determinado consultor

            Cálculo utilizado
            -------

            ``quantidade_total / (anos * 12)
        """

        quantidade_media_mensal = self.__get_media_mensal_receita_ou_quantidade__('QUANTIDADE')

        return quantidade_media_mensal
    
    def __get_delta_receita_ou_quantidade_mensal__(self, ano: int, mes: str, key: str) -> int:

        """
            Função privada, retorna o valor do parâmetro ``delta`` para a função ``col.metric`` do streamlit

            O ``delta_receita_ou_quantidade_mensal`` é a diferença entre a receita ou quantidade de vendas 
            do mês referência  comparado com a receita ou quantidade do mês passado.

            Parâmetros
            ---------

            ano : int
            
                O ano atual que servirá como referência para o ``delta``

            mes : str

                O mês atual que servirá como referência para o ``delta`` 
            
            key : str

                O nome da coluna que deseja calcular o delta. Deve ser ``RECEITA`` ou ``QUANTIDADE``

        """

        media_atual, media_mes_passado = '', ''

        # Retorna o primeiro ano que o consultor realizou uma venda
        primeiro_ano = min(self.years)

        # A função irá retornar 0 caso não haja venda anterior à do mês e ano referência.
        if ano == primeiro_ano and mes == 'Janeiro':
            return 0 
        
        # Se o mês referência for o mês de ``Janeiro``, então o ano referência será o ano passado.
        ano_delta = ano - 1 if mes == 'Janeiro' else ano

        index_mes_passado = meses.index(mes) - 1
        mes_delta = meses[index_mes_passado]

        if key == 'RECEITA':
            media_atual = self.receita(ano = ano, mes = mes)
            media_mes_passado = self.receita(ano_delta, mes_delta)
        
        elif key == 'QUANTIDADE':
            media_atual = self.quantidade(ano = ano, mes = mes)
            media_mes_passado = self.quantidade(ano_delta, mes_delta)

        else:
            raise ValueError('O valor do parâmetro key deve ser RECEITA OU QUANTIDADE')


        return media_atual - media_mes_passado
    
    def delta_receita_mensal(self, ano: int, mes: str) -> int:
        """
            Retorna o valor do parâmetro ``delta`` para a função ``col.metric`` do streamlit

            O ``delta_receita_mensal`` é a diferença entre a receita do mês referência 
            comparado com a receita do mês passado.

            Parâmetros
            ---------

            ano : int
            
                O ano atual que servirá como referência para o ``delta``

            mes : str

                O mês atual que servirá como referência para o ``delta`` 
        """

        delta_receita_mensal = self.__get_delta_receita_ou_quantidade_mensal__(ano, mes, 'RECEITA')

        return delta_receita_mensal
    
    def delta_quantidade_mensal(self, ano: int, mes: str) -> int:
        """
            Retorna o valor do parâmetro ``delta`` para a função ``col.metric`` do streamlit

            O ``delta_receita_mensal`` é a diferença entre a quantidade de vendas do mês referência 
            comparado com a quantidade de vendas do mês passado.

            Parâmetros
            ---------

            ano : int
            
                O ano atual que servirá como referência para o ``delta``

            mes : str

                O mês atual que servirá como referência para o ``delta`` 
        """

        delta_quantidade_mensal = self.__get_delta_receita_ou_quantidade_mensal__(ano, mes, 'QUANTIDADE')

        return delta_quantidade_mensal
    
    def __get_media_receita_ou_quantidade_diaria__(self, key: str, ano: int = None, mes: str = None) -> int:

        """
            Função privada que retorna a média da receita ou quantidade de produtos vendidos 
            diariamente de um determinado consultor 

            Parâmetros
            ---------

            key : str

                Se você deseja calcular a Receita ou Quantidade. Parâmetro deve ser ``RECEITA`` ou
                ``QUANTIDADE``

            ano : int | None

                O ano que você deseja ver a média. 
            
            mes : int | None

                O mês que você deseja ver a média.

            Cálculo Utilizado
            ---------

            ``receita_ou_quantidade_total`` / ``dias_trabalhados``
        """

        if ano and mes:
            dataframe = self.__dataframe__[
                (self.__dataframe__['ANO'] == ano) & 
                (self.__dataframe__['MÊS'] == mes)
            ]

        if key == 'RECEITA':
            key = 'VALOR ACUMULADO'
        
        elif key == 'QUANTIDADE':
            key = 'QUANTIDADE DE PRODUTOS'
        
        else:
            raise ValueError('O valor do parâmetro key deve ser RECEITA OU QUANTIDADE')

        receita_ou_quantidade_total = dataframe[key].sum()
        dias_trabalhados = self.dias_trabalhados

        media_diaria = receita_ou_quantidade_total / dias_trabalhados

        return media_diaria
    
    def media_receita_diaria(self, ano: int = None, mes: str = None) -> int:

        """
            Retorna a média da receita total diária de um determinado consultor 

            Parâmetros
            ---------

            ano : int | None

                O ano que você deseja ver a média. 
            
            mes : int | None

                O mês que você deseja ver a média.

            Cálculo Utilizado
            ---------

            ``receita_total`` / ``dias_trabalhados``
        """

        receita_media_diaria = self.__get_media_receita_ou_quantidade_diaria__(
            self, 'RECEITA', ano, mes
        )

        return receita_media_diaria
    
    def media_quantidade_diaria(self, ano: int = None, mes: str = None) -> int:

        """
            Retorna a média da quantidade de produtos vendidos diariamente de um determinado consultor 

            Parâmetros
            ---------

            ano : int | None

                O ano que você deseja ver a média. 
            
            mes : int | None

                O mês que você deseja ver a média.

            Cálculo Utilizado
            ---------

            ``quantidade_total`` / ``dias_trabalhados``
        """

        quantidade_media_diaria = self.__get_media_receita_ou_quantidade_diaria__(
            self, 'QUANTIDADE', ano, mes
        )

        return quantidade_media_diaria
    
    def group_by_meses(self, ano: int) -> pd.DataFrame:

        """
            Agrupa o total de vendas de cada mês realizadas por um determinado consultor

            Parâmetros
            ------

            ano : int

                O ano que você deseja analizar 
        """
        meses_numeros = {
            'Janeiro': 1,
            'Fevereiro': 2,
            'Março': 3,
            'Abril': 4,
            'Maio': 5,
            'Junho': 6,
            'Julho': 7,
            'Agosto': 8,
            'Setembro': 9,
            'Outubro': 10,
            'Novembro': 11,
            'Dezembro': 12
        }

        dataframe = self.__dataframe__[
            (self.__dataframe__['ANO'] == ano)
        ]

        dataframe_grouped = dataframe.groupby('MÊS').sum(numeric_only = True)

        # Transforma o index do dataframe em coluna, dessa forma é possível colocar a coluna MÊS em ordem.
        vendas_mensais_T = dataframe_grouped.T
        columns = list(vendas_mensais_T.columns)
        
        meses = sorted(columns, key=lambda x: meses_numeros[x])

        vendas_mensais = vendas_mensais_T[meses].T.reset_index()

        return vendas_mensais
    
    def group_by_ano(self) -> pd.DataFrame:

        """
            Agrupa o total de vendas de cada ano realizadas por um determinado consultor

        """

        dataframe_grouped = self.__dataframe__.groupby('ANO', as_index = False).sum(numeric_only = True)
        vendas_anuais = dataframe_grouped.sort_values(by = 'ANO', ascending = True)

        return vendas_anuais