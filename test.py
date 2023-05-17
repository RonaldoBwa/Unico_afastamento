from unico_afastamento import *

# Processo de afastamento
ano_afastamento = "2023"
mes_afastamento = "05"
codigo_da_empresa_afastamento = "433"
# Processo liquido/cheques
cnpj_liquido = "15.452.593/0001-02"
colaborador_liquido = "1605"
ano_liquido = "2023"
mes_liquido = "04"
dia_liquido = "28"

# teste, eu iniciei colocar o cnpj aq
iniciar_robo_relatorio = Unico_robo(
    ano_afastamento,
    mes_afastamento,
    codigo_da_empresa_afastamento,
    cnpj_liquido,
    colaborador_liquido,
    ano_liquido,
    mes_liquido,
    dia_liquido,
)

"""
Inicializnado o robo e abrir o UNICO/folha
"""
iniciar_robo_relatorio.execute("mstsc /v:209.126.83.104:30555 /f")

iniciar_robo_relatorio.login_user()

iniciar_robo_relatorio.sistema_folha()

"""
Inicialização do processo de relátorio de afastamento
"""
iniciar_robo_relatorio.abrir_relacao_afastamento()

iniciar_robo_relatorio.formulario_afastamento()

iniciar_robo_relatorio.imprimir_relatorio_afastamento()


"""
Inicialização do processo de relátorio líquido
"""
iniciar_robo_relatorio.abrir_liquido()

iniciar_robo_relatorio.formulario_liquido()

iniciar_robo_relatorio.imprimir_relatorio_liquido()

iniciar_robo_relatorio.fechar_unico()
