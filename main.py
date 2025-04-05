from faker import Faker
import random
from datetime import datetime
from supabase import create_client, Client

#config do supabase
#laura
supabase_url = 'https://bgaldydhkrrtwxiivwtr.supabase.co'
supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJnYWxkeWRoa3JydHd4aWl2d3RyIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTczODcwOTMxNywiZXhwIjoyMDU0Mjg1MzE3fQ.wSJss4EPy3w8jBmBUPBiNovEK3xQuoZmdZV5JOsvK4U'

#bia

#supabase_url = 'https://ubvcklbdyepjvjologao.supabase.co'
#supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVidmNrbGJkeWVwanZqb2xvZ2FvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mzg3MDkzMDksImV4cCI6MjA1NDI4NTMwOX0.lp9adnmkgPspF5RVgjsSmAJQvZs-tkAeE3ke8vdadnU'

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

#adicionar cursos no supabase
contador = 0
for curso in cursos:
    try:
        # Verificar se o curso já existe no Supabase
        response = supabase.table('curso').select("id_curso").eq(
            'nome_curso', curso).execute()
        # Se não encontrar o curso, adiciona
        if len(response.data) == 0:
            data = {
                'nome_curso': curso,
                'id_curso': id_cursos[cursos.index(curso)]
            }
            supabase.table('curso').insert(data).execute()

            print(
                f"Curso {curso} com id {data['id_curso']} adicionado com sucesso!"
            )
            contador += 1
        else:
            print(f"Curso {curso} já existe no banco de dados.")

    except Exception as e:
        print(f"Erro ao adicionar curso {curso}: {e}")

#PROFESSORES
professores = []

#adicionar professores no supabase
for j in range(10):
    nome_professor = faker.name()  #gera nome aleatório
    id_professor = faker.unique.random_int(min=100000000, max=999999999)

    professores.append({
        "id_professor": id_professor,
        "nome_professor": nome_professor
    })

contadorProf = 0

for professor in professores:
    try:
        response = supabase.table('professor').select("id_professor").eq(
            'id_professor', professor["id_professor"]).execute()

        if len(response.data) == 0:  # Se não encontrar o id, adiciona
            supabase.table('professor').insert(professor).execute()
            print(
                f"Professor {professor['nome_professor']} com id {professor['id_professor']} adicionado com sucesso!"
            )
            contadorProf += 1
        else:
            print(
                f"Professor {professor['id_professor']} já existe no banco de dados."
            )
    except Exception as e:
        print(f"Erro ao adicionar professor {professor['id_professor']}: {e}")

print(f"Total de novos professores adicionados: {contadorProf}")

#TCC
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

#inserir tcc no supabase
for titulo in titulosDeTcc:
    try:
        tcc_data = supabase.table('tcc').insert(titulo).execute()
        # tcc_ids = [item['id'] for item in tcc_data.data]
        #print("tcc_ids", tcc_ids)
        #tcc_notas = [item['nota'] for item in tcc_data.data]
        print(
            f"Título de TCC inserido: {titulo['titulo']} (id: #{titulo['id_professor']})"
        )
    except Exception as e:
        print(
            f"Erro ao inserir título de TCC para o professor {titulo['id_professor']}: {e}"
        )
        print("Exception", e)

#print("processo finalizado!")

#GERAR ALUNOS

# Buscar todos os TCCs e extrair os IDs
tcc_result = supabase.table('tcc').select('id_tcc').execute()
tcc_ids = [tcc['id_tcc'] for tcc in tcc_result.data]

alunos = []

for i in range(10):
    nome = faker.name()  # Gera um nome fictício
    ra = faker.unique.random_int(min=100000000,
                                 max=999999999)  # Gera um RA único
    id_curso = id_cursos[random.randint(0, len(id_cursos) - 1)]
    # 70% de chance de ter um id_tcc, 30% de chance de ser None
    id_tcc = random.choice(
        tcc_ids) if tcc_ids and random.random() < 0.7 else None

    alunos.append({
        "nome": nome,
        "ra": ra,
        "id_curso": id_curso,
        "id_tcc": id_tcc
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

#MATERIAS
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

# Buscar professores existentes
professores = supabase.table('professor').select('id_professor').execute()
professores_ids = [prof['id_professor'] for prof in professores.data]
contador = 0
for materia in materias:
    try:
        codigo_materia = f"MAT-{contador+1:03d}"  # Ex: MAT-001, MAT-002...
        id_professor = random.choice(
            professores_ids) if professores_ids else None

        # Verificar se já existe matéria com mesmo nome
        response = supabase.table('materias').select("codigo_materia").eq(
            'nome_materia', materia).execute()

        if len(response.data) == 0:
            data = {
                'nome_materia': materia,
                'codigo_materia': codigo_materia,
                'id_professor': id_professor
            }
            supabase.table('materias').insert(data).execute()

            print(
                f"Materia '{materia}' com código {data['codigo_materia']} adicionada com sucesso!"
            )
            contador += 1
        else:
            print(f"Matéria '{materia}' já existe no banco de dados.")

    except Exception as e:
        print(f"Erro ao adicionar matéria '{materia}': {e}")

# DEPARTAMENTOS
departamentos = [
    "Matemática", "Ciência da Computação", "Física", "Engenharia Elétrica",
    "Engenharia Civil", "Engenharia de Produção", "Administração",
    "Ciência Social e Jurídica", "Engenharia Mecânica", "Engenharia Química"
]

# Buscar dados do banco
cursos = supabase.table('curso').select('id_curso').execute().data
professores = supabase.table('professor').select('id_professor').execute().data
materias = supabase.table('materias').select('codigo_materia').execute().data

# Verificar registros existentes
cursos_ids = [curso["id_curso"] for curso in cursos] if cursos else []
professores_ids = [prof["id_professor"] for prof in professores] if professores else []
materias_codigos = [materia["codigo_materia"] for materia in materias] if materias else []

# Buscar nomes dos departamentos já existentes
departamentos_ja_existentes = supabase.table('departamento').select(
    'nome').execute().data
nomes_departamentos_existentes = [
    dep['nome'] for dep in departamentos_ja_existentes
]

# Lista para armazenar os departamentos a serem inseridos
departamentos_para_inserir = []

# Cópia dos IDs para um professor so ser gerente de um departamento
professores_ids_disponiveis = professores_ids.copy()

for nome_departamento in departamentos:
    # Verifica se o nome já existe no banco
    if nome_departamento in nomes_departamentos_existentes:
        print(f"Departamento '{nome_departamento}' já existe no banco.")
        continue

    if not professores_ids_disponiveis:
        print("Todos os professores já foram alocados a departamentos.")
        break 

    id_professor = professores_ids_disponiveis.pop()
    id_curso = random.choice(cursos_ids) if cursos_ids else None
    codigo_materia = random.choice(
        materias_codigos) if materias_codigos else None

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