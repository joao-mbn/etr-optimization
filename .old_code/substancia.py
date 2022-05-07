class Substancia():

    def __init__(substancia, nome, preco, propriedades_fisqui):

        substancia.nome = nome
        substancia.preco = preco

        for key in propriedades_fisqui:
            setattr(substancia, key, propriedades_fisqui[key])