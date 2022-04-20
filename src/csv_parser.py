import pandas as pd
import json
import sys

def read_csv(arquivo, sep):
    df = pd.read_csv(
        arquivo,
        sep = sep,
        encoding = "utf-8",
        dtype = object,
    )
    return df

def write_csv(dataframe, nome_saida, sep, encoding):
    df_saida = (
            dataframe.to_csv(
                f"{nome_saida}",
            index = False,
            encoding = encoding,
            sep = sep,
            escapechar = '"',
            float_format = '%d'
            )
        )
    return df_saida

def read_json(filename):
    return json.load(open(filename))

def user_csv_output(json_file, csv_folder):
    
    json_data = []
    for i in range(len(json_file)):
        json_data.append(json_file[i]['business_discovery'])
    
    df = pd.DataFrame(json_data).drop('media', 1)
    
    return write_csv(df, f'{csv_folder}/'+sys.argv[1].split('.')[0]+'_user_data.csv', sep = ';', encoding = 'utf-8')

def media_csv_output(json_file, csv_folder):
    
    lista_postagens = []
    for i in range(len(json_file)):
        for p in range(len(json_file[i]['business_discovery']['media']['data'])):
            lista_postagens.append(json_file[i]['business_discovery']['media']['data'][p])
    
    df = pd.DataFrame(lista_postagens)
    
    return write_csv(df, f'{csv_folder}/'+sys.argv[1].split('.')[0]+'_media_data.csv', sep = ';', encoding = 'utf-8')

def get_username(nome_arquivo, coluna):
    user_df = read_csv(nome_arquivo, sep = ';')
    usernames_list = list(user_df[coluna])
    return usernames_list