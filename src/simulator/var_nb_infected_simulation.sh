#!/bin/bash

# définition des paramètres à passer au simulateur pour la variable nb_infected
n_v="-name_var=1"
n_o_i_n_b="-number_of_initial_node_begin=100"
n_o_i_n_e="-number_of_initial_node_end=500"
nb_n_i="-nb_node_incremented=10"
v_v_b="-variable_value_begin=1"
v_v_e="-variable_value_end=50"
v_v_i="var_value_incremented=1"
o_i_v="-other_interest_var=-stop_all_sane=1,-gui=0,-printout=2"
p_s_r="-path_save_result=result_simulations/infected"


python3 simulator.py $n_v $n_o_i_n_b $n_o_i_n_e $nb_n_i $v_v_b $v_v_e $v_v_i $o_i_v $p_s_r
