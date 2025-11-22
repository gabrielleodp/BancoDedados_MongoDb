from config import MENUS
from src.utils.splash_screen import SplashScreen
from src.controller.controller_usuario import ControllerUsuario
from src.controller.controller_tarefa import ControllerTarefa
from src.reports.relatorios import Relatorio
from src.conexion.oracle_queries import OracleQueries

# Conexão única
oracle = OracleQueries(can_write=True)
oracle.connect()

# Instanciando controllers e relatórios com a mesma conexão
tela_inicial = SplashScreen()
ctrl_usuario = ControllerUsuario(oracle)
ctrl_tarefa = ControllerTarefa(oracle)
relatorio = Relatorio(oracle)  # ajuste necessário em relatorios.py para receber oracle

def exibir_contagem():
    """Exibe a contagem de registros das tabelas"""
    total_usuarios = oracle.sqlToMatrix("SELECT COUNT(1) FROM USUARIOS")[0][0]
    total_tarefas = oracle.sqlToMatrix("SELECT COUNT(1) FROM TAREFAS")[0][0]
    print(f"Total de Usuários: {total_usuarios}")
    print(f"Total de Tarefas: {total_tarefas}")

def listar_usuarios():
    """Lista os usuários e retorna os IDs"""
    usuarios = oracle.sqlToMatrix("SELECT ID_USUARIO, NOME FROM USUARIOS ORDER BY ID_USUARIO")
    for u in usuarios:
        print(f"{u[0]} - {u[1]}")
    return [u[0] for u in usuarios]

def listar_tarefas():
    """Lista as tarefas e retorna os IDs"""
    tarefas = oracle.sqlToMatrix("SELECT ID_TAREFA, TITULO FROM TAREFAS ORDER BY ID_TAREFA")
    for t in tarefas:
        print(f"{t[0]} - {t[1]}")
    return [t[0] for t in tarefas]

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
            opc_rel = input("Escolha relatório: ").strip()
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
                inserir_op = input("Escolha entidade: ").strip()
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
                atualizar_op = input("Escolha entidade: ").strip()
                if atualizar_op == "1":
                    listar_usuarios()
                    ctrl_usuario.atualizar()
                elif atualizar_op == "2":
                    listar_tarefas()
                    ctrl_tarefa.atualizar()
                elif atualizar_op == "0":
                    break
                else:
                    print("Opção inválida.")

        # ---------- EXCLUIR ----------
        elif opcao == 4:
            while True:
                print(MENUS["entidades"])
                excluir_op = input("Escolha entidade: ").strip()
                if excluir_op == "1":
                    listar_usuarios()
                    if confirmar_acao("Deseja realmente excluir este usuário?"):
                        ctrl_usuario.excluir()
                elif excluir_op == "2":
                    listar_tarefas()
                    if confirmar_acao("Deseja realmente excluir esta tarefa?"):
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

