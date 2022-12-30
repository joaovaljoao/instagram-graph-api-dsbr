import requests
import os
from dotenv import load_dotenv, set_key
from datetime import datetime, timedelta

class Facebook:
    """Classe para interagir com a API do Facebook."""

    def __init__(self):
        """Inicializa um objeto da classe Facebook.

        Carrega as variáveis de ambiente a partir do arquivo .env e define os atributos do objeto com base nessas
        variáveis.
        """
        # Carrega as variáveis de ambiente a partir do arquivo .env
        load_dotenv()

        # Define os atributos do objeto a partir das variáveis de ambiente
        self.input_token = os.getenv('INPUT_TOKEN')
        self.long_lived_token = os.getenv('LONG_LIVED_TOKEN')
        self.grant_type = os.getenv('GRANT_TYPE')
        self.client_secret = os.getenv('CLIENT_SECRET')
        self.client_id = os.getenv('CLIENT_ID')
        self.graph_domain = os.getenv('GRAPH_DOMAIN')
        self.version = os.getenv('VERSION')
        self.facebook_id = os.getenv('FACEBOOK_ID')
        self.endpoint = f"{self.graph_domain}{self.version}/{self.facebook_id}"

    def refresh_long_lived_token(self):
        """Atualiza o token de longa duração.

        Faz uma solicitação à API do Facebook para trocar o token de entrada pelo token de longa duração e atualiza as
        variáveis LONG_LIVED_TOKEN e EXPIRES_IN no arquivo .env com os novos valores. Em seguida, carrega novamente as
        variáveis de ambiente do arquivo .env e atualiza o atributo LONG_LIVED_TOKEN do objeto.

        Returns:
            str: O token de longa duração atualizado.
        """
        # Faz uma solicitação à API do Facebook para trocar o token de entrada pelo token de longa duração
        params = (
            ('grant_type', self.grant_type),
            ('client_secret', self.client_secret),
            ('client_id', self.client_id),
            ('fb_exchange_token', self.input_token),
        )
        response = requests.get(f"{self.graph_domain}{self.version}/oauth/access_token", params = params)
        print(response.content)
        long_lived_token = response.json()['access_token']
        expires_in = response.json()['expires_in']
        load_dotenv()

        # Escreve atualizando as variáveis LONG_LIVED_TOKEN e EXPIRES_IN no arquivo .env usando dotenv.set_key
        set_key(dotenv_path='.env', key_to_set='LONG_LIVED_TOKEN', value_to_set=long_lived_token)
        set_key(dotenv_path='.env', key_to_set='EXPIRES_IN', value_to_set=expires_in)

        # Update LONG_LIVED_TOKEN and EXPIRES_IN variables in .env file
        with open('.env', 'r') as f:
            lines = f.readlines()
        with open('.env', 'w') as f:
            for line in lines:
                if line.startswith('LONG_LIVED_TOKEN'):
                    f.write('LONG_LIVED_TOKEN=' + long_lived_token + '\n')
                elif line.startswith('EXPIRES_IN'):
                    f.write('EXPIRES_IN=' + expires_in + '\n')
                else:
                    f.write(line)
        
        # Update LONG_LIVED_TOKEN attribute of object
        self.long_lived_token = long_lived_token
            
        return long_lived_token

    def debug_token(self, token):
        """Obtém informações de depuração sobre um token.

        Args:
            token (str): O token para o qual obter informações de depuração.

        Returns:
            dict: As informações de depuração do token.
        """
        params = (
            ('input_token', token),
            ('access_token', self.client_id + '|' + self.client_secret),
        )
        return requests.get(f"{self.graph_domain}{self.version}/debug_token", params=params).json()

    def is_token_expiring(self, expiration_threshold_seconds=604800):
        """Verifica se o token atual está prestes a expirar.

        Args:
            expiration_threshold_seconds (int, optional): O número de segundos antes da expiração do token em que deve
                ser atualizado. Padrão é 604800 (1 semana).

        Returns:
            bool: Verdadeiro se o token está prestes a expirar, senão falso.
        """
        # Verifica se a variável LONG_LIVED_TOKEN está definida no ambiente
        if 'LONG_LIVED_TOKEN' in os.environ:
            # Usa LONG_LIVED_TOKEN
            token = os.environ['LONG_LIVED_TOKEN']
        else:
            # Gera o LONG_LIVED_TOKEN usando o INPUT_TOKEN
            self.refresh_long_lived_token()
            token = self.long_lived_token

        # Obtém a hora de expiração do token
        token_info = self.debug_token(token)['data']
        expiration_time = datetime.fromtimestamp(token_info['expires_at'])

        # Compara a hora de expiração com a hora atual e o limiar de expiração
        now = datetime.now()
        expiration_threshold = timedelta(seconds=expiration_threshold_seconds)
        if expiration_time < now + expiration_threshold:
            # Atualiza o token
            self.refresh_long_lived_token()
