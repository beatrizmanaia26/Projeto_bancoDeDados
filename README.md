# Projeto_bancoDeDados

Projeto de Banco de Dados para uma universidade: 

O objetivo deste projeto é implementar um sistema de banco de dados para uma universidade. O sistema deve ser capaz de armazenar e gerenciar informações relacionadas a alunos, professores, departamentos, cursos, disciplinas, históricos escolares de alunos, histórico de disciplinas lecionadas por professores, TCCs apresentados considerando tanto o grupo de alunos como o professor orientador.

Integrantes:

-Beatriz Manaia Lourenço Berto RA: 22.125.060-8

-Laura de Souza Parente RA:22.123.033-7

# Como executar o projeto:
-abre o supabase (https://supabase.com/)e em "SQL Editor" coloque a primeira DDL abaixo, em seguida clique em "run"

-após rodar a primeira DDL, no supabase, em "SQL editor" rode a segunda que está logo abaixo para fazer o relacionamento das tabelas que dependem uma da outra (como departamento na tabela professor)

-no replit coloque o código commitado nesse projeto (código esse que serve tanto para: gerar, inserir e validar dados na tabela) antes de rodar, coloque sua supabaseUrl e supabaseKey no código 

-execute as queries abaixo para verificar o funcionamento do projeto

##  Modelo Entidade Relacionamento:
![codigo1](./imagens/MER.jpg)

## Modelo Relacional na 3FN:
![codigo1](./imagens/MR-3FN.jpg)

## DDL usado para a criação das tabelas necessárias:

```sql

-- Apagar todas as tabelas considerando dependências
drop table if exists historico_aluno cascade;
drop table if exists matriz_curricular_curso cascade;
drop table if exists materias_lecionadas_por_professor cascade;
drop table if exists departamento cascade;
drop table if exists materias cascade;
drop table if exists alunos cascade;
drop table if exists tcc cascade;
drop table if exists professor cascade;
drop table if exists curso cascade;

--criar tabelas
create table curso
    (id_curso	text, 
    nome_curso	text, 
    primary key (id_curso)
    );

 create table professor
  (nome_professor text,
  id_professor integer,
 -- id_departamento serial not null,
  primary key(id_professor)
  --foreign key (id_departamento) references departamento (id_departamento)
  );
  
  create table tcc
    (id_tcc serial not null, 
    titulo text,
  id_professor integer,
  nota float,
    primary key (id_tcc),
  foreign key (id_professor) references professor (id_professor)
    );

create table alunos
    (ra		text,
     nome		text,
   id_curso text, --coluna tem q existir p chave estrangeira aponta
   id_tcc	integer,
     primary key (ra),
   foreign key (id_curso) references curso (id_curso),
   foreign key (id_tcc) references tcc (id_tcc)
    );

create table materias
  (nome_materia text,
   codigo_materia text,
   primary key (codigo_materia)
  );

create table departamento 
  (nome text,
   id_departamento serial not null,
   id_curso text, 
   codigo_materia text,
   id_professor integer,
   primary key(id_departamento),
   foreign key (id_curso) references curso (id_curso),
   foreign key (codigo_materia) references materias (codigo_materia),
   foreign key (id_professor) references professor (id_professor)
  );

create table materias_lecionadas_por_professor
  (horas_dadas float,
   semestre int,
   ano int,
   codigo_materia text,
   id_professor integer,
  foreign key (codigo_materia) references materias (codigo_materia),
  foreign key (id_professor) references professor (id_professor)
  );

create table matriz_curricular_curso
  (semestre int,
   codigo_materia text,
   id_curso	text,
   foreign key (codigo_materia) references materias (codigo_materia),
   foreign key (id_curso) references curso (id_curso)
  );

create table historico_aluno
  (nota_aluno float,
   semestre int,
   ra	text,
   ano integer ,
   codigo_materia text,
   primary key(semestre, ra,ano,codigo_materia),
   foreign key (ra) references alunos (ra),
   foreign key (codigo_materia) references materias (codigo_materia)
  );
  
```

## DDL para fazer relacionamento entra tabela "departamento" e tabela "professor"7

```sql 
--mudar tabelas adicionando FKs

ALTER TABLE curso 
ADD COLUMN id_professor INTEGER REFERENCES professor(id_professor);

ALTER TABLE professor
ADD COLUMN id_departamento INTEGER NOT NULL REFERENCES departamento(id_departamento),
ADD COLUMN id_curso TEXT  REFERENCES curso(id_curso);

-- Inserir curso
insert into curso (id_curso, nome_curso, id_professor)
values ('CC35473', 'Ciência da Computação', NULL);


-- Inserir os departamentos
insert into departamento (id_departamento, nome)
values 
  (1, 'Matemática'),
  (2, 'Ciência da Computação'),
  (3, 'Física'),
  (4, 'Engenharia Elétrica'),
  (5, 'Engenharia Civil'),
  (6, 'Engenharia de Produção'),
  (7, 'Administraçãoo'),
  (8, 'Ciência Social e Jurídica'),
  (9, 'Engenharia Mecânica'),
  (10, 'Engenharia Química');


-- inserir o professor para conseguir adicionar professor aleatorios com codigo sem impactar dependencia entre professor e departamento
insert into professor (id_professor, nome_professor, id_departamento, id_curso)
values (0, 'Default', 1, 'CC35473');

```

## QUERIES: 


```sql
--1) Mostre todo o histórico escolar de um aluno que teve reprovação em uma disciplina, retornando inclusive a reprovação em um semestre e a aprovação no semestre seguinte;

--validar query final:
--SELECT * from historico_aluno 

--SELECT * FROM historico_aluno
--WHERE 
--  historico_aluno.ra = '990842947' AND historico_aluno.nota_aluno < 5

--SELECT * FROM historico_aluno
--WHERE historico_aluno.ra = '990842947' AND historico_aluno.codigo_materia = 'MAT-001'

SELECT 
  histRep.ano AS ano_reprovacao,
  histRep.codigo_materia,
  histRep.nota_aluno AS nota_reprovacao,
  histRep.ra AS ra_aluno,
  histRep.semestre AS semestre_reprovacao,
  histAp.ano AS ano_aprovacao,
  histAp.nota_aluno AS nota_aprovacao,
  histAp.semestre AS semestre_aprovacao
FROM historico_aluno histRep
INNER JOIN historico_aluno histAp ON histRep.ra = histAp.ra --junta td onde todas as condicoes ocorrerem
AND histRep.codigo_materia = histAp.codigo_materia
AND (
    (histAp.ano > histRep.ano) 
  OR (histAp.ano = histRep.ano AND histAp.semestre > histRep.semestre)
)
WHERE 
  histRep.nota_aluno < 5
  AND histAp.nota_aluno >= 5;

--2)Mostre todos os TCCs orientados por um professor junto com os nomes dos alunos que fizeram o projeto;

--SELECT titulo FROM tcc WHERE id_professor = 234076463
--SELECT id_tcc FROM tcc WHERE  id_professor = 234076463
--SELECT nome FROM alunos WHERE id_tcc = select 2
SELECT 
  tcc.titulo AS titulo_tcc,
  alunos.nome AS nome_aluno,
  professor.nome_professor AS nome_orientador
FROM tcc
  INNER JOIN alunos ON alunos.id_tcc = tcc.id_tcc
  INNER JOIN professor ON professor.id_professor = tcc.id_professor;

--3)Mostre a matriz curicular de pelo menos 2 cursos diferentes que possuem disciplinas em comum (e.g., Ciência da Computação e Ciência de Dados). Este exercício deve ser dividido em 2 queries sendo uma para cada curso; 

--para descobrir os cursos que tem materias em comum:
--query que mostra os cursos onde a materia (que ta em mais de um curso) aparece

--SELECT DISTINCT(matriz_curricular_curso.id_curso)
---FROM matriz_curricular_curso
--WHERE matriz_curricular_curso.codigo_materia IN (
  --SELECT matriz_curricular_curso.codigo_materia
 --FROM matriz_curricular_curso
  --GROUP BY matriz_curricular_curso.codigo_materia
  --HAVING COUNT(matriz_curricular_curso.id_curso) >= 2);

SELECT 
  matriz_curricular_curso.codigo_materia,
  matriz_curricular_curso.id_curso,
  matriz_curricular_curso.semestre
FROM matriz_curricular_curso
WHERE matriz_curricular_curso.codigo_materia IN (
  SELECT matriz_curricular_curso.codigo_materia
  FROM matriz_curricular_curso
  GROUP BY matriz_curricular_curso.codigo_materia
  HAVING COUNT(matriz_curricular_curso.id_curso) >= 2)
  AND matriz_curricular_curso.id_curso = 'EM98785';
--query intenra retorna as materias que aparecem em mais de um curso

SELECT 
  matriz_curricular_curso.codigo_materia,
  matriz_curricular_curso.id_curso,
  matriz_curricular_curso.semestre
FROM matriz_curricular_curso
WHERE matriz_curricular_curso.codigo_materia IN (
  SELECT matriz_curricular_curso.codigo_materia
  FROM matriz_curricular_curso
  GROUP BY matriz_curricular_curso.codigo_materia
  HAVING COUNT(matriz_curricular_curso.id_curso) >= 2)
  AND matriz_curricular_curso.id_curso = 'CC35473';

--4)Para um determinado aluno, mostre os códigos e nomes das diciplinas já cursadas junto com os nomes dos professores que lecionaram a disciplina para o aluno; DUVIDA (calendario) 

SELECT 
  historico_aluno.codigo_materia,
  materias.nome_materia,
  professor.nome_professor
FROM 
  historico_aluno
INNER JOIN 
  materias ON materias.codigo_materia = historico_aluno.codigo_materia
INNER JOIN 
  materias_lecionadas_por_professor ON materias_lecionadas_por_professor.codigo_materia = materias.codigo_materia
INNER JOIN 
  professor ON professor.id_professor = materias_lecionadas_por_professor.id_professor
WHERE historico_aluno.ra = '117586697'; --RA sempre muda!!!!!!!!!!!!!!!!

--SELECT historico_aluno.codigo_materia FROM historico_aluno WHERE historico_aluno.ra ='133386147'; --para comparar cm query acima

--5)Liste todos os chefes de departamento e coordenadores de curso em apenas uma query de forma que a primeira coluna seja o nome do professor, a segunda o nome do departamento coordena e a terceira o nome do curso que coordena. Substitua os campos em branco do resultado da query pelo texto "nenhum"

--INNER JOIN, e isso só traria as linhas onde o professor é tanto chefe de departamento quanto coordenador de curso ao mesmo tempo 

SELECT 
  professor.nome_professor,
  COALESCE(departamento.nome, 'nenhum') AS departamento, --coalesce, se tiver o primeiro ele retorna o primeiro, se nao ele retorna o segundo do ()
  COALESCE(curso.nome_curso, 'nenhum') AS curso --depois do AS fica o nome dado para a coluna
FROM departamento
LEFT JOIN professor ON professor.id_professor = departamento.id_professor
LEFT JOIN curso ON curso.id_curso = professor.id_curso;

--6) Encontre os nomes de todos os estudantes.

SELECT alunos.nome FROM alunos;

--7) Liste os IDs e nomes de todos os professores.

SELECT
  professor.id_professor,
  professor.nome_professor
FROM professor;

--8) Encontre os nomes de todos os estudantes que cursaram "Banco de Dados"

SELECT
  alunos.nome
 FROM alunos
INNER JOIN historico_aluno ON alunos.ra = historico_aluno.ra
INNER JOIN materias ON historico_aluno.codigo_materia = materias.codigo_materia
WHERE materias.nome_materia = 'Banco de dados';

--9) Recupere os nomes dos estudantes que cursaram disciplinas do departamento de "Matemática".

SELECT DISTINCT alunos.nome
FROM alunos
INNER JOIN historico_aluno ON historico_aluno.ra = alunos.ra
INNER JOIN departamento ON departamento.codigo_materia = historico_aluno.codigo_materia
WHERE departamento.nome = 'Matemática';

-- 10) Encontre o número total de estudantes que cursaram "Inteligência artificial"

SELECT 
  COUNT(DISTINCT historico_aluno.ra) AS total_estudantes --distinct pra contar cada aluno apenas 1x
FROM historico_aluno
INNER JOIN materias ON materias.codigo_materia = historico_aluno.codigo_materia
WHERE materias.nome_materia = 'Inteligência artificial';

--11)  Recupere os nomes e IDs dos estudantes que são orientados por um professor específico (ID = 'I001').

SELECT 
  alunos.nome,
  alunos.ra
FROM alunos
INNER JOIN tcc ON tcc.id_tcc = alunos.id_tcc
INNER JOIN professor ON professor.id_professor = tcc.id_professor
WHERE tcc.id_professor = 944226947;

--12)Liste os cursos que foram ministrados pelos professores ID XXXX e 'YYYYY'. 

SELECT 
  DISTINCT(curso.nome_curso),
  materias_lecionadas_por_professor.id_professor
FROM curso
INNER JOIN matriz_curricular_curso ON matriz_curricular_curso.id_curso = curso.id_curso 
INNER JOIN materias_lecionadas_por_professor ON materias_lecionadas_por_professor.codigo_materia = matriz_curricular_curso.codigo_materia
WHERE materias_lecionadas_por_professor.id_professor IN (289492942, 756307682); --ID SEMPRE MUDA (materias lecionadas por prof)

--13) Encontre o número de alunos matriculados em cada curso e liste-os por título de curso.

SELECT 
  curso.nome_curso,
  COUNT(alunos.id_curso) 
FROM curso
INNER JOIN alunos ON alunos.id_curso = curso.id_curso
GROUP BY curso.nome_curso; --sempre que usa a função COUNT, deseja agrupar os resultados de acordo com algum critério é necessário usar a cláusula GROUP BY

--14) Encontre os estudantes que cursaram "Sistemas de Banco de Dados" mas não "Inteligência Artificial". 

SELECT 
  alunos.nome,
  alunos.ra --no select so coloco oq quero mostrar
FROM alunos
INNER JOIN historico_aluno ON historico_aluno.ra = alunos.ra
INNER JOIN  materias ON materias.codigo_materia = historico_aluno.codigo_materia
WHERE materias.nome_materia = 'Banco de dados' 
AND alunos.ra NOT IN(
  SELECT historico_aluno.ra
  FROM historico_aluno hist2
  INNER JOIN materias ON materias.codigo_materia = historico_aluno.codigo_materia
  WHERE materias.nome_materia = 'Inteligência artificial'
)

--15) Encontre os estudantes que cursaram "Ciência da Computação" ou "Engenharia Elétrica".

SELECT 
  alunos.nome,
  alunos.ra
FROM alunos
INNER JOIN curso ON curso.id_curso = alunos.id_curso
WHERE curso.nome_curso IN ('Engenharia Elétrica', 'Ciência da Computação');
```


