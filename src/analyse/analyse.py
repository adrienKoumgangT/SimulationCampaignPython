from numpy import *
from pandas import *
from matplotlib import pyplot


def get_name_file(path_access, name_variable, value_node, value_variable):
    """
    Fonction qui renvoit le nom d' accès à un fichier résultat d' une simulation
    :param path_access: le chemin d' accès au répertoire où il se trouve
    :param name_variable: le nom de la variable simulée
    :param value_node: la valeur du nombre de node de la simulation
    :param value_variable: la valeur de la variable simulée

    :return: {path_access}/res_initial_node_{value_node}_{name_var}_{value_variable}.txt
    """

    return f"{path_access}/res_initial_node_{value_node}_{name_variable}_{value_variable}.txt"


def calcul_during_epidemic(variable_simulator: str, nb_nodes_begin: int, nb_nodes_end: int, incremented_node: int,
                           values_variables_begin: int, value_variable_end: int, incremented_variable: int,
                           path_directory: str, file_name_result):
    """
    Fonction qui me permet de calculé la durée de l' épidémie

    :param file_name_result: Nom du fichier dans lequel sauvegardé le dataFrame résultat de l' analyse
    :param variable_simulator: la variable simulé dont on veut avoir la durée
    :param nb_nodes_begin: le nombre de noeuds initial durant la simulation de 'variable simulator'
    :param nb_nodes_end: le nombre de noeuds final durant la simulation de 'variable simulator'
    :param incremented_node: l' incrémentation du nombre de noeuds durant la simulation
    :param values_variables_begin: la valeur initial de la variable simulée
    :param value_variable_end: la valeur finale de la variable simulée
    :param incremented_variable: la valeur d' incrémentation de la variable simulée
    :param path_directory: le chemin d' accès aux résultats de la simulations

    :return: un dataFrame contenant en index le nombre de node initial et
                en label la valeur de la variable de simulation:
            => index = list nodes; label = list valeurs variables; data = le nombre de snapshot
            ex: nombre initial d'infecté: index = valeurs du nombre de nodes 100 -> 300
                                        label = valeurs de la variable nombre initial d' infecté 1 -> 100
    """

    if variable_simulator == "infected":
        variable_name = 'initial_infected'
    elif variable_simulator == "travel":
        variable_name = 'initial_travel_distance'
    elif variable_simulator == "vaccinated":
        variable_name = 'initial_vaccinated'
    elif variable_simulator == "vaccine efficiency":
        variable_name = 'vaccine_efficiency'
    elif variable_simulator == "infection period":
        variable_name = 'initial_infection_period'
    elif variable_simulator == "contagion period":
        variable_name = 'initial_contagion_period'
    elif variable_simulator == "immune period":
        variable_name = 'initial_immune_period'
    else:
        raise Exception("Variable de simulation non reconnu")

    dict_result = {}
    my_variable = values_variables_begin
    while my_variable <= value_variable_end:
        my_var_node = nb_nodes_begin
        list_nodes = []
        list_values = []
        while my_var_node <= nb_nodes_end:
            list_nodes.append(my_var_node)
            with open(get_name_file(path_access=path_directory, name_variable=variable_name, value_node=my_var_node,
                                    value_variable=my_variable), 'rb') as f:
                result = f.read().decode('utf-8')
                list_line = result.split('\n')
                list_values.append(len(list_line) - 18)
            my_var_node += incremented_node
        dict_result[my_variable] = list_values, list_nodes
        my_variable += incremented_variable
    df = DataFrame(dict_result)
    df.to_csv(file_name_result)


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


def calcul_proportion_max_population_infected(variable_simulator: str, nb_nodes_begin: int, nb_nodes_end: int,
                                              incremented_node: int, values_variables_begin: int,
                                              value_variable_end: int, incremented_variable: int,
                                              path_directory: str, file_name_result):
    """
    Fonction qui me permet de calculé la durée de l' épidémie

    :param file_name_result: Nom du fichier dans lequel sauvegardé le dataFrame résultat de l' analyse
    :param variable_simulator: la variable simulé dont on veut avoir la durée
    :param nb_nodes_begin: le nombre de noeuds initial durant la simulation de 'variable simulator'
    :param nb_nodes_end: le nombre de noeuds final durant la simulation de 'variable simulator'
    :param incremented_node: l' incrémentation du nombre de noeuds durant la simulation
    :param values_variables_begin: la valeur initial de la variable simulée
    :param value_variable_end: la valeur finale de la variable simulée
    :param incremented_variable: la valeur d' incrémentation de la variable simulée
    :param path_directory: le chemin d' accès aux résultats de la simulations

    :return: un dataFrame contenant en index le nombre de node initial et
                en label la valeur de la variable de simulation:
            => index = list nodes; label = list valeurs variables; data = le nombre de snapshot
            ex: nombre initial d'infecté: index = valeurs du nombre de nodes 100 -> 300
                                        label = valeurs de la variable nombre initial d' infecté 1 -> 100
    """

    if variable_simulator == "infected":
        variable_name = 'initial_infected'
    elif variable_simulator == "travel":
        variable_name = 'initial_travel_distance'
    elif variable_simulator == "vaccinated":
        variable_name = 'initial_vaccinated'
    elif variable_simulator == "vaccine efficiency":
        variable_name = 'vaccine_efficiency'
    elif variable_simulator == "infection period":
        variable_name = 'initial_infection_period'
    elif variable_simulator == "contagion period":
        variable_name = 'initial_contagion_period'
    elif variable_simulator == "immune period":
        variable_name = 'initial_immune_period'
    else:
        raise Exception("Variable de simulation non reconnu")

    dict_result = {}
    my_variable = values_variables_begin
    while my_variable <= value_variable_end:
        my_var_node = nb_nodes_begin
        list_nodes = []
        list_values = []
        while my_var_node <= nb_nodes_end:
            list_nodes.append(my_var_node)
            with open(get_name_file(path_access=path_directory, name_variable=variable_name, value_node=my_var_node,
                                    value_variable=my_variable), 'rb') as f:
                result = f.read().decode('utf-8')
                list_line = result.split('\n')[18:]
                # get_proportion_infected(list_line) : renvoit le nombre maximal de noeuds qui ont été infecté à
                # n' importe quel moment t
                list_values.append(get_proportion_infected(list_line=list_line))
            my_var_node += incremented_node
        dict_result[my_variable] = list_values, list_nodes
        my_variable += incremented_variable
    df = DataFrame(dict_result)
    df.to_csv(file_name_result)


def calcul_proportion_population_infected(variable_simulator: str, nb_nodes_begin: int, nb_nodes_end: int,
                                          incremented_node: int, values_variables_begin: int,
                                          value_variable_end: int, incremented_variable: int,
                                          path_directory: str, file_name_result):
    """
    Fonction qui me permet de calculé la proportion de la population infectée

    :param file_name_result: Nom du fichier dans lequel sauvegardé le dataFrame résultat de l' analyse
    :param variable_simulator: la variable simulé dont on veut avoir la durée
    :param nb_nodes_begin: le nombre de noeuds initial durant la simulation de 'variable simulator'
    :param nb_nodes_end: le nombre de noeuds final durant la simulation de 'variable simulator'
    :param incremented_node: l' incrémentation du nombre de noeuds durant la simulation
    :param values_variables_begin: la valeur initial de la variable simulée
    :param value_variable_end: la valeur finale de la variable simulée
    :param incremented_variable: la valeur d' incrémentation de la variable simulée
    :param path_directory: le chemin d' accès aux résultats de la simulations

    :return: un dataFrame contenant en index le nombre de node initial et
                en label la valeur de la variable de simulation:
            => index = list nodes; label = list valeurs variables; data = le nombre de snapshot
            ex: nombre initial d'infecté: index = valeurs du nombre de nodes 100 -> 300
                                        label = valeurs de la variable nombre initial d' infecté 1 -> 100
    """

    if variable_simulator == "infected":
        variable_name = 'initial_infected'
    elif variable_simulator == "travel":
        variable_name = 'initial_travel_distance'
    elif variable_simulator == "vaccinated":
        variable_name = 'initial_vaccinated'
    elif variable_simulator == "vaccine efficiency":
        variable_name = 'vaccine_efficiency'
    elif variable_simulator == "infection period":
        variable_name = 'initial_infection_period'
    elif variable_simulator == "contagion period":
        variable_name = 'initial_contagion_period'
    elif variable_simulator == "immune period":
        variable_name = 'initial_immune_period'
    else:
        raise Exception("Variable de simulation non reconnu")

    dict_result = {}
    my_variable = values_variables_begin
    while my_variable <= value_variable_end:
        my_var_node = nb_nodes_begin
        list_nodes = []
        list_values = []
        while my_var_node <= nb_nodes_end:
            list_nodes.append(my_var_node)
            with open(get_name_file(path_access=path_directory, name_variable=variable_name, value_node=my_var_node,
                                    value_variable=my_variable), 'rb') as f:
                result = f.read().decode('utf-8')
                list_line = result.split('\n')[18:]
                # get_proportion_infected(list_line) : renvoit le nombre de noeud qui ont été infecté au moins 1e fois
                list_values.append(get_proportion_infected(list_line=list_line))
            my_var_node += incremented_node
        dict_result[my_variable] = list_values, list_nodes
        my_variable += incremented_variable
    df = DataFrame(dict_result)
    df.to_csv(file_name_result)


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
#


def calcul_proportion_multi_infection(variable_simulator: str, nb_nodes_begin: int, nb_nodes_end: int,
                                      incremented_node: int, values_variables_begin: int,
                                      value_variable_end: int, incremented_variable: int,
                                      path_directory: str, file_name_result):
    """
    Fonction qui me permet de calculé la distribution des multi-infections durant une épidémie

    :param file_name_result: Nom du fichier dans lequel sauvegardé le dataFrame résultat de l' analyse
    :param variable_simulator: la variable simulé dont on veut avoir la durée
    :param nb_nodes_begin: le nombre de noeuds initial durant la simulation de 'variable simulator'
    :param nb_nodes_end: le nombre de noeuds final durant la simulation de 'variable simulator'
    :param incremented_node: l' incrémentation du nombre de noeuds durant la simulation
    :param values_variables_begin: la valeur initial de la variable simulée
    :param value_variable_end: la valeur finale de la variable simulée
    :param incremented_variable: la valeur d' incrémentation de la variable simulée
    :param path_directory: le chemin d' accès aux résultats de la simulations

    :return: un dataFrame contenant en index le nombre de node initial et
                en label la valeur de la variable de simulation:
            => index = list nodes; label = list valeurs variables; data = le nombre de snapshot
            ex: nombre initial d'infecté: index = valeurs du nombre de nodes 100 -> 300
                                        label = valeurs de la variable nombre initial d' infecté 1 -> 100
    """

    if variable_simulator == "infected":
        variable_name = 'initial_infected'
    elif variable_simulator == "travel":
        variable_name = 'initial_travel_distance'
    elif variable_simulator == "vaccinated":
        variable_name = 'initial_vaccinated'
    elif variable_simulator == "vaccine efficiency":
        variable_name = 'vaccine_efficiency'
    elif variable_simulator == "infection period":
        variable_name = 'initial_infection_period'
    elif variable_simulator == "contagion period":
        variable_name = 'initial_contagion_period'
    elif variable_simulator == "immune period":
        variable_name = 'initial_immune_period'
    else:
        raise Exception("Variable de simulation non reconnu")

    dict_result = {}
    my_variable = values_variables_begin
    while my_variable <= value_variable_end:
        my_var_node = nb_nodes_begin
        list_nodes = []
        list_values = []
        while my_var_node <= nb_nodes_end:
            list_nodes.append(my_var_node)
            with open(get_name_file(path_access=path_directory, name_variable=variable_name, value_node=my_var_node,
                                    value_variable=my_variable), 'rb') as f:
                result = f.read().decode('utf-8')
                list_line = result.split('\n')[18:]
                # get_proportion_infected(list_line) : renvoit le nombre de noeud qui ont été infecté au moins 1e fois
                list_values.append(get_proportion_infected(list_line=list_line))
            my_var_node += incremented_node
        dict_result[my_variable] = list_values, list_nodes
        my_variable += incremented_variable
    df = DataFrame(dict_result)
    df.to_csv(file_name_result)


def analyse_files(variable_simulator, file_result_during, file_result_proportion, file_result_distribution):
    if variable_simulator == "infected":
        variable_name = 'initial_infected'
    elif variable_simulator == "travel":
        variable_name = 'initial_travel_distance'
    elif variable_simulator == "vaccinated":
        variable_name = 'initial_vaccinated'
    elif variable_simulator == "vaccine efficiency":
        variable_name = 'vaccine_efficiency'
    elif variable_simulator == "infection period":
        variable_name = 'initial_infection_period'
    elif variable_simulator == "contagion period":
        variable_name = 'initial_contagion_period'
    elif variable_simulator == "immune period":
        variable_name = 'initial_immune_period'
    else:
        raise Exception("Variable de simulation non reconnu")

    calcul_during_epidemic(variable_simulator='infected', nb_nodes_begin=100, nb_nodes_end=500,
                           incremented_node=10, values_variables_begin=1, value_variable_end=100,
                           incremented_variable=1, path_directory='infected', file_name_result=file_result_during)


def analyse_nb_infected(file_csv_during):
    df = read_csv(file_csv_during, index_col=0)
