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
        #verificar se o curso já existe no Supabase
        response = supabase.table('curso').select("id_curso").eq(
            'nome_curso', curso).execute()  #eq é como um where no sql
        #se não encontrar o curso, adiciona
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
listaValidacaoIdsDep = [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  #para que todos os departamentos tenham pelo menos um professor

listaValidacaoIdsCursos = id_cursos.copy()  #para que todos os cursos tenham pelo menos um professor

while listaValidacaoIdsDep or listaValidacaoIdsCursos: #enquanto uma delas for verdadeira, continua o loop
    nome_professor = faker.name()
    id_professor = faker.unique.random_int(min=100000000, max=999999999)
    id_curso = random.choice(id_cursos)

    if listaValidacaoIdsDep: #se ainda tiver ids de departamentos na lista, usa um deles
        id_departamento = random.choice(listaValidacaoIdsDep)
        listaValidacaoIdsDep.remove(id_departamento)
    else:
        id_departamento = random.randint(1, 10)

    if listaValidacaoIdsCursos:
        id_curso = random.choice(listaValidacaoIdsCursos)
        listaValidacaoIdsCursos.remove(id_curso)
    else:
        id_curso = random.choice(id_cursos)

    professores.append({
        "id_professor": id_professor,
        "nome_professor": nome_professor,
        "id_departamento": id_departamento,
        "id_curso": id_curso
    })

#após garantir as condições, gerar mais professores com departamentos aleatórios
for j in range(20):
    nome_professor = faker.name()
    id_professor = faker.unique.random_int(min=100000000, max=999999999)
    id_departamento = random.randint(1, 10)
    id_curso = random.choice(id_cursos)

    professores.append({
        "id_professor": id_professor,
        "nome_professor": nome_professor,
        "id_departamento": id_departamento,
        "id_curso": id_curso
    })

 # adicionar os professores no supabase
contadorProf = 0
for professor in professores:
    try:
        response = supabase.table('professor').select("id_professor").eq(
            'id_professor', professor["id_professor"]).execute()

        if len(response.data) == 0:  #se não encontrar o id, adiciona
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

#na tabela de curso, adiciona coordenador de curso (id_prof) 
for curso in cursos:
    try:
        id_curso = id_cursos[cursos.index(curso)] #verifica o id do curso e pegar o departamento ou curso correspondente

        professores_do_curso = supabase.table('professor').select('id_professor').eq('id_curso', id_curso).execute() #busca todos os professores que estão associados ao curso

        if not professores_do_curso.data:
            print(f"Nenhum professor encontrado para o curso {curso}.")
            continue

        #nunca colocar prof de id 0 para ser coordenador
        professores_validos = []
        for prof in professores_do_curso.data:
            if prof["id_professor"] != 0:
                professores_validos.append(prof)

        if not professores_validos:
            print(f"Sem professor válido para o curso {curso}.")
            continue

        id_professor_escolhido = random.choice(professores_validos)["id_professor"] #escolhe um professor aleatório do curso entre os válidos

        #atualiza a tabela curso com o id_professor escolhido
        supabase.table('curso').update({
            "id_professor":id_professor_escolhido  
        }).eq("id_curso", id_curso).execute()

        print(
            f"Curso {curso} atualizado com coordenador de id{id_professor_escolhido}"
        )

    except Exception as e:
        print(f"Erro ao atualizar o curso {curso}: {e}")

print("Professores adicionados com sucesso!")

#TCC
titulosDeTcc = []
#percorrer a lista de professores que guarda "id_professor": id_professor e "nome_professor": nome_professor e iterar entre os id dos professores para inserir aleatoriamente os ids dos professores "id_professor" dentro da tabela "tcc"

for id_professor in professores:
    titulo_tcc = faker.sentence(nb_words=5)  #gera uma frase aleatória com 5 palavras
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
        print(
            f"Título de TCC inserido: {titulo['titulo']} (id: #{titulo['id_professor']})"
        )
    except Exception as e:
        print(
            f"Erro ao inserir título de TCC para o professor {titulo['id_professor']}: {e}"
        )

print("TCCs adicionados com sucesso!")

#GERAR ALUNOS
#busca todos os TCCs e extrair os IDs
tcc_result = supabase.table('tcc').select('id_tcc').execute()
tcc_ids = [tcc['id_tcc'] for tcc in tcc_result.data]

alunos = []

for i in range(30):
    nome = faker.name()
    ra = faker.unique.random_int(min=100000000, max=999999999)  #gera um RA único
    id_curso = id_cursos[random.randint(0, len(id_cursos) - 1)]
    #80% de chance de ter um id_tcc, 20% de chance de ser None (tem gente que nao tem tcc pq nao ta pra se formar)
    id_tcc = random.choice(tcc_ids) if tcc_ids and random.random() < 0.8 else None

    alunos.append({
        "nome": nome,
        "ra": ra,
        "id_curso": id_curso,
        "id_tcc": id_tcc
    })

#insere dados na tabela do Supabase
for aluno in alunos:
    try:
        data, count = supabase.table('alunos').insert(aluno).execute()
        print(f"Aluno inserido: {aluno['nome']} (ra: {aluno['ra']})")
    except Exception as e:
        print(f"Erro ao inserir aluno {aluno['nome']}: {e}")

print("Alunos adicionados com sucesso!")

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
#busca professores existentes
contador = 0
for materia in materias:
    try:
        codigo_materia = f"MAT-{contador+1:03d}"  # Ex: MAT-001, MAT-002...

        #verifica se já existe matéria com mesmo nome
        response = supabase.table('materias').select("codigo_materia").eq('nome_materia', materia).execute()

        if len(response.data) == 0:
            data = {'nome_materia': materia, 'codigo_materia': codigo_materia}
            supabase.table('materias').insert(data).execute()
            print(
                f"Materia '{materia}' com código {data['codigo_materia']} adicionada com sucesso!"
            )
            contador += 1
        else:
            print(f"Matéria '{materia}' já existe no banco de dados.")

    except Exception as e:
        print(f"Erro ao adicionar matéria '{materia}': {e}")

print("Matérias adicionadas com sucesso!")

# DEPARTAMENTOS

#busca dados no supabase
cursos = supabase.table('curso').select('id_curso').execute().data
materias = supabase.table('materias').select('codigo_materia').execute().data

#verifica registros existentes
cursos_ids = []
if cursos:
    for curso in cursos:
        cursos_ids.append(curso["id_curso"])

materias_codigos = []
if materias:
    for materia in materias:
        materias_codigos.append(materia["codigo_materia"])

#copia os IDs para um professor so ser gerente de um departamento

#atualiza os departamentos com curso, matéria e professor correspondente
for id_departamento in range(1, 11):
    try:
        id_curso_aleatorio = random.choice(cursos_ids)
        codigo_materia_aleatorio = random.choice(materias_codigos)

        professores_response = supabase.table('professor').select(
            'id_professor').eq('id_departamento', id_departamento).execute()
        professores_do_departamento = [
            p['id_professor'] for p in professores_response.data
        ]

        #filtra para garantir que o professor com ID 0 nunca seja usado
        professores_validos = []
        for p in professores_do_departamento:
            if p != 0:
                professores_validos.append(p)

        if not professores_validos:
            print(
                f"Nenhum professor válido encontrado para o departamento {id_departamento}"
            )
            continue

        id_professor_escolhido = random.choice(professores_validos)

        supabase.table('departamento').update({
            "id_curso":id_curso_aleatorio,
            "codigo_materia":codigo_materia_aleatorio,
            "id_professor":id_professor_escolhido
        }).eq("id_departamento", id_departamento).execute()

        print(f"Departamento {id_departamento} atualizado com curso {id_curso_aleatorio}, matéria {codigo_materia_aleatorio} e professor {id_professor_escolhido}")

    except Exception as e:
        print(f"Erro ao atualizar departamento {id_departamento}: {e}")

print("Departamentos adicionados com sucesso!")

#MATERIAS LECIONADAS POR PROFESSOR
#buscar dados no supabase
professores = supabase.table('professor').select('id_professor').execute()
materias = supabase.table('materias').select('codigo_materia').execute()
professores_ids = []
for prof in professores.data:
    professores_ids.append(prof['id_professor'])

materias_codigos = []
for materia in materias.data:
    materias_codigos.append(materia['codigo_materia'])

materias_por_professor = [] #para garantir que todas as materias tenham pelo menos um professor que as de

for codigo_materia in materias_codigos:
    id_professor = random.choice(professores_ids)
    ano = random.randint(1945, datetime.now().year)
    semestre = random.randint(1, 12)
    horas_dadas = round(random.uniform(20, 80), 1)

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
        print(f"Matéria {dados['codigo_materia']} lecionada pelo prof {dados['id_professor']} adicionada com sucesso!")
    except Exception as e:

        print(f"Erro ao inserir dados{dados}: {e}")

print("Histório de matérias lecionadas por professor adicionadas com sucesso!")


#MATRIZ CURRICULAR CURSO

#busca dados dos cursos e materias no supabase
cursos = supabase.table('curso').select('id_curso').execute()
materias = supabase.table('materias').select('codigo_materia').execute()

lista_curso = [curso['id_curso'] for curso in cursos.data]
lista_materia = [materia['codigo_materia'] for materia in materias.data]

#define número de semestres por curso
semestres_por_curso = {
    "CC": 10,
    "CD": 10,
    "AD": 10,
    "EC": 10,
    "EA": 10,
    "EP": 10,
    "EM": 10,
    "ER": 10,
    "EE": 10,
    "EQ": 10
}

materias_por_semestre = 3 #define número de matérias por semestre

materia_comum = random.choice(lista_materia)#escolhe 1 matéria comum para todos os cursos

matriz_curricular = []#cria as relações entre curso e matéria

for id_curso in lista_curso:
    prefixo = id_curso[:2]
    max_semestre = semestres_por_curso.get(prefixo, 10)

    materias_disponiveis = list(lista_materia)
    materias_disponiveis.remove(
        materia_comum)  #remove a matéria comum para evitar repetição

    for semestre in range(1, max_semestre + 1):
        materias_semestre = []

        if semestre == 1:
            materias_semestre.append(
                materia_comum
            )  #adiciona matéria comum no 1º semestre (precisa ter materia em cmum por conta da query)
            num_materias_necessarias = materias_por_semestre - 1
        else:
            num_materias_necessarias = materias_por_semestre

        if len(materias_disponiveis) < num_materias_necessarias:
            print(f"Sem mais matérias disponíveis para o curso {id_curso}.")
            break

        materias_selecionadas = random.sample(materias_disponiveis,num_materias_necessarias)

        #remove as matérias escolhidas da lista de disponíveis
        for materia in materias_selecionadas:
            materias_disponiveis.remove(materia)

        materias_semestre.extend(materias_selecionadas)

        #insere no supabase e montar a matriz curricular
        for codigo_materia in materias_semestre:
            dado = {
                "id_curso": id_curso,
                "codigo_materia": codigo_materia,
                "semestre": semestre
            }

            try:
                supabase.table('matriz_curricular_curso').insert(
                    dado).execute()
                print(f"Dados inseridos: {dado}")
            except Exception as e:
                print(
                    f"Erro ao inserir dados da matriz curricular: {dado}: {e}")

            matriz_curricular.append(dado)

print("\nMatriz curricular adicionada com sucesso!")

#HISTORICO ALUNO

'''
HISTORICO:
-com todos os RA (coloca todos os ra da tabela alunos e faz for neles):
garantir que na tabela historico: VARIOS RA COM MATERIAS DIFERENTES e cada materia com varios ra
fazer ter aluno com nota 5: se pessoa ta com nota abaixo da media (5)
(ANO SEMESTRE RA CODIGO MATERIA NOTA)
adiciono nova linha no historico com nota > 5 aleatoria, codigo materia = codigo materia anterior, ra igual ra anterior e se semestre for 2, aumento 1 no ano e faco semestre ser 1, se semestre for 1, aumento 1 no semestr ee mantenho ano 

'''

#busca dados no supabase
alunos = supabase.table('alunos').select('ra').execute()
ras = [aluno['ra'] for aluno in alunos.data]
materias = supabase.table('materias').select('codigo_materia').execute()
codigos_materia = [m['codigo_materia'] for m in materias.data]

#para cada aluno, criar um histórico acadêmico
for ra in ras:
    historicos_aluno = []  #lista para armazenar os registros de histórico deste aluno

    ano_ingresso = random.randint(1945, datetime.now().year)  
    semestre_atual = random.choice([1,2,3])   #escolher aleatoriamente se o aluno ingressou no 1º ou 2º semestre


    num_materias = random.randint(20, min(40, len(codigos_materia)))  #escolher aleatoriamente quantas matérias o aluno cursou 

    materias_aleatorias = random.sample(codigos_materia, num_materias)

    for codigo_materia in materias_aleatorias:
        nota = round(random.uniform(0, 10))

        # Criar registro do histórico
        historico = {
            'ra': ra,
            'codigo_materia': codigo_materia,
            'nota_aluno': nota,
            'semestre': semestre_atual,
            'ano': ano_ingresso
        }
        historicos_aluno.append(historico)

        # Se a nota for menor que 5, adicionar uma segunda vez a materia, ra e ano, mas com nota maior que 5
        if nota < 5:
            nova_nota = round(random.uniform(5, 10), 1)

            # Ajustar semestre e ano
            if semestre_atual == 1:
                novo_semestre = 2
                novo_ano = ano_ingresso
            else:
                novo_semestre = 1
                novo_ano = ano_ingresso + 1

            # Adicionar registro de recuperação
            historico_recuperacao = {
                'ra': ra,
                'codigo_materia': codigo_materia,
                'nota_aluno': nova_nota,
                'semestre': novo_semestre,
                'ano': novo_ano
            }
            historicos_aluno.append(historico_recuperacao)

            # Atualizar semestre e ano para próxima matéria
            semestre_atual = novo_semestre
            ano_ingresso = novo_ano
        else:
            if semestre_atual == 1:
                semestre_atual = 2
            else:
                semestre_atual = 1
                ano_ingresso += 1

    #inserir todos os registros
    try:
        supabase.table('historico_aluno').insert(historicos_aluno).execute()
        print(f"histórico do aluno {ra['ra']} adicionado com sucesso!")
    except Exception as e:
        print(f"Erro ao inserir histórico para RA {ra}: {e}")

print("\nHistórico adicionado com sucesso!")

