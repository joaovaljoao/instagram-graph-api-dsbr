# instagram-graph-api-dsbr
Código para extração de metadados das redes das IFES.

# Setup inicial

1. Crie um arquivo .env na raiz do projeto com as variáveis de ambiente. Exemplo:
```shell
CLIENT_ID="123456789"
CLIENT_SECRET="fsdfsdfsdfsadferrwewerwerwerwerew"
INPUT_TOKEN= "fsdfsdfsdfsdfsdfsdfsdfsdfsdfsdfsdf"
GRAPH_DOMAIN="https://graph.facebook.com/"
VERSION="v11.0"
FACEBOOK_ID="123456789"
GRANT_TYPE="fb_exchange_token"
```

2. Crie um ambiente virtual:
```shell
python3 -m venv venv
source venv/bin/activate
```

3. Verifique o funcionamento rodando os testes da aplicação:
```shell
source venv/bin/activate
pytest
```

# Execução do código

1. Ative o ambiente virtual
```shell
source venv/bin/activate
```

2. Execute o programa principal passando como parâmetro o nome do arquivo de saída:
```shell
python3 src/main.py output.csv
```

Lembre-se que existe um limite para apenas duas chamadas no main.py.