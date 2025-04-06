# Projeto_bancoDeDados
Projeto de Banco de Dados para uma universidade: 
O objetivo deste projeto é implementar um sistema de banco de dados para uma universidade. O sistema deve ser capaz de armazenar e gerenciar informações relacionadas a alunos, professores, departamentos, cursos, disciplinas, históricos escolares de alunos, histórico de disciplinas lecionadas por professores, TCCs apresentados considerando tanto o grupo de alunos como o professor orientador.

Integrantes:
-Beatriz Manaia Lourenço Berto RA: 22.125.060-8
-Laura de Souza Parente RA:22.123.033-7

# Como executar o projeto:
-abre o supabase (https://supabase.com/)e em "SQL Editor" coloque a DDL abaixo, emseguida clique em "run"

-no replit coloque o código commitado nesse projeto para inserir os dados na tabela, antes de rodar, coloque sua supabaseUrl e supabaseKey

-execute as queries abaixo para verificar o funcionamento do projeto

##  Modelo Entidade Relacionamento:
![codigo1](./imagens/MER.png)

## Modelo Relacional na 3FN:
![codigo1](./imagens/MR-3FN.png)

## DDL usado para a criação das tabelas necessárias:

```sql  
create table curso
	(id_curso	text, 
	nome_curso	text, 
	primary key (id_curso)
	);

 create table professor
  (nome_professor text,
  id_professor integer,
  primary key(id_professor)
  foreign key (id_departamento) references departamento (id_departamento)
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
   id_professor integer,
   primary key (codigo_materia),
  foreign key (id_professor) references professor (id_professor)
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
   codigo_materia text,
   foreign key (ra) references alunos (ra),
   foreign key (codigo_materia) references materias (codigo_materia)
  );


```
