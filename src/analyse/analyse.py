import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import threading
from time import sleep


def get_name_file(path_access: str, name_variable: str, simulation_index: int, value_variable: int) -> str:
    """
    Fonction qui renvoit le nom d' accès à un fichier résultat d' une simulation
    :param path_access: le chemin d' accès au répertoire où il se trouve
    :param name_variable: le nom de la variable simulée
    :param simulation_index: la valeur du nombre de node de la simulation
    :param value_variable: la valeur de la variable simulée

    :return: {path_access}/res_initial_node_{value_node}_{name_var}_{value_variable}.txt
    """
    # TODO: change name file to result
    return f"{path_access}res_{name_variable[1:]}_{value_variable}_simulation_n_{simulation_index}.txt"


def calcul_during_epidemic(variable_simulator: str, nb_simulations: int,
                           value_variables_begin: int, value_variable_end: int, incremented_variable: int,
                           path_directory: str, file_name_result):
    """
    Fonction qui me permet de calculé la durée de l' épidémie

    :param nb_simulations: Nombre de simulations effectué pour chaque valeur de la variable d' interet
    :param file_name_result: Nom du fichier dans lequel sauvegardé le dataFrame résultat de l' analyse
    :param variable_simulator: la variable simulé dont on veut avoir la durée
    :param value_variables_begin: la valeur initial de la variable simulée
    :param value_variable_end: la valeur finale de la variable simulée
    :param incremented_variable: la valeur d' incrémentation de la variable simulée
    :param path_directory: le chemin d' accès aux résultats de la simulations

    :return: un dataFrame contenant en index le nombre de node initial et
                en label la valeur de la variable de simulation:
            => index = list des numéros de la simulation; label = list valeurs variables; data = le nombre de snapshot
            ex: nombre initial d'infecté: index = n-ième simulation
                                        label = valeurs de la variable nombre initial d' infecté 1 -> 100
    """

    if variable_simulator not in {"-nb_infected", "-travel_distance", "-nb_vaccinated", "-vaccine_efficiency",
                                  "-infection_period", "-contagion_period", "-immune_period"}:
        raise Exception("Variable de simulation non reconnu")

    # supprime la possibilité de cycle infini
    if incremented_variable <= 0:
        return None
    if nb_simulations <= 0:
        return None

    dict_result = {}
    my_variable = value_variables_begin
    while value_variables_begin <= my_variable <= value_variable_end:
        index_simulation = 1
        list_index_simulations = []
        list_values = []
        while index_simulation <= nb_simulations:
            list_index_simulations.append(index_simulation)
            with open(get_name_file(path_access=path_directory, name_variable=variable_simulator[1:],
                                    simulation_index=index_simulation, value_variable=my_variable), 'rb') as f:
                result = f.read().decode('utf-8')
                list_line = result.split('\n')
                list_values.append(len(list_line) - 18)
            index_simulation += 1
        dict_result[my_variable] = pd.Series(list_values, index=list_index_simulations)
        my_variable += incremented_variable
    df = pd.DataFrame(dict_result)
    if file_name_result:
        df.to_csv(file_name_result)
    return df


def get_proportion_max_infected(list_line):
    """
    Fonction qui me permet de déterminer en fonction d' une liste de snapshot,
    la proportion maximale de la population qui est infectée.

    :param list_line: la liste des snapshot

    :return: le nombre maximal d' infecté qu' il y'a eu durant un moment t de l' épidémie
    """
    nb_max_infected = 0
    for line in list_line:
        list_nodes = line.split()
        nb_infected = 0
        for node in list_nodes:
            if int(node) in {1, 4}:
                nb_infected += 1
        if nb_infected > nb_max_infected:
            nb_max_infected = nb_infected
    return nb_max_infected


def get_proportion_infected(list_line):
    """
    Fonction qui me permet de déterminer en fonction d' une liste de snapshot,
    la proportion de la population qui est infecté durant l' épidémie
    (le nombre de noeuds qui ont été contaminé au au moins une fois durant l' épidémie)

    :param list_line: la liste des snapshot

    :return: la proportion d' infecté qu' il y'a eu durant un moment t de l' épidémie
    """
    set_nodes_infected = set()
    for line in list_line:
        list_nodes = line.split()
        for i in range(len(list_nodes)):
            if int(list_nodes[i]) in {1, 4}:
                set_nodes_infected |= {i}
    return len(set_nodes_infected)


def calcul_proportion_population_infected(variable_simulator: str, proportion_max: int, nb_simulations: int,
                                          value_variables_begin: int, value_variable_end: int,
                                          incremented_variable: int, path_directory: str, file_name_result):
    """
    Fonction qui me permet de calculé la durée de l' épidémie

    :param proportion_max: Variable qui me permet de préciser s'il s'agit d'une proportion maximale ou simple
            {(0) => simple proportion, (!= 0) => proportion max}
    :param nb_simulations: Nombre de simulation faites pour chaque valeur de la variable
    :param file_name_result: Nom du fichier dans lequel sauvegardé le dataFrame résultat de l' analyse
    :param variable_simulator: la variable simulé dont on veut avoir la durée
    :param value_variables_begin: la valeur initial de la variable simulée
    :param value_variable_end: la valeur finale de la variable simulée
    :param incremented_variable: la valeur d' incrémentation de la variable simulée
    :param path_directory: le chemin d' accès aux résultats de la simulations

    :return: un dataFrame contenant en index le nombre de node initial et
                en label la valeur de la variable de simulation:
            => index = list des numéros de la simulation; label = list valeurs variables; data = le nombre de snapshot
            ex: nombre initial d'infecté: index = n-ième simulation 1 -> 100
                                          label = valeurs de la variable nombre initial d' infecté 1 -> 100
    """

    if variable_simulator not in {"-nb_infected", "-travel_distance", "-nb_vaccinated", "-vaccine_efficiency",
                                  "-infection_period", "-contagion_period", "-immune_period"}:
        raise Exception("Variable de simulation non reconnu")

    # supprime la possibilité de cycle infini
    if incremented_variable <= 0:
        return None
    if nb_simulations <= 0:
        return None

    dict_result = {}
    my_variable = value_variables_begin
    while value_variables_begin <= my_variable <= value_variable_end:
        index_simulation = 1
        list_index_simulations = []
        list_values = []
        while index_simulation <= nb_simulations:
            list_index_simulations.append(index_simulation)
            with open(get_name_file(path_access=path_directory, name_variable=variable_simulator[1:],
                                    simulation_index=index_simulation, value_variable=my_variable), 'rb') as f:
                result = f.read().decode('utf-8')
                list_line = result.split('\n')[18:]
                if proportion_max == 0:
                    list_values.append(get_proportion_infected(list_line=list_line))
                else:
                    list_values.append(get_proportion_max_infected(list_line=list_line))
            index_simulation += 1
        dict_result[my_variable] = pd.Series(list_values, index=list_index_simulations)
        my_variable += incremented_variable
    df = pd.DataFrame(dict_result)
    df.to_csv(file_name_result)
    return df


def get_proportion_multi_infection(list_line):
    """
    Fonction qui me permet de déterminer en fonction d' une liste de snapshot,
    la proportion des multi-infections qu' il y a eu durant l' épidémie

    :param list_line: la liste des snapshot

    :return: un dictionnaire key = nombre de fois qu'un noeud a été infecté et
                             value = nombre de noeud qui a été infecté 'key' fois
    """
    nb_nodes = 1
    # dict_nodes_immune = ensemble des noeuds infectés durant toute la simulation
    dict_nodes_infected = dict()
    # set_nodes_immune = ensemble des nodes saint à la ligne précédente (au temps t-1)
    set_nodes_immune = set()
    # me permet de mettre à 0, le compteur des noeuds qui n' ont pas été infectP
    for i in range(nb_nodes):
        dict_nodes_infected[i] = 0
        set_nodes_immune |= {i}
    for line in list_line:
        list_nodes = line.split()
        for i in range(len(list_nodes)):
            if int(list_nodes[i]) in {0, 3}:
                set_nodes_immune |= {i}
            elif int(list_nodes[i]) in {1, 4}:
                if i in set_nodes_immune:
                    dict_nodes_infected[i] = 1
                    set_nodes_immune -= {i}
    return dict_nodes_infected


def calcul_proportion_multi_infection(variable_simulator: str, nb_simulations: int, value_variables_begin: int,
                                      value_variable_end: int, incremented_variable: int,
                                      path_directory: str, file_name_result):
    """
    Fonction qui me permet de calculé la distribution des multi-infections durant une épidémie

    :param nb_simulations: Nombre de simulations effectué pour chaque valeur de la variable d'interet
    :param file_name_result: Nom du fichier dans lequel sauvegardé le dataFrame résultat de l' analyse
    :param variable_simulator: la variable simulé dont on veut avoir la durée
    :param value_variables_begin: la valeur initial de la variable simulée
    :param value_variable_end: la valeur finale de la variable simulée
    :param incremented_variable: la valeur d' incrémentation de la variable simulée
    :param path_directory: le chemin d' accès aux résultats de la simulations

    :return: un dataFrame contenant en index le nombre de node initial et
                en label la valeur de la variable de simulation:
            => index = list des numéros de la simulation; label = list valeurs variables; data = le nombre de snapshot
            ex: nombre initial d'infecté: index = n-ième simulation 1 -> 100
                                          label = valeurs de la variable nombre initial d' infecté 1 -> 100
    """

    if variable_simulator not in {"-nb_infected", "-travel_distance", "-nb_vaccinated", "-vaccine_efficiency",
                                  "-infection_period", "-contagion_period", "-immune_period"}:
        raise Exception(f"Variable de simulation non reconnu {variable_simulator}")

    # supprime la possibilité de cycle infini
    if incremented_variable <= 0:
        return None
    if nb_simulations <= 0:
        return None

    dict_result = {}
    my_variable = value_variables_begin
    while value_variables_begin <= my_variable <= value_variable_end:
        index_simulation = 1
        list_index_simulations = []
        list_values = []
        while index_simulation <= nb_simulations:
            list_index_simulations.append(index_simulation)
            with open(get_name_file(path_access=path_directory, name_variable=variable_simulator[1:],
                                    simulation_index=index_simulation, value_variable=my_variable), 'rb') as f:
                result = f.read().decode('utf-8')
                list_line = result.split('\n')[18:]
                list_values.append(get_proportion_multi_infection(list_line=list_line))
            index_simulation += 1
        dict_result[my_variable] = pd.Series(list_values, index=list_index_simulations)
        my_variable += incremented_variable
    df = pd.DataFrame(dict_result)
    df.to_csv(file_name_result)


def analyse_variable(variable_simulator: str, nb_simulations: int,
                     value_variables_begin: int, value_variable_end: int, incremented_variable: int,
                     path_directory_files_simulations: str, path_directory_files_result_analyse: str,
                     files_result: dict):

    if variable_simulator not in {"-nb_infected", "-travel_distance", "-nb_vaccinated", "-vaccine_efficiency",
                                  "-infection_period", "-contagion_period", "-immune_period"}:
        raise Exception(f"Variable de simulation non reconnu {variable_simulator}")

    if path_directory_files_result_analyse:
        if path_directory_files_result_analyse[-1] != '/':
            path_directory_files_result_analyse += '/'

    # calcul during epidemic
    calcul_during_epidemic(variable_simulator=variable_simulator, nb_simulations=nb_simulations,
                           value_variables_begin=value_variables_begin, value_variable_end=value_variable_end,
                           incremented_variable=incremented_variable, path_directory=path_directory_files_simulations,
                           file_name_result=path_directory_files_result_analyse + files_result['during'])

    # calcul proportion population infected
    if variable_simulator == "-nb_infected":
        p_max = 1
    else:
        p_max = 0
    calcul_proportion_population_infected(variable_simulator=variable_simulator, proportion_max=p_max,
                                          nb_simulations=nb_simulations,
                                          value_variables_begin=value_variables_begin,
                                          value_variable_end=value_variable_end,
                                          incremented_variable=incremented_variable,
                                          path_directory=path_directory_files_simulations,
                                          file_name_result=f"{path_directory_files_result_analyse}"
                                                           f"{files_result['proportion population']}")

    # calcul proportion multi-infection
    calcul_proportion_multi_infection(variable_simulator=variable_simulator, nb_simulations=nb_simulations,
                                      value_variables_begin=value_variables_begin,
                                      value_variable_end=value_variable_end,
                                      incremented_variable=incremented_variable,
                                      path_directory=path_directory_files_simulations,
                                      file_name_result=f"{path_directory_files_result_analyse}"
                                                       f"{files_result['multi infection']}")


figure_number = 1


def draw_graph(file_csv, file_pdf, title_graph, x_label, y_label):
    df = pd.read_csv(file_csv, index_col=0)
    df = df.T.mean(1)
    global figure_number
    plt.figure(figure_number)
    figure_number += 1
    df.plot()
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title_graph)
    plt.savefig(file_pdf)


def get_graph(name_variable, path_files, files_analyse, files_result):
    print(f">>> graph for {name_variable}")
    for key in files_analyse.keys():
        print(f">>>>> ")


if __name__ == '__main__':
    all_variables = {"-nb_infected": {"variable_simulator": "-nb_infected",
                                      "nb_simulations": 100,
                                      "value_variables_begin": 1,
                                      "value_variable_end": 10,
                                      "incremented_variable": 1,
                                      "path_directory_files_simulations":
                                          "../simulator/result_simulations/infected",
                                      "path_directory_files_result_analyse":
                                          "result_analyse/infected",
                                      "files result analyse": {"during": "infected_during.csv",
                                                               "proportion population": "infected_proportion.csv",
                                                               "multi infection": "infected_multi_infection.csv"
                                                               },
                                      "file result graph": {"during": "infected_during.pdf",
                                                            "proportion population": "infected_proportion.pdf",
                                                            "multi infection": "infected_multi_infection.pdf"
                                                            }
                                      },
                     "-travel_distance": {"variable_simulator": "-travel_distance",
                                          "nb_simulations": 100,
                                          "value_variables_begin": 150,
                                          "value_variable_end": 250,
                                          "incremented_variable": 10,
                                          "path_directory_files_simulations":
                                              "../simulator/result_simulations/travel_distance",
                                          "path_directory_files_result_analyse":
                                              "result_analyse/travel_distance",
                                          "files result analyse": {"during": "travel_distance_during.csv",
                                                                   "proportion population":
                                                                       "travel_distance_proportion.csv",
                                                                   "multi infection":
                                                                       "travel_distance_multi_infection.csv"
                                                                   },
                                          "files result graph": {"during": "travel_distance_during.pdf",
                                                                 "proportion population":
                                                                     "travel_distance_proportion.pdf",
                                                                 "multi infection":
                                                                     "travel_distance_multi_infection.pdf"
                                                                 }
                                          },
                     "-nb_vaccinated": {"variable_simulator": "-nb_vaccinated",
                                        "nb_simulations": 100,
                                        "value_variables_begin": 0,
                                        "value_variable_end": 10,
                                        "incremented_variable": 1,
                                        "path_directory_files_simulations":
                                            "../simulator/result_simulations/nb_vaccinated",
                                        "path_directory_files_result_analyse":
                                            "result_analyse/vaccinated",
                                        "files result analyse": {"during": "vaccinated_during.csv",
                                                                 "proportion population": "vaccinated_proportion.csv",
                                                                 "multi infection": "vaccinated_multi_infection.csv"
                                                                 },
                                        "files result graph": {"during": "vaccinated_during.pdf",
                                                               "proportion population": "vaccinated_proportion.pdf",
                                                               "multi infection": "vaccinated_multi_infection.pdf"
                                                               }
                                        },
                     "-vaccine_efficiency": {"variable_simulator": "-vaccine_efficiency",
                                             "nb_simulations": 100,
                                             "value_variables_begin": 1,
                                             "value_variable_end": 10,
                                             "incremented_variable": 1,
                                             "path_directory_files_simulations":
                                                 "../simulator/result_simulations/vaccine_efficiency",
                                             "path_directory_files_result_analyse":
                                                 "result_analyse/vaccine_efficiency",
                                             "files result analyse": {"during": "vaccine_efficiency_during.csv",
                                                                      "proportion population":
                                                                          "vaccine_efficiency_proportion.csv",
                                                                      "multi infection":
                                                                          "vaccine_efficiency_multi_infection.csv"
                                                                      },
                                             "files result graph": {"during": "vaccine_efficiency_during.pdf",
                                                                    "proportion population":
                                                                        "vaccine_efficiency_proportion.pdf",
                                                                    "multi infection":
                                                                        "vaccine_efficiency_multi_infection.pdf"
                                                                    }
                                             },
                     "-infection_period": {"variable_simulator": "-infection_period",
                                           "nb_simulations": 100,
                                           "value_variables_begin": 50,
                                           "value_variable_end": 150,
                                           "incremented_variable": 10,
                                           "path_directory_files_simulations":
                                               "../simulator/result_simulations/infection_period",
                                           "path_directory_files_result_analyse":
                                               "result_analyse/infection_period",
                                           "files result analyse": {"during": "infection_period_during.csv",
                                                                    "proportion population":
                                                                        "infection_period_proportion.csv",
                                                                    "multi infection":
                                                                        "infection_period_multi_infection.csv"
                                                                    },
                                           "files result graph": {"during": "infection_period_during.pdf",
                                                                  "proportion population":
                                                                      "infection_period_proportion.pdf",
                                                                  "multi infection":
                                                                      "infection_period_multi_infection.pdf"
                                                                  }
                                           },
                     "-contagion_period": {"variable_simulator": "-contagion_period",
                                           "nb_simulations": 100,
                                           "value_variables_begin": 150,
                                           "value_variable_end": 300,
                                           "incremented_variable": 10,
                                           "path_directory_files_simulations":
                                               "../simulator/result_simulations/contagion_period",
                                           "path_directory_files_result_analyse":
                                               "result_analyse/contagion_period",
                                           "files result analyse": {"during": "contagion_period_during.csv",
                                                                    "proportion population":
                                                                        "contagion_period_proportion.csv",
                                                                    "multi infection":
                                                                        "contagion_period_multi_infection.csv"
                                                                    },
                                           "files result graph": {"during": "contagion_period_during.pdf",
                                                                  "proportion population":
                                                                        "contagion_period_proportion.pdf",
                                                                  "multi infection":
                                                                        "contagion_period_multi_infection.pdf"
                                                                  }
                                           },
                     "-immune_period": {"variable_simulator": "-immune_period",
                                        "nb_simulations": 100,
                                        "value_variables_begin": 200,
                                        "value_variable_end": 400,
                                        "incremented_variable": 10,
                                        "path_directory_files_simulations":
                                            "../simulator/result_simulations/immune_period",
                                        "path_directory_files_result_analyse":
                                            "result_analyse/immune_period",
                                        "files result analyse": {"during": "immune_period_during.csv",
                                                                 "proportion population":
                                                                     "immune_period_proportion.csv",
                                                                 "multi infection": "immune_period_multi_infection.csv"
                                                                 },
                                        "files result graph": {"during": "immune_period_during.pdf",
                                                               "proportion population":
                                                                   "immune_period_proportion.pdf",
                                                               "multi infection": "immune_period_multi_infection.pdf"
                                                               }
                                        },
                     "-nb_nodes": {"variable_simulator": "-nb_nodes",
                                   "nb_simulations": 100,
                                   "value_variables_begin": 100,
                                   "value_variable_end": 150,
                                   "incremented_variable": 10,
                                   "path_directory_files_simulations":
                                       "../simulator/result_simulations/nodes",
                                   "path_directory_files_result_analyse":
                                       "result_analyse/nodes",
                                   "files result analyse": {"during": "nodes_during.csv",
                                                            "proportion population": "nodes_proportion.csv",
                                                            "multi infection": "nodes_multi_infection.csv"
                                                            },
                                   "files result graph": {"during": "nodes_during.pdf",
                                                          "proportion population": "nodes_proportion.pdf",
                                                          "multi infection": "nodes_multi_infection.pdf"
                                                          }
                                   }
                     }

    for variable in all_variables.keys():
        param = all_variables[variable]
        threading.Thread(target=analyse_variable,
                         args=(param['variable_simulator'],
                               param['nb_simulations'],
                               param['value_variables_begin'],
                               param['value_variable_end'],
                               param['incremented_variable'],
                               param['path_directory_files_simulations'],
                               param['path_directory_files_result_analyse'],
                               param['files result analyse'], )
                         ).start()

    while threading.active_count() > 1:
        sleep(5)
