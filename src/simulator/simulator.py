import subprocess
import sys


def get_name_variable(name_var: int) -> str:
    if name_var == 0:
        return "-nb_nodes"
    elif name_var == 1:
        return "-nb_infected"
    elif name_var == 2:
        return "-travel_distance"
    elif name_var == 3:
        return "-nb_vaccinated"
    elif name_var == 4:
        return "-vaccine_efficiency"
    elif name_var == 5:
        return "-infection_period"
    elif name_var == 6:
        return "-contagion_period"
    elif name_var == 7:
        return "-immune_period"
    else:
        return "unknown"


def get_help(name_software: str) -> str:
    return f"Software that allows you to launch the simulation of the epidemic according to a certain variable.\n\n" \
           f"Syntax: {name_software} -name_var=name [-number_of_initial_node_begin=x] [-number_of_initial_node_end=x]" \
           f" [-nb_node_incremented=x]\n" \
           f"                       [-variable_value_begin=x] [-variable_value_end=x] [-var_value_incremented=x]\n" \
           f"                       [-other_interest_var=list_var]\n" \
           f"                       [-path_save_result=pathname]\n" \
           f"\n" \
           f"\t -name_var:         [name] name of the variable of interest\n" \
           f"\t                         [=0] for nb nodes\n" \
           f"\t                         [=1] for nb infected\n" \
           f"\t                         [=2] for travel distance\n" \
           f"\t                         [=3] for nb vaccinated\n" \
           f"\t                         [=4] for vaccine efficiency\n" \
           f"\t                         [=5] for infection period\n" \
           f"\t                         [=6] for contagion period\n" \
           f"\t                         [=7] for immune period\n" \
           f"\t -number_of_initial_node_begin:         [=x] initial total nodes for the beginning simulations\n" \
           f"\t -number_of_initial_node_end:           [=x] initial total nodes for the ending simulations\n" \
           f"\t -nb_node_incremented:   [=x] increment value for total nodes for simulations\n" \
           f"\t -variable_value_begin:       [=x] initial value for variable simulation for the simulations\n" \
           f"\t -variable_value_end:         [=x] final value for variable simulation for the simulations\n" \
           f"\t -var_value_incremented: [=x] increment value for variable simulation\n" \
           f"\n" \
           f"\t -other_interest_var:    [=list_var] list of other parameters to switch to the simulator\n" \
           f"\t                            ex: -stop_all_sane=1,-gui=0,-printout=2\n" \
           f"\n" \
           f"\t -path_save_result:      [=pathname] path to directory where save file to result of the simulator\n"


def get_simulator_info():
    return f"---------\n" \
           f"Simulator parameters:\n" \
           f"Using {get_name_variable(name_variable)} variable to interest.\n" \
           f"Using {nb_nodes_begin} as initial value for the initial number of node.\n" \
           f"Using {nb_nodes_end} as final value for the initial number of node." \
           f"Using {nb_nodes_incremented} as value for increment number of node during the simulation\n" \
           f"Using {var_value_begin} as initial value for the initial value for the variable to interest\n" \
           f"Using {var_value_end} as final value for the initial value for the variable to interest\n" \
           f"Using {var_incremented_value} as value for increment number of variable to interest during" \
           f" the simulation\n" \
           f"Using {list_other_parameter_simulator} for other parameter simulator\n" \
           f"Using {pathname} to directory where save files result to the simulator\n" \
           f"---------\n"


def get_info_values_nodes(name_var: int):
    if name_var in {1, 2, 3, 4, 5, 6, 7}:
        # nb = 41 [100 -> 500]; shift = 10
        return 100, 500, 10
    else:
        # nb = 1 [100]; shift = 0
        return 100, 100, 0


def get_info_values_var(name_var: int):
    if name_var == 1:
        # var = "nb infected"; nb = 50 [1 -> 50]; shift = 1
        return 1, 50, 1
    elif name_var == 2:
        # var = "travel distance"; nb = 20 [100 -> 300]; shift = 10
        return 100, 300, 10
    elif name_var == 3:
        # var = "nb vaccinated"; nb = 51 [0 -> 51]; shift = 1
        return 0, 50, 1
    elif name_var == 4:
        # var = "vaccine efficiency"; nb = 5 [1 -> 5]; shift = 1
        return 1, 5, 1
    elif name_var == 5:
        # var = "infection period"; nb = 51 [50 -> 150]; shift = 2
        return 50, 150, 2
    elif name_var == 6:
        # var = "contagion period"; nb = 101 [100 -> 300]; shift = 2
        return 100, 300, 2
    elif name_var == 7:
        # var = "immune period"; nb = 41 [100 -> 500]; shift = 10
        return 100, 500, 10
    else:
        # nb = 1 [100]; shift = 0
        return 100, 100, 0

# TODO: regarder le cas où la variable principale est celle du nombre de noeud


def run_simulator(variable_interest: str, variable_value_begin: int, variable_value_end: int,
                  variable_incremented_value: int,
                  number_of_initial_node_begin: int, number_of_initial_node_end: int, incremented_node: int,
                  list_other_interest_var: list, path_directory: str):

    def do_simulation(value_of_variable: int, nb_nodes: int):
        list_arg = ['java', '-jar', 'Virus.jar', '-nb_nodes=' + str(nb_nodes),
                    variable_interest + '=' + str(value_of_variable),
                    '-stop_all_sane=1', '-gui=0', '-printout=2']
        for other_arg in list_other_interest_var:
            list_arg.append(other_arg)
        res = subprocess.run(list_arg, capture_output=True)
        with open(path_directory + 'res_initial_nodes_' + str(nb_nodes) + '_value_variable_' +
                  str(var_value) + '.txt', 'w') as file_result:
            file_result.write(res.stdout.decode('utf-8'))

    # Pour empêcher des cycle infini
    if incremented_node <= 0:
        incremented_node = 1
    if variable_incremented_value <= 0:
        variable_incremented_value = 1
    if number_of_initial_node_begin > number_of_initial_node_end:
        val_inter = number_of_initial_node_end
        number_of_initial_node_end = number_of_initial_node_begin
        number_of_initial_node_begin = val_inter
    if variable_value_begin > variable_value_end:
        val_inter = variable_value_end
        variable_value_end = variable_value_begin
        variable_value_begin = val_inter

    # début de la simulation
    var_nb_nodes = number_of_initial_node_begin
    while var_nb_nodes <= number_of_initial_node_end:
        print(f"\nSimulation for a number of nodes = {var_nb_nodes}")
        var_value = variable_value_begin
        while var_value <= variable_value_end:
            print(f"\t-> Simulation for {variable_interest} = {var_value}")
            do_simulation(value_of_variable=var_value, nb_nodes=var_nb_nodes)
            var_value += variable_incremented_value
        var_nb_nodes += incremented_node


if __name__ == '__main__':
    # variable par défaut de la simulation : nb nodes
    name_variable = 0
    var_interest = "-nb_nodes"
    # valeurs par défaut pour le nombre de nodes de la simulation
    nb_nodes_begin = 100
    nb_nodes_end = 100
    nb_nodes_incremented = 10
    # valeurs par défaut pour la variable d' interet de la simulation
    var_value_begin = 0
    var_value_end = 0
    var_incremented_value = 1
    # autres paramètres avec valeurs à passer au simulateur
    list_other_parameter_simulator = []
    # chemin d' accès au dossier où sauvegarder les fichiers résultats des simulations
    pathname = "."

    if len(sys.argv) == 1:
        print(get_help(name_software=sys.argv[0]))
        exit(0)
    else:
        for argument in sys.argv:
            option = argument.split("=")
            if option[0] == "-name_var":
                name_variable = int(option[1])
            elif option[0] == "-number_of_initial_node_begin":
                nb_nodes_begin = int(option[1])
            elif option[0] == "-number_of_initial_node_end":
                nb_nodes_end = int(option[2])
            elif option[0] == "-nb_node_incremented":
                nb_nodes_incremented = int(option[1])
            elif option[0] == "-variable_value_begin":
                var_value_begin = int(option[1])
            elif option[0] == "-variable_value_end":
                var_value_end = int(option[1])
            elif option[0] == "-var_value_incremented":
                var_incremented_value = int(option[1])
            elif option[0] == "-other_interest_var":
                index_first_equal = argument.index('=')
                list_other_parameter = argument[index_first_equal+1:]
                list_other_parameter_simulator = list_other_parameter.split(",")
            elif option[0] == "-path_save_result":
                pathname = option[1]
        print(get_simulator_info())

    if name_variable in {0, 1, 2, 3, 4, 5, 6, 7}:
        run_simulator(variable_interest=var_interest, variable_value_begin=var_value_begin,
                      variable_value_end=var_value_end, variable_incremented_value=var_incremented_value,
                      number_of_initial_node_begin=nb_nodes_begin, number_of_initial_node_end=nb_nodes_end,
                      incremented_node=nb_nodes_incremented, list_other_interest_var=list_other_parameter_simulator,
                      path_directory=pathname)

    else:
        print(f"Bad value for variable to interest: {name_variable}")
        print(get_help(sys.argv[0]))
