"""
Robo para conseguir a relação de afatamento de funcionários atraves do sistema da UNICO
"""

import pynput
from pynput import mouse, keyboard
from pynput.mouse import Button, Controller
from pynput.keyboard import Key, Controller
from pag import *
from img import images
from time import sleep

mouse = pynput.mouse.Controller()
keyboard = pynput.keyboard.Controller()
caminho_downloads = str(pathlib.Path.cwd() / "download" / "Relação de afastamento")


class Unico_afastamento:
    def __init__(self, ano, mes, codigo_empresa) -> None:
        self.__ano = ano
        self.__mes = mes
        self.__codigo_empresa = codigo_empresa
        self.__competencia = self.__mes + self.__ano

    def ano(self):
        return self.__ano

    def mes(self):
        return self.__mes

    def codigo_empresa(self):
        return self.__codigo_empresa

    """Inicialização do app da unico"""

    def unico_acess(self):
        """Duplo click na imagem do app da unico"""
        double_click(images.IMAGES["ICONES"]["UNICO"])
        sleep(3)
        """Clica no botão de confirmação do error alert"""
        to_click(images.IMAGES["BUTTONS"]["CONFIRM"])
        sleep(3)

    """Processo para efetuar o login do usuário"""

    def login_user(self):
        """Atribuição as variáveis de login e password do usuário que irá entrar no sistema"""
        login = "ROBOT"
        password = "123mudar."

        """Escrevendo o login do usuário atraves do metodo type"""
        to_click(images.IMAGES["LABEL"]["USER"])
        keyboard.type(login)

        """Escrevendo a senha do usuário atraves do metodo type"""
        to_click(images.IMAGES["LABEL"]["PASSWORD"])
        keyboard.type(password)
        keyboard.press(Key.enter)

    """Processo para a mudança do tipo de sistema na plataforma da UNICO"""

    def sistema_folha(self):
        """Inicialização do 'try' para caso tenha outro usuário acessando a plataforma com o mesmo login poder prescionar 'esc' e fechar a tela de alert"""
        try:
            to_click(images.IMAGES["ICONES"]["ILERT"])
            keyboard.press(Key.esc)
        except:
            pass

        sleep(1)
        """Mudança do tipo de sistema unico contabil para unico folha"""
        to_click(images.IMAGES["BUTTONS"]["UNICO-CONTABIL"])
        sleep(1)
        to_click(images.IMAGES["BUTTONS"]["UNICO-FOLHA"])
        sleep(1)

    """Abertura do processo de listagem dos usuários afastados"""

    def abrir_relacao_afastamento(self):
        to_click(images.IMAGES["BUTTONS"]["RELATORIOS"])
        to_click(images.IMAGES["BUTTONS"]["PERIODICOS"])
        to_click(images.IMAGES["BUTTONS"]["AFASTAMENTO"])

    """
    A maior parte, e a mais importante do robo inteiro, ocorre aqui dentro. 
    Basicamente sua função é a de informar o código da empresa, o período de listagem e por pra imprimir.
    Os passos vindouros faz parte do processo de salvar o arquivo dentro da página designada -> download.
    """

    def listar_e_download(self):
        """Área listar"""

        """Muda o código da empresa"""
        to_click(images.IMAGES["LABEL"]["EMPRESA"], x=10)
        keyboard.type(self.codigo_empresa())
        keyboard.press(Key.enter)

        sleep(3)
        keyboard.press(Key.tab)
        """Muda a competencia do processo"""
        to_click(images.IMAGES["LABEL"]["COMPETENCIA"])
        keyboard.type(self.__competencia)

        """Área baixar"""
        to_click(images.IMAGES["BUTTONS"]["IMPRIMIR"])
        sleep(1)

        """
        Testa caso esteja selecionado outro tipo de formato que não seja o de PDF.
        """
        try:
            to_click(images.IMAGES["BUTTONS"]["IMPRESSORA-NOME"])
            sleep(1)
            to_click(images.IMAGES["BUTTONS"]["IMPRESSORA-PDF"])
            sleep(1)
        except:
            pass

        keyboard.press(Key.enter)
        sleep(2)

        """
        Aponta e diz qual o nome deve ser salvo no arquivo.
        """
        to_click(images.IMAGES["LABEL"]["MUDAR-NOME-ARQUIVO"], x=10)
        keyboard.type(caminho_downloads)
        keyboard.press(Key.enter)
        """
        Teste caso peça para substituir o arquivo com mesmo nome (Provavelmente devo mudar)
        """
        try:
            to_click(images.IMAGES["ICONES"]["ATENTION-SAVE"])
            to_click(images.IMAGES["BUTTONS"]["BTN-SIM"])
        except:
            pass

    """
    Função para fechar o UNICO
    """

    def fechar_unico(self):
        for i in range(2):
            keyboard.press(Key.esc)
            sleep(1)
        sleep(1)
        keyboard.press(Key.enter)
