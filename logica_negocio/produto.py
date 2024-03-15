
from sqlalchemy.orm import Session
from models import Produto
from logica_negocio import categoria
from sqlalchemy import select

def incluir(motor):
    print("Incluir novo produto")
    nome = input("Qual o nome do produto?")
    preco = float(input("Qual o preço do produto?"))
    estoque = int(input("Qual o estoque inicial do produto?"))
    cat_id = categoria.selecionar(motor)

    with Session(motor) as sessao:
        produto = Produto()
        produto.nome = nome
        produto.preco = preco
        produto.estoque = estoque
        produto.ativo = True
        produto.categoria_id =cat_id
        sessao.add(produto)
        sessao.commit()
        print(f"O Produto {nome} foi adicionado com sucesso!")

def selecionar(motor):

    nome_parcial = input("Digite uma parte do nome da categoria desejada: ")
    stmt = select(Produto).where(Produto.nome.ilike(f"%{nome_parcial}%")).order_by("nome")
    with Session(motor) as sessao:
        rset = sessao.execute(stmt).scalars()
        contador = 1
        ids = list()
        for produto in rset:
            print(f"{contador:3d} - {produto.nome}")
            ids.append(produto.id)
            contador = contador + 1
        cod = int(input("Digite o numero do produto desejada: "))
        produto = ids[cod - 1]
    return produto

def alterar(motor):
    id_produto = selecionar(motor)
    with Session(motor) as sessao:
        produto = sessao.get(Produto, id_produto)
        print(f"Deixe em branco as respostas abaixo para manter os valores atuais")
        novo_nome = input(f"Qual vai ser o novo nome ({produto.nome})?")
        novo_preco = input(f"Qual vai ser o novo preço: ({produto.preco:.2f})? ")
        situacao_hoje =  "Ativo" if produto.ativo else "Inativo"
        # if produto.ativo:
        #     siatuacao_hoje = "Ativo"
        # else:
        #     siatuacao_hoje = "Inativo"
        novo_ativo = input(f"Muda o status do produto ({situacao_hoje}) (S/N)?")
        if novo_nome != "":
            produto.nome = novo_nome
        if novo_preco != "":
            produto.preco = float(novo_preco)
        if novo_ativo[0].lower() == "s":
           produto.ativo = not produto.ativo

        sessao.commit()
        print(f"Produto Alterado!")