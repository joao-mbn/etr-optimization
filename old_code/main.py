import numpy as np
from scipy.optimize import fsolve


class Elemento():

    def __init__(elemento, nome, simbolo, preco, ca0):

        elemento.nome = nome
        elemento.preco = preco
        elemento.simbolo = simbolo
        elemento.ca0 = ca0

    def chutes_iniciais(elemento, n_celulas, valor_esperado_final):

        return np.linspace(elemento.ca0, valor_esperado_final, n_celulas)

    def concentracoes_aquoso(elemento, chutes):

        cas = {'ca1': chutes[0]}

        for i in range(2, isoterma.n_celulas + 1):
            cas['ca' + str(i)] = chutes[i - 1]

        return cas


class Proton(Elemento):

    def __init__(proton, nome, simbolo, preco, ca0):

        super().__init__(nome, simbolo, preco, ca0)
        proton.pH_inicial = -np.log10(ca0)

    def pH (proton, ca):

        pH = -np.log10(ca)
        return pH


class ETR(Elemento):

    def __init__(etr, nome, simbolo, preco, pureza_minima,
                 ca0, con, massa_molar_oxido, proporcao_estequiometrica, coef_ang_modelo, coef_lin_modelo):

        super().__init__(nome, simbolo, preco, ca0)
        etr.ca0_gl = ca0
        etr.con_gl = con
        etr.massa_molar_oxido = massa_molar_oxido
        etr.proporcao_estequiometrica = proporcao_estequiometrica #proporção estequiométrica entre o elemento e o seu óxido
        etr.a = coef_ang_modelo
        etr.b = coef_lin_modelo
        etr.ca0 = etr.ca0_gl * etr.proporcao_estequiometrica / etr.massa_molar_oxido
        etr.con = etr.con_gl * etr.proporcao_estequiometrica / etr.massa_molar_oxido
        etr.pureza_minima = pureza_minima

    def D (etr, H):

        D = H ** - etr.a * 10 ** etr.b
        return D

    def concentracoes_organico(etr, D, ca):

        co = D * ca
        return co

    def conservacao_de_massa_aq(etr, ca_anterior, ca_atual, ca_posterior, h_atual, h_posterior, rao):

        cm_etr = (
                  ca_atual * (etr.D(h_atual) + rao)
                  - ca_posterior * etr.D(h_posterior)
                  - ca_anterior * rao
                  )

        return cm_etr

    def conservacao_de_massa_org(etr, ca_anterior, ca_atual, co_inicial, h_atual, rao):

        cm_etr = (
                  ca_atual * (etr.D(h_atual) + rao)
                  - co_inicial
                  - ca_anterior * rao
                  )

        return cm_etr


class Celula():

    def __init__(celula, nome, preco, numero, tempo_depreciacao = None):

        celula.nome = nome
        celula.preco = preco
        celula.numero = numero
        celula.tempo_depreciacao = tempo_depreciacao

    def balanco_de_massa(celula, etr, cas_etr, cas_H, rao, n_celulas):

        if celula.numero == 1:
            bm_etr = etr.conservacao_de_massa_aq(etr.ca0,
                                                 cas_etr['ca1'],
                                                 cas_etr['ca2'],
                                                 cas_H['ca1'],
                                                 cas_H['ca2'],
                                                 rao)
        elif celula.numero == n_celulas:
            bm_etr = etr.conservacao_de_massa_org(cas_etr['ca' + str(n_celulas - 1)],
                                                  cas_etr['ca' + str(n_celulas)],
                                                  etr.con,
                                                  cas_H['ca' + str(n_celulas)],
                                                  rao)
        else:
            bm_etr = etr.conservacao_de_massa_aq(cas_etr['ca' + str(celula.numero - 1)],
                                                 cas_etr['ca' + str(celula.numero)],
                                                 cas_etr['ca' + str(celula.numero + 1)],
                                                 cas_H['ca' + str(celula.numero)],
                                                 cas_H['ca' + str(celula.numero + 1)],
                                                 rao)

        return bm_etr

    def balanco_de_carga(celula, cas_H, lista_cas_etrs, K):

        etrs_totais_celula = 0

        for cas_etr in range(len(lista_cas_etrs)):
            etr_total_celula = lista_cas_etrs[cas_etr]['ca' + str(celula.numero)]
            etrs_totais_celula += etr_total_celula

        carga_total_protons_celula = cas_H['ca' + str(celula.numero)]
        carga_total_celula = 3 * etrs_totais_celula + carga_total_protons_celula

        bc = carga_total_celula - K

        return bc


class Isoterma():

    def __init__ (isoterma, n_celulas, rao, lista_elementos):

        isoterma.n_celulas = n_celulas
        isoterma.rao = rao
        isoterma.lista_elementos = lista_elementos

    def junta_chutes_iniciais(isoterma):

        proton = isoterma.lista_elementos[0]
        lista_etrs = isoterma.lista_elementos[1:]

        chutes_H = proton.chutes_iniciais(isoterma.n_celulas, 1.2 * proton.ca0)
        chutes_etrs = np.concatenate([etr.chutes_iniciais(isoterma.n_celulas, 0.001 * etr.ca0) for etr in lista_etrs])

        chutes = np.concatenate((chutes_H, chutes_etrs))

        return chutes

    def junta_variaveis(isoterma, chutes):

        proton = isoterma.lista_elementos[0]
        chutes_H = chutes[0 : isoterma.n_celulas]

        cas_H = proton.concentracoes_aquoso(chutes_H)
        cas = [cas_H]

        for i in range(1, len(isoterma.lista_elementos)):
            etr = isoterma.lista_elementos[i]
            chutes_etr = chutes[i * isoterma.n_celulas : (i + 1) * isoterma.n_celulas]
            cas_etr = etr.concentracoes_aquoso(chutes_etr)
            cas.append(cas_etr)

        return cas

    def constante_de_carga(isoterma):

        proton = isoterma.lista_elementos[0]
        cargas_totais_etr = 0

        for etr in isoterma.lista_elementos[1:]:
            cargas_totais_etr += 3 * (etr.ca0)

        K = cargas_totais_etr + proton.ca0

        return K

    def equacoes_massa_carga(isoterma, chutes):

        rao = isoterma.rao
        n_celulas = isoterma.n_celulas
        cas_H = isoterma.junta_variaveis(chutes)[0]
        lista_cas_etrs = isoterma.junta_variaveis(chutes)[1:]
        K = isoterma.constante_de_carga()

        equacoes = []

        for numero_da_celula in range(1, n_celulas + 1):
            celula = Celula(None, None, numero_da_celula)

        #equações de balanço de massa
            for cas_etrs in range(len(lista_cas_etrs)):
                cas_etr = lista_cas_etrs[cas_etrs]
                etr = isoterma.lista_elementos[cas_etrs + 1]
                bm_etr = celula.balanco_de_massa(etr, cas_etr, cas_H, rao, n_celulas)
                equacoes.append(bm_etr)

        #equações de balanço de carga
            bc = celula.balanco_de_carga(cas_H, lista_cas_etrs, K)
            equacoes.append(bc)

        return equacoes

    def resolve_equacoes_massa_carga(isoterma):

        resultados = fsolve(isoterma.equacoes_massa_carga, isoterma.junta_chutes_iniciais())
        return resultados