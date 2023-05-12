from unico_afastamento import *


iniciar_robo_relatorio_afastamento = Unico_afastamento("2023", "05", "2729")
iniciar_robo_relatorio_afastamento.unico_acess()
sleep(20)
iniciar_robo_relatorio_afastamento.login_user()
sleep(27)
iniciar_robo_relatorio_afastamento.sistema_folha()
sleep(3)
iniciar_robo_relatorio_afastamento.abrir_relacao_afastamento()
sleep(3)
iniciar_robo_relatorio_afastamento.listar_e_download()
sleep(2)
iniciar_robo_relatorio_afastamento.fechar_unico()
