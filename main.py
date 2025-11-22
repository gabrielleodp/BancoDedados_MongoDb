# main.py
from config import MENUS
from src.utils.splash_screen import SplashScreen
from src.controller.controller_usuario import ControllerUsuario
from src.controller.controller_tarefa import ControllerTarefa
from src.reports.relatorios import Relatorio
from src.conexion.mongo_queries import MongoQueries

# Conexão única
mongo = MongoQueries(can_write=True)
mongo.connect()

# Instanciando controllers e relatórios com a mesma conexão
tela_inicial = SplashScreen()
ctrl_usuario = ControllerUsuario(mongo)
ctrl_tarefa = ControllerTarefa(mongo)
relatorio = Relatorio(mongo)

def exibir_contagem():
    """Exibe a contagem de registros das coleções"""
    total_usuarios = mongo.count("usuarios")
    total_tarefas = mongo.count("tarefas")
    print(f"Total de Usuários: {total_usuarios}")
    print(f"Total de Tarefas: {total_tarefas}")

def confirmar_acao(msg: str) -> bool:
    """Pergunta ao usuário se deseja confirmar a ação"""
    resp = input(f"{msg} (S/N): ").strip().upper()
    return resp == "S"

def run():
    print(tela_inicial.get_updated_screen())
    exibir_contagem()

    while True:
        print(MENUS["principal"])
        opcao = input("Escolha uma opção [1-5]: ").strip()
        if not opcao.isdigit():
            continue
        opcao = int(opcao)

        # ---------- RELATÓRIOS ----------
        if opcao == 1:
            print(MENUS["relatorios"])
            opc_rel = input("Escolha o relatório: ").strip()
            if opc_rel == "1":
                relatorio.rel_usuarios()
            elif opc_rel == "2":
                relatorio.rel_tarefas()
            elif opc_rel == "3":
                relatorio.rel_tarefas_group_by()
            elif opc_rel == "4":
                relatorio.rel_tarefas_join()
            elif opc_rel == "0":
                continue

        # ---------- INSERIR ----------
        elif opcao == 2:
            while True:
                print(MENUS["entidades"])
                inserir_op = input("Escolha uma opção: ").strip()
                if inserir_op == "1":
                    ctrl_usuario.inserir()
                elif inserir_op == "2":
                    ctrl_tarefa.inserir()
                elif inserir_op == "0":
                    break
                else:
                    print("Opção inválida.")

        # ---------- ATUALIZAR ----------
        elif opcao == 3:
            while True:
                print(MENUS["entidades"])
                atualizar_op = input("Escolha uma opção: ").strip()
                if atualizar_op == "1":
                    ctrl_usuario.atualizar()
                elif atualizar_op == "2":
                    ctrl_tarefa.atualizar()
                elif atualizar_op == "0":
                    break
                else:
                    print("Opção inválida.")

        # ---------- EXCLUIR ----------
        elif opcao == 4:
            while True:
                print(MENUS["entidades"])
                excluir_op = input("Escolha uma opção: ").strip()
                if excluir_op == "1":
                    ctrl_usuario.excluir()
                elif excluir_op == "2":
                    ctrl_tarefa.excluir()
                elif excluir_op == "0":
                    break
                else:
                    print("Opção inválida.")

        # ---------- SAIR ----------
        elif opcao == 5:
            print("Saindo do sistema. Obrigado!")
            break

        # Atualiza contagem após cada operação
        exibir_contagem()

if __name__ == "__main__":
    run()
