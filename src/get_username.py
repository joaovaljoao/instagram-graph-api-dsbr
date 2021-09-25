from csv_parser import read_csv

def get_username(nome_arquivo):
    user_df = read_csv(nome_arquivo, sep = ';')
    usernames_list = list(user_df['username'])
    return usernames_list

