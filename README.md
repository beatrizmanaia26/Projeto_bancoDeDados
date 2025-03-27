# Projeto_bancoDeDados
Projeto realizado em dupla com @laaurap na matéria de banco de dados 

##  Modelo Entidade Relacionamento:
![codigo1](./imagens/MER.png)

## Modelo Relacional na 3FN:
![codigo1](./imagens/MR3FN.png)

## DDL usado para a criação das tabelas necessárias:

```sql     create table curso
	(id_curso	serial not null, 
	nome_curso	text, 
	primary key (id_curso)
	);

 create table professor
  (nome_professor text,
  id_professor serial not null,
  primary key(id_professor)
  --foreign key (id_departamento) references departamento (id_departamento)
  );

  create table tcc
	(id_tcc serial not null, 
	titulo text,
  id_professor serial not null,
	primary key (id_tcc),
  foreign key (id_professor) references professor (id_professor)
	);

create table alunos
	(ra		text,
	 nome		text,
   id_curso	serial not null, --coluna tem q existir p chave estrangeira aponta
   id_tcc	serial not null,
	 primary key (ra),
   foreign key (id_curso) references curso (id_curso),
   foreign key (id_tcc) references tcc (id_tcc)
	);

  
create table materias
  (nome_materia text,
   codigo_materia text,
   id_professor serial not null,
   primary key (codigo_materia),
  foreign key (id_professor) references professor (id_professor)
  );

create table departamento 
  (nome text,
   id_departamento serial not null,
   id_curso	serial not null, 
   codigo_materia text,
   id_professor serial not null,
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
   id_professor serial not null,
  references materias (codigo_materia),
  foreign key (id_professor) references professor (id_professor)
  );

create table matriz_curricular_curso
  (semestre int,
   codigo_materia text,
   id_curso	serial not null,
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