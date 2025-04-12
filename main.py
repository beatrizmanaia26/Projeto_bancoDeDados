from faker import Faker
import random
from datetime import datetime
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

#adicionar cursos no supabase
contador = 0
for curso in cursos:
    try:
        # Verificar se o curso já existe no Supabase
        response = supabase.table('curso').select("id_curso").eq(
            'nome_curso', curso).execute()  #eq é como um where no sql
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
listaValidacaoIdsDep = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

while listaValidacaoIdsDep:
    nome_professor = faker.name()
    id_professor = faker.unique.random_int(min=100000000, max=999999999)

    # Garante que os primeiros ids_departamento cobrem todos da lista
    id_departamento = random.choice(listaValidacaoIdsDep)

    # Remove da lista após uso
    listaValidacaoIdsDep.remove(id_departamento)

    professores.append({
        "id_professor": id_professor,
        "nome_professor": nome_professor,
        "id_departamento": id_departamento
    })

# Após garantir cobertura, pode gerar mais professores com departamentos aleatórios
for j in range(20):  # Gera mais 20 professores extras
    nome_professor = faker.name()
    id_professor = faker.unique.random_int(min=100000000, max=999999999)
    id_departamento = random.randint(1, 10)

    professores.append({
        "id_professor": id_professor,
        "nome_professor": nome_professor,
        "id_departamento": id_departamento
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

#GERAR ALUNOS

# Buscar todos os TCCs e extrair os IDs
tcc_result = supabase.table('tcc').select('id_tcc').execute()
tcc_ids = [tcc['id_tcc'] for tcc in tcc_result.data]

alunos = []

for i in range(30):
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

contador = 0
for materia in materias:
    try:
        codigo_materia = f"MAT-{contador+1:03d}"  # Ex: MAT-001, MAT-002...

        # Verificar se já existe matéria com mesmo nome
        response = supabase.table('materias').select("codigo_materia").eq(
            'nome_materia', materia).execute()

        if len(response.data) == 0:
            data = {
                'nome_materia': materia,
                'codigo_materia': codigo_materia
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

# Buscar dados do banco
cursos = supabase.table('curso').select('id_curso').execute().data
#professores = supabase.table('professor').select('id_professor').execute().data
materias = supabase.table('materias').select('codigo_materia').execute().data

# Verificar registros existentes
cursos_ids = [curso["id_curso"] for curso in cursos] if cursos else []
#professores_ids = [prof["id_professor"] for prof in professores] if professores else []
materias_codigos = [materia["codigo_materia"] for materia in materias] if materias else []


# Cópia dos IDs para um professor so ser gerente de um departamento

# Atualizar os departamentos com curso, matéria e professor correspondente
# Atualizar os departamentos com curso, matéria e professor correspondente
for id_departamento in range(1, 11):
    try:
        id_curso_aleatorio = random.choice(cursos_ids)
        codigo_materia_aleatorio = random.choice(materias_codigos)

        professores_response = supabase.table('professor').select('id_professor').eq('id_departamento', id_departamento).execute()
        professores_do_departamento = [p['id_professor'] for p in professores_response.data]

        # Filtrar para garantir que o professor com ID 0 nunca seja usado
        professores_validos = [p for p in professores_do_departamento if p != 0]

        if not professores_validos:
            print(f"Nenhum professor válido encontrado para o departamento {id_departamento}, pulando...")
            continue

        id_professor_escolhido = random.choice(professores_validos)

        supabase.table('departamento').update({
            "id_curso": id_curso_aleatorio,
            "codigo_materia": codigo_materia_aleatorio,
            "id_professor": id_professor_escolhido
        }).eq("id_departamento", id_departamento).execute()

        print(f"Departamento {id_departamento} atualizado com curso {id_curso_aleatorio}, matéria {codigo_materia_aleatorio} e professor {id_professor_escolhido}")

    except Exception as e:
        print(f"Erro ao atualizar departamento {id_departamento}: {e}")

#MATERIAS LECIONADAS POR PROFESSOR
#buscar dados no supabase
professores = supabase.table('professor').select('id_professor').execute()
materias = supabase.table('materias').select('codigo_materia').execute()
professores_ids = [prof['id_professor'] for prof in professores.data]
codigo_materia = [materia['codigo_materia'] for materia in materias.data]

materias_por_professor = []

for p in range(15):
    id_professor = random.choice(professores_ids)
    codigo_materia = random.choice(materias_codigos)
    ano = random.randint(1945, datetime.now().year)
    semestre = random.randint(1, 12)
    horas_dadas = round(random.uniform(20, 80), 1)  # de 20 a 80 horas

    materias_por_professor.append({
        "id_professor": id_professor,
        "codigo_materia": codigo_materia,
        "ano": ano,
        "horas_dadas": horas_dadas,
        "semestre": semestre
    })

#inserir na tabela
for dados in materias_por_professor:
    try:
        supabase.table('materias_lecionadas_por_professor').insert(
            dados).execute()
        print(f"Dados inseridos: {dados}")
    except Exception as e:
        print(f"Erro ao inserir dados {dados}: {e}")

print("Matérias lecionadas adicionadas!")

#MATRIZ CURRICULAR CURSO
import random

# buscar dados dos cursos e materias no supabase
cursos = supabase.table('curso').select('id_curso').execute()
materias = supabase.table('materias').select('codigo_materia').execute()

lista_curso = [curso['id_curso'] for curso in cursos.data]
lista_materia = [materia['codigo_materia'] for materia in materias.data]

# Definir número de semestres por curso
semestres_por_curso = {
    "CC": 10, "CD": 10, "AD": 10, "EC": 10, "EA": 10,
    "EP": 10, "EM": 10, "ER": 10, "EE": 10, "EQ": 10
}

# Definir número de matérias por semestre
materias_por_semestre = 3

# Escolher 1 matéria comum para todos os cursos
materia_comum = random.choice(lista_materia)

# Criando as relações entre curso e matéria
matriz_curricular = []

for id_curso in lista_curso:
    prefixo = id_curso[:2]
    max_semestre = semestres_por_curso.get(prefixo, 10)

    materias_disponiveis = list(lista_materia)
    materias_disponiveis.remove(materia_comum)  # remove a matéria comum para evitar repetição indevida

    for semestre in range(1, max_semestre + 1):
        materias_semestre = []

        if semestre == 1:
            materias_semestre.append(materia_comum)  # adiciona matéria comum no 1º semestre
            num_materias_necessarias = materias_por_semestre - 1
        else:
            num_materias_necessarias = materias_por_semestre

        if len(materias_disponiveis) < num_materias_necessarias:
            print(f"Sem mais matérias disponíveis para o curso {id_curso}.")
            break

        materias_selecionadas = random.sample(materias_disponiveis, num_materias_necessarias)

        # remove as matérias escolhidas da lista de disponíveis
        for materia in materias_selecionadas:
            materias_disponiveis.remove(materia)

        materias_semestre.extend(materias_selecionadas)

        # inserir no supabase e montar a matriz curricular
        for codigo_materia in materias_semestre:
            dado = {
                "id_curso": id_curso,
                "codigo_materia": codigo_materia,
                "semestre": semestre
            }

            try:
                supabase.table('matriz_curricular_curso').insert(dado).execute()
                print(f"Dados inseridos: {dado}")
            except Exception as e:
                print(f"Erro ao inserir dados da matriz curricular: {dado}: {e}")

            matriz_curricular.append(dado)

print("Matriz curricular adicionada com sucesso!")

#HISTORICO ALUNO

# Buscar alunos que já têm histórico
historico_existente = supabase.table('historico_aluno').select('ra').execute()
ras_ja_com_historico = set([item['ra'] for item in historico_existente.data])

# Buscar todos os RAs de alunos
alunos = supabase.table('alunos').select('ra').execute()
ras = [aluno['ra'] for aluno in alunos.data]

# Buscar códigos das matérias
materias = supabase.table('materias').select('codigo_materia').execute()
codigos_materia = [m['codigo_materia'] for m in materias.data]

historicos = []
contador_inseridos = 0
contador_pulados = 0

for ra in ras:
    if ra in ras_ja_com_historico:
        print(f"RA {ra} já tem histórico")
        contador_pulados += 1
        continue

    try:
        materias_escolhidas = random.sample(codigos_materia, 3)
        for codigo in materias_escolhidas:
            historico = {
                'ra': ra,
                'codigo_materia': codigo,
                'nota_aluno': random.randint(0, 10),
                'semestre': random.randint(1, 10),
                'ano': random.randint(1945,datetime.now().year)
            }
            historicos.append(historico)

        # Inserir histórico no Supabase
        supabase.table('historico_aluno').insert(historicos).execute()
        print(f"Histórico inserido com sucesso para RA {ra}!")
        contador_inseridos += 1
        historicos = []  # limpa para o próximo aluno

    except Exception as e:
        print(f"Erro ao inserir histórico para RA {ra}: {e}")

'''
HISTORICO:
-com todos os RA (coloca todos os ra da tabela alunos e faz for neles):
garantir que na tabela historico: VARIOS RA COM MATERIAS DIFERENTES e cada materia com varios ra
fazer ter aluno com nota 5: se pessoa ta com nota abaixo da media (5)
(ANO SEMESTRE RA CODIGO MATERIA NOTA)
adiciono nova linha no historico com nota > 5 aleatoria, codigo materia = codigo materia anterior, ra igual ra anterior e se semestre for 2, aumento 1 no ano e faco semestre ser 1, se semestre for 1, aumento 1 no semestr ee mantenho ano 

'''
