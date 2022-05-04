from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from main import Proton

def monta_tabela(isoterma, uso, excel = False):

    resultados = isoterma.resolve_equacoes_massa_carga()
    tabela_externa = pd.DataFrame({'Estágio Nº': np.arange(1, isoterma.n_celulas + 1)})
    tabela_interna = pd.DataFrame({'Estágio Nº': np.arange(1, isoterma.n_celulas + 1)})

    for i in range(len(isoterma.lista_elementos)):
        elemento = isoterma.lista_elementos[i]
        simbolo_elementar = elemento.simbolo
        concentracoes_aq_molar = (resultados[isoterma.n_celulas * i: isoterma.n_celulas * (i + 1)])

        if type(elemento) != Proton:
            concentracoes_aq_gl = (concentracoes_aq_molar * elemento.massa_molar_oxido
                                    / elemento.proporcao_estequiometrica)
            D = elemento.D(tabela_externa['[' + isoterma.lista_elementos[0].simbolo + '](mol/L)'])
            concentracoes_org_molar = elemento.concentracoes_organico(D, concentracoes_aq_molar)
            concentracoes_org_gl = elemento.concentracoes_organico(D, concentracoes_aq_gl)

            tabela_interna['[' + simbolo_elementar + ']aq(mol/L)'] = concentracoes_aq_molar
            tabela_externa['[' + simbolo_elementar + ']aq(g/L)'] = concentracoes_aq_gl
            tabela_interna['[' + simbolo_elementar + ']org(mol/L)'] = concentracoes_org_molar
            tabela_externa['[' + simbolo_elementar + ']org(g/L)'] = concentracoes_org_gl
            tabela_externa['D ' + simbolo_elementar] = D

            if i > 1:
                Beta = D / tabela_externa['D ' + isoterma.lista_elementos[i - 1].simbolo]
                tabela_externa['Beta ' + simbolo_elementar + '/' + isoterma.lista_elementos[i - 1].simbolo] = Beta

        else:
            tabela_interna['[' + simbolo_elementar + '](mol/L)'] = concentracoes_aq_molar
            tabela_externa['[' + simbolo_elementar + '](mol/L)'] = concentracoes_aq_molar
            tabela_externa['pH'] = elemento.pH(concentracoes_aq_molar)

    tabela_externa.set_index('Estágio Nº', inplace = True)
    tabela_interna.set_index('Estágio Nº', inplace = True)

    if excel:
        tabela_externa.to_excel('Isoterma.xlsx',
                                sheet_name = str((isoterma.rao, isoterma.n_celulas,
                                                    isoterma.lista_elementos[0].pH_inicial)))
    if uso == 'interno':
        return tabela_interna
    else:
        return tabela_externa

def resumo(isoterma):

    tabela = isoterma.monta_tabela(uso = 'interno')

    tabela_resumida = pd.DataFrame(columns = [etr.simbolo for etr in isoterma.lista_elementos[1:]])
    tabela_resumida.loc['Alimentação aq. (mol/L)'] = [etr.ca0 for etr in isoterma.lista_elementos[1:]]
    tabela_resumida.loc['Alimentação org. (mol/L)'] = [etr.con for etr in isoterma.lista_elementos[1:]]
    tabela_resumida.loc['Rafinado (mol/L)'] = np.array(tabela.iloc[-1, 1: :2])
    tabela_resumida.loc['Carregado Orgânico (mol/L)'] = np.array(tabela.iloc[0, 2: :2])
    tabela_resumida.loc['Composição Rafinado (%)'] = (tabela_resumida.loc['Rafinado (mol/L)'] * 100
                                                        / tabela_resumida.loc['Rafinado (mol/L)'].sum())
    tabela_resumida.loc['Composição org. Carregado (%)'] = (tabela_resumida.loc['Carregado Orgânico (mol/L)']
                                                            * 100 / (tabela_resumida.loc['Carregado Orgânico (mol/L)']
                                                            .sum()))
    if isoterma.tipo == 'Extração':
        tabela_resumida.loc['Recuperação Rafinado (%)'] = (tabela_resumida.loc['Rafinado (mol/L)'] * 100
                                                            / tabela_resumida.loc['Alimentação aq. (mol/L)'])
    else:
        tabela_resumida.loc['Recuperação Rafinado (%)'] = ((tabela_resumida.loc['Alimentação org. (mol/L)']
                                                            - tabela_resumida.loc['Carregado Orgânico (mol/L)'])
                                                            * 100 / tabela_resumida.loc['Alimentação org. (mol/L)'])

    tabela_resumida.loc['Recuperação Orgânico (%)'] = 100 - tabela_resumida.loc['Recuperação Rafinado (%)']

    return tabela_resumida

def monta_grafico(isoterma):

    tabela = isoterma.monta_tabela(uso = 'externo')

    for elemento in isoterma.lista_elementos[1:]:
        posicao_na_lista = 1
        reta_operacional = np.concatenate(
                                            (
                                            [elemento.ca0_gl],
                                            np.array(tabela['[' + elemento.simbolo + ']aq(g/L)']),
                                            np.array(tabela['[' + elemento.simbolo + ']org(g/L)']),
                                            [elemento.con_gl]
                                            )
                                            ).reshape(2, isoterma.n_celulas + 1)

        estagios_aquoso = [reta_operacional[0, 0]]
        for n in range(1, isoterma.n_celulas + 1):
            estagios_aquoso += 2 * [reta_operacional[0, n]]

        estagios_organico = []
        for n in range(0, isoterma.n_celulas):
            estagios_organico += 2 * [reta_operacional[1, n]]
        estagios_organico += [reta_operacional[1, -1]]

        fig = plt.figure()
        axes = fig.add_axes([0, posicao_na_lista - 1.2, 1, 1])
        axes.plot(estagios_aquoso, estagios_organico, '.-', markersize = 8, label = "Estágios")
        axes.plot(reta_operacional[0, :], reta_operacional[1, :], '.-', markersize = 8, label = 'Reta de Operação')
        axes.plot(np.array(tabela['[' + elemento.simbolo + ']aq(g/L)']),
                    np.array(tabela['[' + elemento.simbolo + ']org(g/L)']),
                    '.-', markersize = 8, label = 'Reta de Equilíbrio')
        axes.set_xlabel('Aquoso')
        axes.set_ylabel('Orgânico')
        axes.set_ylim([0, None])
        axes.set_xlim([0, None])
        axes.legend(loc = 0)
        axes.set_title('Isoterma de ' + isoterma.tipo + ' de ' + elemento.nome)