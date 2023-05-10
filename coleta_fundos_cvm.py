#COLETA DE DADOS FUNDOS CVM

import pandas as pd
import requests
import zipfile
from validate_docbr import CPF, CNPJ
from datetime import date

#Tratamento de erros
def cnpj_e_valido(cnpj):
    if len(cnpj) == 14:
        validate_cnpj = CNPJ()
        return validate_cnpj.validate(cnpj)
    else:
        raise ValueError("CNPJ inválido: ", cnpj)
    
def cnpj_in_tbl(cnpj):
    if cnpj in fundos_2023.values:
        return True
    else:
        raise ValueError("CNPJ não encontrado na tabela", cnpj)   
    

#Importando ano e mes atuais
anomes_atual = date.today()
anomes_atual = str(anomes_atual).replace('-', '')[:6]

#lista meses do ano
meses_ano = []
for mes in range(1, (int(anomes_atual[4:6])+1)):
    meses_ano.append(mes)

#Novo df
fundos_2023 = pd.DataFrame()

#leitura zip(csv) internet
for mes in range(1, (len(meses_ano)+1)):
    url = f'https://dados.cvm.gov.br/dados/FI/DOC/INF_DIARIO/DADOS/inf_diario_fi_{anomes_atual[:5]}{mes}.zip'
    df = pd.read_csv(url, sep = ";", encoding= "ISO-8859-1")
    fundos_2023 = fundos_2023.append(df)



#Nome dos fundos
dados_cadastro = pd.read_csv("https://dados.cvm.gov.br/dados/FI/CAD/DADOS/cad_fi.csv", sep= ";", encoding= "ISO-8859-1")
dados_cadastro = dados_cadastro[["CNPJ_FUNDO", "DENOM_SOCIAL"]]
dados_cadastro = dados_cadastro.drop_duplicates()

dados_cadastro

fundos_2023 = fundos_2023[['DT_COMPTC', 'CNPJ_FUNDO', 'VL_QUOTA']]
fundos_2023 = fundos_2023.sort_values('DT_COMPTC', axis=0, ascending= True)


#Pesquisar fundos por CNPJ
lista_cnpj = []
pesquisa = True

while pesquisa == True:
        cnpj = str(input('Digite o CNPJ(somente números) que deseja procurar ou pressione Enter para finalizar a pesquisa: '))
        if cnpj == '':
                pesquisa = False
                print('Você não digitou nenhum mais CNPJ. Pesquisa finalizada.')
        else:
                cnpj_e_valido(cnpj)
                cnpj = CNPJ().mask(cnpj)
                cnpj_in_tbl(cnpj)
                print(cnpj)
                lista_cnpj.append(cnpj)
                

fundos_filtro = pd.DataFrame()
for cnpj in range(0, len(lista_cnpj)):
    df_pesquisa = fundos_2023.loc[fundos_2023['CNPJ_FUNDO'] == lista_cnpj[cnpj]]
    fundos_filtro = fundos_filtro.append(df_pesquisa)
       
#DF com nomes
fundos_filtro_nome = pd.merge(fundos_filtro, dados_cadastro, how='left',
                       left_on=['CNPJ_FUNDO'], right_on=['CNPJ_FUNDO'])
fundos_filtro_nome
fundo_nome = fundos_filtro_nome.drop_duplicates(['CNPJ_FUNDO'])
fundo_nome[['CNPJ_FUNDO', 'DENOM_SOCIAL']]

# #OPICIONAL
# data_atual = date.today()
# anomes = (str(data_atual).replace('-', ''))[:6]
# nome_excel = f'fundos_filtro{anomes}.xlsx'

# excel_export = fundos_filtro.copy()
# excel_export['CNPJ_FUNDO']=  excel_export['CNPJ_FUNDO'].str.replace('[.,/,-]', '')
# #Novo excel
# excel_export.to_excel(f'{nome_excel}.xlsx')