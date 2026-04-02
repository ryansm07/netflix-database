#criar ambiente virtual
#separar arquivos de dados, scripts e virtual


import pandas as pd #para manipulação dos dados
import os #manipulação de diretorios operacionais
import glob #ler todos os arquivos globalmente em massa

# caminho para ler os arquivos
folder_path = 'src\\data\\raw'

#listar todos os arquivos de excel
excel_files = glob.glob(os.path.join(folder_path, '*.xlsx'))

if not excel_files:
    print ('nenhum arquivo encontrado')
else:

    #dataframe
    dfs = []

    for excel_file in excel_files:
        
        try:
            #salvar todos os arquivos de excel em um array
            df_temp = pd.read_excel(excel_file)

            #pegar o nome do arquivo
            file_name = os.path.basename(excel_file)

            #criação da nova coluna com o nome do arquivo
            df_temp['filename'] = file_name

            #criação da nova coluna location
            if 'brasil' in file_name.lower():
                df_temp['location'] = 'br'
            elif 'france' in file_name.lower():
                df_temp['location'] = 'fr'
            elif 'italian' in file_name.lower():
                df_temp['location'] = 'it'


            #criação da nova coluna campanha
            df_temp['campaign'] = df_temp['utm_link'].str.extract(r'utm_campaign=(.*)')

            #guarda os dados tratados para um dataframe comum
            dfs.append(df_temp)

        
        except Exception as e:
            print (f"Erro ao ler o arquivo {excel_file} : {e}")

if dfs: #verifica se não está vazia a tabela

    #concatena todas as tabelas salvas em uma unica tabela
    result = pd.concat(dfs, ignore_index=True)

    #caminho de saida
    output_file = os.path.join('src', 'data', 'ready', 'clean.xlsx')

    #configura o motor de escrita
    writer = pd.ExcelWriter(output_file, engine='xlsxwriter')

    #leva os dados do resultados para serem escritos no motor de excel configurado
    result.to_excel(writer, index=False)

    #salva o arquivo de excel
    writer._save()

else: print('nenhum dado para ser salvo')