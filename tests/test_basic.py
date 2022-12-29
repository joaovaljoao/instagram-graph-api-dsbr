'''
Testes básicos do repositório

Importação de bibliotecas, acesso aos arquivos, existência de arquivos
de configuração, criação de objetos com tipos de dados corretos, etc.
'''


def test_first_one():
    assert True
    
def test_import_scripts():
    '''
    Testa a importação dos scripts do repositório dentro do diretório tests src
    '''
    try:
        from src import business_data
        from src import facebook_creds
        from src import image_downloader
        from src import image_resizer
        # from src import main #TODO: Fix relative import
        assert True
    except Exception as e:
        assert False

def test_loggin_folder():
    '''
    Testa a existência do diretório logging
    '''
    from src.business_data import loggin_setup
    loggin_setup()
    import os
    assert os.path.exists('logging')

def test_image_folder():
    '''
    Testa a existência do diretório images
    '''
    from src.image_downloader import create_image_folder
    create_image_folder()
    import os
    assert os.path.exists('pub')
    assert os.path.exists('pub/images')
    
def test_env_file():
    '''
    Testa a existência do arquivo .env
    '''
    import os
    assert os.path.exists('.env')
    
def test_env_file_contet():
    '''
    Testa a existência do arquivo .env com os parâmetros de configuração
    '''
    import os
    import dotenv
    dotenv.load_dotenv()
    assert int(os.getenv('CLIENT_ID')) > 10
    assert len(os.getenv('CLIENT_SECRET')) > 10
    assert len(os.getenv('INPUT_TOKEN')) > 10
    assert len(os.getenv('GRAPH_DOMAIN')) > 10
    assert len(os.getenv('FACEBOOK_ID')) > 10
    assert len(os.getenv('GRANT_TYPE')) > 10
    assert len(os.getenv('FACEBOOK_ID')) > 10