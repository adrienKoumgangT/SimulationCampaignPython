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
           f"Syntax: {name_software} -name_var=name [-number_of_simulation=x]\n" \
           f"                       [-variable_value_begin=x] [-variable_value_end=x] [-var_value_incremented=x]\n" \
           f"                       [-other_interest_var=list_var]\n" \
           f"                       [-path_save_result=pathname]\n" \
           f"\n" \
           f"\t -name_var:              [name] name of the variable of interest\n" \
           f"\t                         [=0] for nb nodes\n" \
           f"\t                         [=1] for nb infected\n" \
           f"\t                         [=2] for travel distance\n" \
           f"\t                         [=3] for nb vaccinated\n" \
           f"\t                         [=4] for vaccine efficiency\n" \
           f"\t                         [=5] for infection period\n" \
           f"\t                         [=6] for contagion period\n" \
           f"\t                         [=7] for immune period\n" \
           f"\t -number_of_simulation:  [=x] number of simulations to do for each value of " \
           f"the variable of interest\n" \
           f"\t -variable_value_begin:  [=x] initial value for variable simulation for the simulations\n" \
           f"\t -variable_value_end:    [=x] final value for variable simulation for the simulations\n" \
           f"\t -var_value_incremented: [=x] increment value for variable simulation\n" \
           f"\n" \
           f"\t -other_interest_var:    [=list_var] list of other parameters to switch to the simulator\n" \
           f"\t                         ex: -stop_all_sane=1,-gui=0,-printout=2\n" \
           f"\n" \
           f"\t -path_save_result:      [=pathname] path to directory where save file to result of the simulator\n"


def get_simulator_info():
    return f"---------\n" \
           f"Simulator parameters:\n" \
           f"Using {get_name_variable(name_variable)} variable to interest.\n" \
           f"Using {nb_simulation} as number of simulations to do for each value of the variable of interest.\n" \
           f"Using {var_value_begin} as initial value for the initial value for the variable to interest\n" \
           f"Using {var_value_end} as final value for the initial value for the variable to interest\n" \
           f"Using {var_incremented_value} as value for increment number of variable to interest during" \
           f" the simulation\n" \
           f"Using {list_other_parameter_simulator} for other parameter simulator\n" \
           f"Using {pathname} to directory where save files result to the simulator\n" \
           f"---------\n"


def get_info_nb_values(name_var: int):
    if name_var in {1, 2, 3, 4, 5, 6, 7}:
        # nb = 41 [100 -> 500]; shift = 10
        return 50
    else:
        # nb = 1 [100]; shift = 0
        return 0


def get_info_values_var(name_var: int):
    if name_var == 1:
        # var = "nb infected"; nb = 10 [1 -> 10]; shift = 1
        return 1, 10, 1
    elif name_var == 2:
        # var = "travel distance"; nb = 11 [150 -> 250]; shift = 10
        return 150, 250, 10
    elif name_var == 3:
        # var = "nb vaccinated"; nb = 11 [0 -> 10]; shift = 1
        return 0, 10, 1
    elif name_var == 4:
        # var = "vaccine efficiency"; nb = 10 [1 -> 10]; shift = 1
        return 1, 10, 1
    elif name_var == 5:
        # var = "infection period"; nb = 51 [50 -> 150]; shift = 10
        return 50, 150, 10
    elif name_var == 6:
        # var = "contagion period"; nb = 16 [150 -> 300]; shift = 10
        return 150, 300, 10
    elif name_var == 7:
        # var = "immune period"; nb = 11 [200 -> 400]; shift = 20
        return 200, 400, 10
    else:
        # nb = 1 [1]; shift = 1
        return 1, 1, 1


def run_simulator(variable_interest: str, variable_value_begin: int, variable_value_end: int,
                  variable_incremented_value: int, number_of_simulation: int,
                  list_other_interest_var: list, path_directory: str):

    if path_directory[-1] != "/":
        path_directory += "/"

    def do_simulation(value_of_variable: int, nb_simulation_to_do: int):
        list_arg = ['java', '-jar', 'Virus.jar', variable_interest + '=' + str(value_of_variable),
                    '-stop_all_sane=1', '-gui=0', '-printout=2']
        for other_arg in list_other_interest_var:
            list_arg.append(other_arg)
        simulation_index = 0
        while simulation_index <= nb_simulation_to_do:
            print(f"\t\t --> simulation n. {simulation_index}")
            res = subprocess.run(list_arg, capture_output=True)
            with open(path_directory + 'res_value_variable_' + str(var_value) + '_simulation_n_' +
                      str(simulation_index) + '.txt', 'w') as file_result:
                file_result.write(res.stdout.decode('utf-8'))
            simulation_index += 1

    # Pour empêcher des cycle infini
    if variable_incremented_value <= 0:
        variable_incremented_value = 1
    if variable_value_begin > variable_value_end:
        val_inter = variable_value_end
        variable_value_end = variable_value_begin
        variable_value_begin = val_inter

    if number_of_simulation <= 0:
        number_of_simulation = 1

    # début de la simulation

    var_value = variable_value_begin
    while var_value <= variable_value_end:
        print(f"Simulation for {variable_interest} = {var_value}")
        do_simulation(value_of_variable=var_value, nb_simulation_to_do=number_of_simulation)
        var_value += variable_incremented_value


if __name__ == '__main__':
    # variable par défaut de la simulation : nb nodes
    name_variable = 0
    var_interest = "-nb_nodes"
    # valeurs par défaut pour le nombre de de simulation à faire pour chaque valeur de la variable d' interet
    nb_simulation = 1
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
                var_interest = get_name_variable(name_var=name_variable)
            elif option[0] == "-nb_simulation":
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
                      number_of_simulation=1, list_other_interest_var=list_other_parameter_simulator,
                      path_directory=pathname)

    else:
        print(f"Bad value for variable to interest: {name_variable}")
        print(get_help(sys.argv[0]))
