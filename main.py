from faker import Faker
import random
from supabase import create_client, Client

#config do supabase
#laura
#supabase_url = 'https://bgaldydhkrrtwxiivwtr.supabase.co'
#supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJnYWxkeWRoa3JydHd4aWl2d3RyIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTczODcwOTMxNywiZXhwIjoyMDU0Mjg1MzE3fQ.wSJss4EPy3w8jBmBUPBiNovEK3xQuoZmdZV5JOsvK4U'

#bia

supabase_url = 'https://ubvcklbdyepjvjologao.supabase.co'
supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVidmNrbGJkeWVwanZqb2xvZ2FvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mzg3MDkzMDksImV4cCI6MjA1NDI4NTMwOX0.lp9adnmkgPspF5RVgjsSmAJQvZs-tkAeE3ke8vdadnU'

supabase: Client = create_client(supabase_url, supabase_key)

faker = Faker('pt_BR')  #inicializar faker

#CURSOS DISPONIVEIS
cursos = [
    "Ciência da Computação", "Ciência de Dados", "Engenharia Civil",
    "Engenharia Automação e controle", "Engenharia de Produção",
    "Engenharia Mecânica", "Engenharia de Robôs", "Engenharia Elétrica",
    "Engenharia Química", "Administração"
]

id_cursos = [
    "CC35473", "CD76764", "EC13532", "EA54378", "EP12145", "EM98785",
    "ER455310", "EE13463", "EQ87455", "AD94221"
]

#Antes de adicionar, ver o array pra saber o que ja ta no supabase, se o nome do curso novo ja existir na lista nao adiciona novamente!!!!!!!!!!!!!!!!!!!!!!!!!

#adicionar cursos no supabase
contador = 0
for curso in cursos: 
    try:
        data, count = supabase.table('curso').insert({
            'nome_curso':
            curso,
            'id_curso':
            id_cursos[cursos.index(curso)]
        }).execute()
        print(f"Curso {curso} com id {id_cursos} adicionado com sucesso!")
        
    except Exception as e:
        print(f"Erro ao adicionar curso {curso}: {e}")

#GERAR PROFESSORES

#Antes de adicionar, ver o array pra saber o que ja ta no supabase, se o id aleatorio novo ja estiver na lista, nao insere, se nao estiver, adiciona na listas!!!!!!!!!!!!!!!!!!!!!!!

professores = []

for j in range(20):
    nome_professor = faker.name()  #gera nome aleatório
    id_professor = faker.unique.random_int(min=100000000, max=999999999)

    professores.append({
        "id_professor": id_professor,
        "nome_professor": nome_professor
    })

for professor in professores:
    try:
        data, count = supabase.table('professor').insert(professor).execute()
        print(
            f"Professor inserido: {professor['nome_professor']} (id: {professor['id_professor']})"
        )
    except Exception as e:
        print(f"Erro ao inserir professor {professor['nome_professor']}: {e}")

print("processo finalizado!")

#tcc
# Gerar frases aleatórias (titulo tcc)
titulosDeTcc = []
#percorrer a lista de professores que guarda "id_professor": id_professor e "nome_professor": nome_professor e iterar entre os id dos professores para inserir aleatoriamente os ids dos professores "id_professor" dentro da tabela "tcc"

for id_professor in professores:
    titulo_tcc = faker.sentence(
        nb_words=5)  #gera uma frase aleatória com 5 palavras
    id_professor_random = random.choice(professores)["id_professor"]
    titulosDeTcc.append({
        "id_professor": id_professor_random,
        "titulo": titulo_tcc,
        "nota": random.randint(0, 10)
    })

for titulo in titulosDeTcc:
    try:
        tcc_data = supabase.table('tcc').insert(titulo).execute()
        tcc_ids = [item['id'] for item in tcc_data.data]
        tcc_notas = [item['nota'] for item in tcc_data.data]
        print(
            f"Título de TCC inserido: {titulo['titulo']} (id: {titulo['id_professor']})"
        )
    except Exception as e:
        print(
            f"Erro ao inserir título de TCC para o professor {titulo['id_professor']}: {e}"
        )
        tcc_ids = []

#print("processo finalizado!")

#GERAR ALUNOS(100)
alunos = []

for i in range(100):  #gerar 100 alunos
    nome = faker.name()  # Gera um nome fictício
    ra = faker.unique.random_int(min=100000000,
                                 max=999999999)  # Gera um RA único
    #hora_complementar = random.randint(0,#200)  #horas complementares de 0 a 200
    id_curso = random.randint(1, 10)
    # id_tcc = random.choice(
    #  tcc_ids) if tcc_ids and random.random() < 0.7 else None

    alunos.append({
        "nome": nome,
        "ra": ra,
        "id_curso": id_curso,
        # "id_tcc": id_tcc
    })

# Inserir dados na tabela 'alunos' do Supabase
for aluno in alunos:
    try:
        data, count = supabase.table('alunos').insert(aluno).execute()
        print(f"Aluno inserido: {aluno['nome']} (ra: {aluno['ra']})")
    # print(
    #  f"Aluno inserido: {aluno['nome']} (ra: {aluno['ra']}) id_tcc: {aluno['id_tcc']}"
    # )
    except Exception as e:
        print(f"Erro ao inserir aluno {aluno['nome']}: {e}")

print("Processo concluído!")

#horas complementares por curso   *****************************
#10 semestres total 200 horas, cada semestre a pessoa pode conseguir no maximo 20 horas,para todos os cursos************************

#MATERIA

#nome da materia

#MATERIA
#nome da materia
materias = [
    "Banco de dados", "Digital Experience", "Fundamentos de algoritmos",
    "Programação Fullstack", "Sociologia", "Modelagem matemática",
    "Arquitetura e organização de computadores", "Digital Experience ultimate",
    "Desenvolvimento de algoritmos", "Leitura e pensamento critico",
    "Cálculo diferencial e Integral", "Cálculo vetorial e geometria analitica",
    "Arquitetura de software e Programação orientada a objetos",
    "experiência do usuário e front-end", "Pessoa, sociedade e tecnologia",
    "redes de computadores", "Álgebra linear e aplicações",
    "Cálculo multivariável", "Estrutura de dados", "engenharia de software",
    "Linguagens formais e autômatos", "desenvolvimendo de aplicações móveis",
    "Ecologia e sustentabilidade", "Equações diferenciais e séries",
    "Métodos numéricos", "Performance e tunning de dados",
    "Interação humano-computador", "Compiladores", "IOT",
    "Sistemas Operacionais", "Expressão oral e escrita",
    "Modelos probabilísticos, amostrafem e inferência estatísitica",
    "Fundamentos de finanças", "Complexidade de algorítmos",
    "Teste de software", "Inteligência artificial", "Ética",
    "Startups inovadoras e sustentáveis", "TCC e metodologia científica",
    "Gestão de projeto de software",
    "Computação gráfica e realidades imersivas", "Cloud computing e devops",
    "Jogos digitais", "Seguranca e criptografia",
    "Projeto de desenvolvimento de software", "Computação Quântica",
    "Gestão de pessoas", "desenho técmico", "Física 1",
    "Práticas de Inovação1", "Práticas de Inovação2", "Física2", "Física3",
    "Mecânica geral", "Topografia", "Economia"
]

# Buscar professores existentes no Supabase
professores = supabase.table('professor').select('id_professor').execute()
professores_ids = [prof['id_professor'] for prof in professores.data]

# Criar lista de matérias a serem inseridas
materias_para_inserir = []

for i in range(100):
    codigo_materia = f"MAT-{i+1:03d}"  # Gera códigos como MAT-001, MAT-002...
    nome_materia = random.choice(materias)  # Escolhe uma matéria da lista
    id_professor = random.choice(
        professores_ids
    ) if professores_ids else None  # Escolhe um professor existente

    materias_para_inserir.append({
        "codigo_materia": codigo_materia,
        "nome_materia": nome_materia,
        "id_professor": id_professor
    })

# Inserindo no banco
for materia in materias_para_inserir:
    try:
        supabase.table('materias').insert(materia).execute()
        print(f"Matéria {materia['nome_materia']} adicionada com sucesso!")
    except Exception as e:
        print(f"Erro ao adicionar matéria {materia['nome_materia']}: {e}")

print("Processo finalizado!")

#DEPARTAMENTOS
departamentos = [
    "Matemática", "Ciencia da Computação", "Fisica", "Engenharia Eletrica",
    "Engenharia Civil", "Engenharia de Produção", "Administração",
    "Ciencia Social e Juridica", "Engenharia Mecanica", "Engenharia Quimica"
]

# Buscar cursos e professores do banco
cursos = supabase.table('curso').select('id_curso').execute().data
professores = supabase.table('professor').select('id_professor').execute().data
materias = supabase.table('materias').select('codigo_materia').execute().data

# Verifica se há registros no banco
cursos_ids = [curso["id_curso"] for curso in cursos] if cursos else []
professores_ids = [prof["id_professor"]
                   for prof in professores] if professores else []
materias_codigos = [materia["codigo_materia"]
                    for materia in materias] if materias else []

# Lista para armazenar os departamentos a serem inseridos
departamentos_para_inserir = []

for i in range(10):
    nome_departamento = faker.company()  # Nome fictício do departamento
    id_curso = random.choice(
        cursos_ids) if cursos_ids else None  # Curso existente
    codigo_materia = random.choice(
        materias_codigos) if materias_codigos else None  # Matéria existente
    id_professor = random.choice(
        professores_ids) if professores_ids else None  # Professor existente

    if id_curso and codigo_materia and id_professor:
        departamentos_para_inserir.append({
            "nome": nome_departamento,
            "id_curso": id_curso,
            "codigo_materia": codigo_materia,
            "id_professor": id_professor
        })

# Inserção no banco
for departamento in departamentos_para_inserir:
    try:
        supabase.table('departamento').insert(departamento).execute()
        print(f"Departamento inserido: {departamento['nome']}")
    except Exception as e:
        print(f"Erro ao inserir departamento {departamento['nome']}: {e}")

print("Processo concluído!")
