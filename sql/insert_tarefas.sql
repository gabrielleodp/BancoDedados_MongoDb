-- Inserção de tarefas
INSERT INTO TAREFAS (ID_TAREFA, TITULO, DESCRICAO, STATUS, USUARIO_TAREFA) 
VALUES (1, 'Estudar SQL', 'Estudar comandos básicos de SQL', 'PENDENTE', 1);
INSERT INTO TAREFAS (ID_TAREFA, TITULO, DESCRICAO, STATUS, USUARIO_TAREFA) 
VALUES (2, 'Criar classes', 'Criar model e controller', 'EM ANDAMENTO', 2);
INSERT INTO TAREFAS (ID_TAREFA, TITULO, DESCRICAO, STATUS, USUARIO_TAREFA) 
VALUES (3, 'Testar sistema', 'Testar todas as funcionalidades', 'PENDENTE', 3);
COMMIT;
