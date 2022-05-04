import pandas as pd
import numpy as np
from main import *

class Operacao():

    def __init__(operacao, lista_etrs,
                 extratante, conc_ext, solv_org, acido, celula,
                 n_min_celulas = 2, n_max_celulas = 10,
                 rao_min = 0.5, rao_max = 2.0,
                 pH_min = 1, pH_max = 1.5):

        operacao.lista_etrs = lista_etrs
        operacao.extratante = extratante
        operacao.conc_ext = conc_ext
        operacao.solv_org = solv_org
        operacao.acido = acido
        operacao.celula = celula
        operacao.n_min_celulas = n_min_celulas
        operacao.n_max_celulas = n_max_celulas
        operacao.rao_min = rao_min
        operacao.rao_max = rao_max
        operacao.pH_min = pH_min
        operacao.pH_max = pH_max
        operacao.tempo_projeto = operacao.celula.tempo_depreciacao

    def testa_varias_isotermas(operacao, excel = False):

        global H
        H = Proton('Próton', 'H+', None, 10 ** - operacao.pH_min)
        global isoterma
        isoterma = Isoterma(operacao.n_min_celulas, 0.5, [H] + operacao.lista_etrs)
        resumo_exemplo = isoterma.resumo()
        colunas_do_df = []

        for indice in range(len(resumo_exemplo)):
            for elemento in operacao.lista_etrs:
                indice_do_df = elemento.simbolo + ' ' + resumo_exemplo.index[indice]
                colunas_do_df.append(indice_do_df)

        guarda_condicoes = pd.DataFrame(columns = (['Operação', 'Extratante', 'Nº Células', 'Razão A/O', 'pH inicial']
                                                   + colunas_do_df))

        for n_celulas in range(operacao.n_min_celulas, operacao.n_max_celulas + 1):
            isoterma.n_celulas = n_celulas

            for rao in np.linspace(operacao.rao_min, operacao.rao_max,
                                   int((operacao.rao_max - operacao.rao_min) * 10 + 1)):
                isoterma.rao = rao

                for ca0 in np.logspace(- operacao.pH_min, - operacao.pH_max,
                                       int((operacao.pH_max - operacao.pH_min) * 10) + 1):
                    H.ca0 = ca0
                    H.pH_inicial = -np.log10(H.ca0)
                    resumo = isoterma.resumo()

                    if (
                        (
                         isoterma.tipo == 'Extração' and resumo.loc['Composição Rafinado (%)'][: -1].sum() >= 99.5
                         ) or
                            (
                             isoterma.tipo == 'Lavagem' and
                                (
                                 resumo.loc['Composição Rafinado (%)'][: -1].sum() >= 99 or
                                 resumo.loc['Composição org. Carregado (%)'][-1] >= operacao.lista_etrs[-1].pureza_minima
                                 )
                             )
                        ):

                            condicao = [isoterma.tipo,
                                        operacao.extratante.nome +' '+ str(int(100 * operacao.conc_ext)) + '%',
                                        n_celulas, rao, H.pH_inicial]
                            for linha in range(len(resumo)):
                                for etr in range(len(operacao.lista_etrs)):
                                    condicao.append(resumo.iloc[linha, etr])
                            condicao = pd.Series(condicao, index = guarda_condicoes.columns)
                            guarda_condicoes = guarda_condicoes.append(condicao, ignore_index = True)

        if excel:
            guarda_condicoes.sort_values(by = [operacao.lista_etrs[0].simbolo + ' Recuperação Rafinado (%)'],
                                         ascending = False, inplace = True)
            guarda_condicoes.to_excel('Melhores Condições.xlsx', sheet_name = 'Melhores Condições')

        return guarda_condicoes

    def viabilidade_economica(operacao, condicoes, kg_etr_produzido, excel = False, nome_planilha = None):

        inv_condicoes = []
        cpv_condicoes = []
        receita_condicoes = [kg_etr_produzido * operacao.tempo_projeto * operacao.lista_etrs[1].preco
                             for i in range(len(condicoes))]

        for i in range(len(condicoes)):

            etr_total_gl = np.array([(condicoes.iloc[i][etr.simbolo + ' Rafinado (mol/L)']
                                      * etr.massa_molar_oxido
                                      / etr.proporcao_estequiometrica)
                                    for etr in operacao.lista_etrs[: -1]]).sum()

            vol_aq = kg_etr_produzido * 1000 / etr_total_gl
            vol_org = vol_aq / condicoes.iloc[i]['Razão A/O']
            vol_ext = vol_org * operacao.conc_ext / operacao.extratante.pureza
            vol_solv = vol_org - vol_ext
            conc_molar_acido = operacao.acido.concentracao_mm * operacao.acido.densidade / operacao.acido.MM
            vol_acido = vol_aq * 10 ** - condicoes.iloc[i]['pH inicial'] / conc_molar_acido

            inv_ext = operacao.extratante.preco * vol_ext
            inv_solv = operacao.solv_org.preco * vol_solv
            inv_cels = operacao.celula.preco * condicoes.iloc[i]['Nº Células']

            cpv_acido = operacao.acido.preco * vol_acido * operacao.acido.densidade
            cpv_ext = inv_ext * operacao.extratante.taxa_perda
            cpv_solv = inv_solv * operacao.solv_org.taxa_perda
            cpv = cpv_acido + cpv_ext + cpv_solv
            cpv_projeto = cpv * operacao.tempo_projeto

            inv_giro = cpv
            inv_projeto = inv_ext + inv_solv + inv_cels + inv_giro

            inv_condicoes.append(inv_projeto)
            cpv_condicoes.append(cpv_projeto)

        condicoes['Receita'] = receita_condicoes
        condicoes['CPV'] = cpv_condicoes
        condicoes['CapEx'] = inv_condicoes
        condicoes['Saldo de Caixa'] = condicoes['Receita'] - condicoes['CPV'] - condicoes['CapEx']

        condicoes.sort_values(by = ['Saldo de Caixa'], ascending = False, inplace = True)

        if excel:
            condicoes.to_excel(nome_planilha + '.xlsx', sheet_name = 'Melhores Condições')

        return condicoes

    def atualiza_parametros(operacao, parametros_da_operacao, etapa_operacao):

        parametros_op = parametros_da_operacao[etapa_operacao + 1]
        operacao.n_min_celulas = parametros_op[0]
        operacao.n_max_celulas = parametros_op[1]
        operacao.rao_min = parametros_op[2]
        operacao.rao_max = parametros_op[3]
        operacao.pH_min = parametros_op[4]
        operacao.pH_max = parametros_op[5]

    def atualiza_correntes(operacao, condicao):

        for j in range(len(operacao.lista_etrs)):
            etr = operacao.lista_etrs[j]
            if isoterma.tipo == 'Extração':
                etr.con = condicao.loc[etr.simbolo + ' Carregado Orgânico (mol/L)']
                etr.ca0 = 0
            else:
                etr.ca0 = condicao.loc[etr.simbolo + ' Carregado Orgânico (mol/L)']
                etr.con = 0

            etr.ca0_gl = etr.ca0 * etr.massa_molar_oxido / etr.proporcao_estequiometrica
            etr.con_gl = etr.con * etr.massa_molar_oxido / etr.proporcao_estequiometrica

    def liga_isotermas(operacao, parametros_da_operacao, excel = False):
        #necessita atualização

        assert type(parametros_da_operacao) == list
        assert type((parametros_da_operacao)[0]) == list
        assert type((parametros_da_operacao)[1]) == list
        assert type((parametros_da_operacao)[2]) == list

        operacao.lista_etrs = parametros_da_operacao[0]
        operacao.extratante = parametros_da_operacao[1][0]
        operacao.conc_ext = parametros_da_operacao[1][1]
        operacao.solv_org = parametros_da_operacao[1][2]
        operacao.acido = parametros_da_operacao[1][3]
        operacao.celula = parametros_da_operacao[1][4]

        etapa_operacao = 1
        operacao.atualiza_parametros(parametros_da_operacao, etapa_operacao)
        condicoes_guardadas1 = operacao.testa_varias_isotermas()
        kg_etr_produzido = 1 #volume da fase aquosa da etapa de extração
        condicoes_guardadas1 = operacao.viabilidade_economica(condicoes_guardadas1, kg_etr_produzido)

        condicoes_finais = pd.DataFrame(columns = condicoes_guardadas1.columns)
        condicoes_finais = pd.concat([condicoes_finais] * 2, axis = 1)

        etapa_operacao += 1

        for condicao1 in range(len(condicoes_guardadas1)):
            condicao_guardada1 = condicoes_guardadas1.iloc[condicao1]
            rao1 = condicao_guardada1['Razão A/O']
            operacao.atualiza_correntes(condicao_guardada1)
            operacao.atualiza_parametros(parametros_da_operacao, etapa_operacao)
            condicoes_guardadas2 = operacao.testa_varias_isotermas()
            condicoes_guardadas2 = operacao.viabilidade_economica(condicoes_guardadas2, None, rao1)

            for condicao2 in range(len(condicoes_guardadas2)):
                condicao_guardada2 = condicoes_guardadas2.iloc[condicao2]
                condicao_final = pd.concat([condicao_guardada1, condicao_guardada2])
                condicoes_finais = condicoes_finais.append(condicao_final, ignore_index = True)

        for i in range(len(condicoes_finais)):
            condicoes_finais['Gastos Totais da Operação'] = condicoes_finais['Gastos da Etapa'].iloc[i].sum()

        if len(condicoes_finais) > 1:
            condicoes_finais.sort_values(by = ['Gastos Totais da Operação'], inplace = True)

        if excel:
            condicoes_finais.T.to_excel('Condições Finais.xlsx', sheet_name = 'Melhores Condições')

        return condicoes_finais

def testa_varias_operacoes(lista_operacoes, kg_etr_produzido, excel = False, nome_planilha = None):

    assert type(lista_operacoes) == list
    condicoes = lista_operacoes[0].viabilidade_economica(lista_operacoes[0].testa_varias_isotermas(), kg_etr_produzido)

    for operacao in lista_operacoes[1:]:
        condicoes = pd.concat([operacao.viabilidade_economica(operacao.testa_varias_isotermas(), kg_etr_produzido),
                               condicoes])

    condicoes = condicoes.drop(condicoes.iloc[:, 5:29], axis = 1)
    condicoes.sort_values(by = ['Saldo de Caixa'], ascending = False, inplace = True)

    if excel:
        condicoes.to_excel('Ranking Extratantes.xlsx', sheet_name = 'Melhores Condições')

    return condicoes