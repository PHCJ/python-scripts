pip install transformers

from transformers import AutoTokenizer, AutoModelForQuestionAnswering
import torch

# Carregar o tokenizador e o modelo pré-treinado
model_name = "timpal0l/mdeberta-v3-base-squad2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForQuestionAnswering.from_pretrained(model_name)

# Verificar se o tokenizador e o modelo foram carregados com sucesso
assert tokenizer is not None, "Erro ao carregar o tokenizador."
assert model is not None, "Erro ao carregar o modelo."

context_text = (
    "Olá! Bem-vindo ao assistente virtual da Full Sports. Estou aqui para ajudar "
    "com suas perguntas sobre nossa equipe incrível e nossos projetos. "
    "A Full Sports é uma empresa fundada em 2021, "
    "dedicada a anunciar e vender produtos esportivos, tais como uniformes, equipamentos para treinamento, acessórios, "
    "suplementos e outros artigos desportivos.\n\n"
    "Objetivo do Projeto:\n"
    "A Full Sports tem como objetivo oferecer produtos de marcas conhecidas e de alta qualidade para os amantes de academia "
    "e esportes. Queremos proporcionar uma experiência de compra completa, focando em produtos que atendam às necessidades "
    "dos nossos clientes.\n\n"
    "Descrição do Projeto:\n"
    "O projeto foi iniciado no primeiro semestre de 2021 como parte do currículo das disciplinas de Banco de Dados, Desenvolvimento Web, "
    "Engenharia de Software e Design Digital na Faculdade de Tecnologia da Zona Leste, em São Paulo. A Full Sports foi criada para "
    "facilitar o dia a dia dos jovens e adultos que estavam em casa devido à quarentena da Covid-19. Através de um e-commerce de artigos esportivos, os clientes podem navegar online ou através do aplicativo em busca de produtos que os auxiliem "
    "a se exercitar em casa, encontrando diversas opções de compra. Nosso objetivo é oferecer equipamentos esportivos e roupas de treinamento, "
    "direcionados ao público fitness na faixa etária de 16 a 48 anos.\n\n"
    "Entre em contato conosco pelo telefone: (11) 9 0000-0000.\n\n"
    "Aqui estão os principais membros da nossa equipe:\n\n"
    "1. Daniela Houck - Front-end Developer:\n   Daniela é especialista em desenvolvimento front-end, "
    "trazendo habilidades excepcionais para criar interfaces de usuário intuitivas e atraentes.\n\n"
    "2. Gabriel Gozzi - Back-end Developer:\n   Gabriel é um desenvolvedor back-end altamente experiente, "
    "contribuindo para a construção robusta e eficiente dos nossos sistemas e servidores.\n\n"
    "3. Lisandra Ferraz - Front-end Developer:\n   Lisandra é uma talentosa desenvolvedora front-end, "
    "trabalhando para criar experiências de usuário envolventes e responsivas.\n\n"
    "4. Paulo H. C. Jesus - Back-end Developer:\n   Paulo é desenvolvedor back-end, "
    "lidando com a lógica e a infraestrutura que sustentam nossas aplicações e serviços.\n\n"
    "5. Renan Figueredo - Full-stack Developer:\n   Renan é um desenvolvedor full-stack versátil, "
    "com habilidades tanto no front-end quanto no back-end, garantindo soluções completas e integradas.\n\n"
    "Se precisar de mais informações ou tiver perguntas específicas sobre algum membro da equipe ou sobre nossos projetos, "
    "fique à vontade para perguntar!"
)

def ask_question(question, context):
    # Tokenizar o contexto e a pergunta
    inputs = tokenizer(context, question, return_tensors="pt")

    # Realizar a inferência no modelo
    outputs = model(**inputs)

    # Obter as previsões
    start_scores = outputs.start_logits
    end_scores = outputs.end_logits

    # Encontrar os tokens de início e fim com as pontuações mais altas
    answer_start = torch.argmax(start_scores)
    answer_end = torch.argmax(end_scores) + 1

    # Decodificar os tokens de resposta
    answer = tokenizer.decode(inputs["input_ids"][0, answer_start:answer_end])

    return answer

def toAsk():
    question_text = input("Qual a pergunta?").lower()
    result = ask_question(question_text, context_text)
    print(result)

if __name__ == "__main__":
    print("Bem-vindo ao assistente virtual da Full Sports!")

    while True:
        try:
            toAsk()
        except Exception as e:
            print(f"Ocorreu um erro: {e}")

        continuar = input("Deseja fazer outra pergunta? (Digite 's' para sim ou 'n' para não): ").lower()
        if continuar != 's':
            break

#Peguntas atuis que podem ser feitas:
#Quem faz parte da equipe?
#Qual o número de telefone?
#Como posso entrar em contato?
#Quando a empresa foi fundada?
#Qual objetivo da empresa?
#O que a empresa faz?
#Como comprar na loja?
#Qual público alvo?
#Quais opções de produto?

#Entre outras varias pergutas que o modelo entendeu o contexto do domínio.