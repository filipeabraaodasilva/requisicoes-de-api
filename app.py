# IMPORTANDO BIBLIOTECAS DE TERCEIROS
from tqdm import tqdm
import requests as rq
import json as js



# MÉTODO PARA AUTÊNTICAÇÃO
class Autenticacao:
    def __init__(self, usuario: str, senha: str) -> None:
        
        #DADOS PARA EXECUÇÃO DA REQUISIÇÃO
        self.__url: str = "https://url_api.com/login"
        
        self.__cabecalho: dict = {
            'Content-Type': 'application/json; charset=UTF-8',
            'user-agent': 'RequisicaoWeb'
        }
        
        self.__dados_post: dict = {
            "username": "{}".format(usuario),
            "password": "{}".format(senha),
            "tempoExpiracao": 0,
            "utilizacaoUnica": True
        }
    
        self.__requisicao = rq.post(url=self.__url, headers=self.__cabecalho, json=self.__dados_post)
        
    # GETs PARA OBTER INFORMAÇÕES DA REQUISIÇÃO
    @property
    def get_resultado(self) -> str:
        return self.__requisicao.text
        
    @property
    def get_json(self) -> dict:
        return self.__requisicao.json()
        
    @property
    def get_token(self) -> str:
        return self.get_json["Token"]



class PostUsuario:
    def __init__(self, bearer_token: str, login: str, nome: str, email: str, senha: str, id_cliente: str, id_unidade: str) -> None:
    
        # DADOS PARA EXECUÇÃO DA REQUISIÇÃO
        self.__url: str = "https://url_api.com/novo_usuario"
        
        self.__cabecalho: dict = {
            'Authorization': f'Bearer {bearer_token}',
            'Content-Type': 'application/json; charset=UTF-8',
            'user-agent': 'RequisicaoWeb' 
        }
        
        self.__dados_post: dict = {
            "login": "{}".format(login),
            "nome": "{}".format(nome),
            "email": "{}".format(email),
            "senha": "{}".format(senha),
            "telefoneFixo": "",
            "telefoneCelular": "",
            "idChefe": "",
            "registrosPorPagina": "10",
            "alteraSenhaProximoLogin": "1",
            "frequenciaTrocaSenha": "",
            "dataAgendamentoInativacao": "",
            "idHorarioTrabalho": "",
            "idCultura": "1",
            "idCalendario": "",
            "notificacaoTTD": "0",
            "clienteMaster": "0",
            "idGrupoChefeImediato": "",
            "idClientePermissao": "{}".format(id_cliente),
            "idUnidadePermissao": "{}".format(id_unidade)
        }
        
        self.__requisicao = rq.post(url=self.__url, headers=self.__cabecalho, json=self.__dados_post)
        
    # GETs PARA OBTER INFORMAÇÕES DA REQUISIÇÃO        
    @property
    def get_json(self) -> dict:
        return self.__requisicao.json()
        
    @property
    def get_status(self) -> int:
        return self.__requisicao.status_code
        
    @property
    def get_texto_resposta(self) -> str:
        return self.__requisicao.text
        


# APLICAÇÃO ########################################################################################

# VARIÁVEIS A SEREM DEFINIDAS PELO USUARIO
USUARIO_API: str = "usuario"
SENHA_API: str = "senha"
ID_CLIENTE: str = "primeiro_parametro"
ID_UNIDADE: str = "segundo_parametro"

auth = Autenticacao(USUARIO_API, SENHA_API)
bearer_token: str = auth.get_token

pasta_de_trabalho: str = input("INFORME A PASTA DE TRABALHO: ")
print("\n")

# ABRINDO ARQUIVO TXT CONTENDO AS INFORMAÇÕES NECESSÁRIAS
with open(pasta_de_trabalho + "\\lista_de_usuarios.txt", "r", encoding="utf-8") as lista_de_usuarios:

    # CONTANDO A QUANTIDADE TOTAL DE LINHAS NO ARQUIVO PARA MONTAR A BARRA DE PROGRESSO
    total_de_usuarios: int = sum(1 for usuario in lista_de_usuarios)
    lista_de_usuarios.seek(0)
    
    contador = 1
    contador_de_sucesso = 0
    contador_de_insucesso = 0
    
    for usuario in tqdm(lista_de_usuarios, total = total_de_usuarios, desc = "PROGRESSO: "):
    
        # QUEBRANDO A LINHA DO TXT
        login, nome, email, senha = usuario.strip().split('|')
        
        # EXECUÇÃO DO POST DE USUARIO
        try:
            requisicao = PostUsuario(bearer_token, login, nome, email, senha, ID_CLIENTE, ID_UNIDADE)
            
            # GRAVANDO LOG DE SUCESSO
            if requisicao.get_status == 200 or requisicao.get_status == 201:
                with open(pasta_de_trabalho + "\\Log\\LOG_DE_SUCESSO.txt", "a", encoding="utf-8") as log_de_sucesso:
                    log_de_sucesso.write("Linha {} executada com sucesso! | Login: '{}' | {}\n".format(contador, login, requisicao.get_texto_resposta))
                    
                # INCREMENTANDO CONTADORES
                contador += 1
                contador_de_sucesso += 1
                    
            # GRAVANDO LOG DE ERRO
            else:
                with open(pasta_de_trabalho + "\\Log\\LOG_DE_ERRO.txt", "a", encoding="utf-8") as log_de_erro:
                    log_de_erro.write("Linha {} não foi executada devido a um erro. | Login: '{}', Nome: '{}', E-mail: '{}', Senha: '{}' | {}\n".format(contador, login, nome, email, senha, requisicao.get_texto_resposta))
                    
                # INCREMENTANDO CONTADORES
                contador += 1
                contador_de_insucesso += 1
            
        # GRAVANDO LOG DE ERROS NÃO TRATADOS
        except Exception as erro_desconhecido:
            with open(pasta_de_trabalho + "\\Log\\LOG_ERRO_NAO_TRATADO", "a", encoding="utf-8") as log_de_erros_nao_tratados:
                log_de_erros_nao_tratados.write("Linha {} com erro desconhecido. | {}\n".format(contador, erro_desconhecido))
                
            # INCREMENTANDO CONTADORES
            contador += 1
            contador_de_insucesso += 1

print("\nUSUÁRIOS CRIADOS: {}".format(contador_de_sucesso))
print("ERROS OCORRIDOS: {}\n".format(contador_de_insucesso))
print("PROCESSO FINALIZADO!")