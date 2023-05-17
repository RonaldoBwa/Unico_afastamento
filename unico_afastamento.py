"""
Robo para conseguir a relação de afatamento e gerar a relação de cheques/liquidos
"""

"""
Importações necessárias
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
caminho_downloads_afastamento = (
    "C:\\WROBO\\08398543000110_4_COMUNICACAO_LTDA" + "\\Relação de afastamento"
)

caminho_downloads_liquido = (
    "C:\\WROBO\\15452593000102_PRIME_SEAFOOD" + "\\Relação de cheques líquidos"
)


class Unico_robo:
    def __init__(
        self,
        ano,
        mes,
        codigo_empresa,
        cnpj_empresa,
        colaborador,
        ano_liquido,
        mes_liquido,
        dia_liquido,
    ) -> None:
        self.__ano = ano
        self.__mes = mes
        self.__codigo_empresa = codigo_empresa
        self.__competencia = self.__mes + self.__ano

        # Processo relatório liquido folha
        self.__cnpj = cnpj_empresa
        self.__colaborador = colaborador

        self.__ano_liquido = ano_liquido
        self.__mes_liquido = mes_liquido
        self.__dia_liquido = dia_liquido
        self.__competencia_liquido = self.__mes_liquido + self.__ano_liquido
        self.__dia_do_pagamento = (
            self.__dia_liquido + self.__mes_liquido + self.__ano_liquido
        )

    """
    Chamadas afastamento.
    """

    def ano(self):
        return self.__ano

    def mes(self):
        return self.__mes

    def codigo_empresa(self):
        return self.__codigo_empresa

    """
    Chamadas liquido.
    """

    def cnpj_empresa(self):
        return self.__cnpj

    def colaborador(self):
        return self.__colaborador

    def ano_liquido(self):
        return self.__ano_liquido

    def mes_liquido(self):
        return self.__mes_liquido

    def dia_liquido(self):
        return self.__dia_liquido

    """
    Inicialização do app da unico.
    """

    def execute(self, path, delay: float = 0.0, LIMITER=3):
        if not LIMITER:
            return False
        try:
            time.sleep(0.5)
            keyboard.press_and_release("win + r")
            write(path, delay=delay)
            keyboard.press_and_release("enter")
            return True
        except:
            return execute(path, delay, decrement(LIMITER))
        sleep(10)

    """
    Processo para efetuar o login do usuário.
    """

    def login_user(self):
        """Atribuição as variáveis de login e password do usuário que irá entrar no sistema"""
        login = "ROBOT"
        password = "Bwa@2022!"

        """Escrevendo o login do usuário atraves do metodo type"""
        to_click(images.IMAGES["LABEL"]["USER"])
        sleep(0.5)
        keyboard.type(login)
        sleep(3)
        """Escrevendo a senha do usuário atraves do metodo type"""
        keyboard.press(Key.tab)
        keyboard.type(password)
        keyboard.press(Key.enter)

        sleep(3)

    """
    Processo para a mudança do tipo de sistema na plataforma da UNICO.
    """

    def sistema_folha(self):
        """Inicialização do 'try' para caso tenha outro usuário acessando a plataforma com o mesmo login poder prescionar 'esc' e fechar a tela de alert"""
        while exists(images.IMAGES["POP-UP"]["ALERT-USU"], seconds=1):
            try:
                keyboard.press(Key.esc)
                sleep(0.5)
            except:
                pass

        """Mudança do tipo de sistema unico contabil para unico folha"""
        to_click(images.IMAGES["BUTTONS"]["UNICO-CONTABIL"])
        sleep(0.5)
        to_click(images.IMAGES["BUTTONS"]["UNICO-FOLHA"])
        sleep(5)

    """
    Abertura do processo de listagem dos usuários afastados.
    """

    def abrir_relacao_afastamento(self):
        to_click(images.IMAGES["BUTTONS"]["RELATORIOS"])
        to_click(images.IMAGES["BUTTONS"]["PERIODICOS"])
        to_click(images.IMAGES["BUTTONS"]["AFASTAMENTO"])
        sleep(1)

    """
    Função para preencher os respectivos campos de formulário:
    Código da empresa -> Competência.
    """

    def formulario_afastamento(self):
        """Muda o código da empresa"""
        to_click(images.IMAGES["LABEL"]["EMPRESA"], x=10)
        keyboard.type(self.codigo_empresa())
        keyboard.press(Key.enter)

        sleep(2)

        keyboard.press(Key.tab)
        """Muda a competencia do processo"""
        to_click(images.IMAGES["LABEL"]["COMPETENCIA"])
        keyboard.type(self.__competencia)

    """
    Função para imprimir o relatório de afastamento.
    """

    def imprimir_relatorio_afastamento(self):
        to_click(images.IMAGES["BUTTONS"]["IMPRIMIR"], seconds=1)
        sleep(0.5)

        """
        Testa caso esteja selecionado outro tipo de formato que não seja o de PDF.
        """

        to_click(images.IMAGES["BUTTONS"]["IMPRESSORA-NOME"], x=35)
        sleep(0.5)
        keyboard.press(Key.up)
        to_click(images.IMAGES["BUTTONS"]["IMPRESSORA-PDF"])
        sleep(0.5)

        keyboard.press(Key.enter)
        sleep(1.5)

        """
        Aponta e diz qual o nome deve ser salvo no arquivo.
        """
        to_click(images.IMAGES["LABEL"]["MUDAR-NOME-ARQUIVO"], x=11)
        keyboard.type(caminho_downloads_afastamento)
        keyboard.press(Key.enter)
        
        #Entra caso tenha um arquivo com o mesmo nome para fazer a substituição
        while exists(images.IMAGES["ICONES"]["ATENTION-SAVE"], seconds=1):
            try:
                to_click(images.IMAGES["ICONES"]["ATENTION-SAVE"])
                to_click(images.IMAGES["BUTTONS"]["BTN-SIM"])
            except:
                pass
        keyboard.press(Key.esc)
        sleep(2)

    """
    Função para escolher a empresa e abir a função do liquido/cheques.
    """

    def abrir_liquido(self):
        to_click(images.IMAGES["BUTTONS"]["BTN-CASINHA"], seconds=1)
        to_click(images.IMAGES["LABEL"]["CAIXA-PESQUISA"], x=20)
        keyboard.type(self.__cnpj)
        keyboard.press(Key.enter)
        sleep(3)
        """Abrir relatorios/periodiocos"""
        to_click(images.IMAGES["BUTTONS"]["RELATORIOS"])
        to_click(images.IMAGES["BUTTONS"]["PERIODICOS"])
        to_click(images.IMAGES["BUTTONS"]["BTN-LIQUIDO"])  # clica no processo indicado
        sleep(5)

    """
    Função para preencher os respectivos campos de formulário:
    Colaborador -> Competência -> Data do pagamento.
    """

    def formulario_liquido(self):
        # defina o colaborador
        keyboard.type(self.__colaborador)
        keyboard.press(Key.enter)
        sleep(3)
        for i in range(4):
            keyboard.press(Key.tab)
            sleep(0.5)

        # defina a competencia
        keyboard.type(self.__competencia_liquido)
        sleep(1.5)

        # defina o dia do pagamento
        keyboard.type(self.__dia_do_pagamento)
        sleep(1)

    """
    Função para imprimir o relatório liquido/cheques.
    """

    def imprimir_relatorio_liquido(self):
        to_click(images.IMAGES["BUTTONS"]["IMPRIMIR"], seconds=1)
        sleep(1.5)

        to_click(images.IMAGES["BUTTONS"]["IMPRESSORA-NOME"], x=35)
        sleep(0.5)

        to_click(images.IMAGES["BUTTONS"]["IMPRESSORA-PDF"])
        sleep(0.5)

        keyboard.press(Key.enter)
        sleep(2)

        """
        Aponta e diz qual o nome deve ser salvo no arquivo.
        """

        to_click(images.IMAGES["LABEL"]["MUDAR-NOME-ARQUIVO"], x=11)
        keyboard.type(caminho_downloads_liquido)
        keyboard.press(Key.enter)

        #Entra caso tenha um arquivo com o mesmo nome para fazer a substituição
        while exists(images.IMAGES["ICONES"]["ATENTION-SAVE"], seconds=1):
            try:
                to_click(images.IMAGES["ICONES"]["ATENTION-SAVE"])
                to_click(images.IMAGES["BUTTONS"]["BTN-SIM"])
            except:
                pass
        sleep(1.25)

    """
    Função para fechar o UNICO.
    """

    def fechar_unico(self):
        for i in range(4):
            keyboard.press(Key.esc)
            sleep(0.25)
        keyboard.press(Key.enter)