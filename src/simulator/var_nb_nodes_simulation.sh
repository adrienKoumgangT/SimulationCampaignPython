#!/bin/bash

# définition des paramètres à passer au simulateur pour la variable nb_nodes
n_v="-name_var=0"
n_o_s="-number_of_simulation=100"
v_v_b="-variable_value_begin=100"
v_v_e="-variable_value_end=150"
v_v_i="-var_value_incremented=10"
o_i_v="-other_interest_var=-stop_all_sane=1,-gui=0,-printout=2"
p_s_r="-path_save_result=result_simulations/nb_nodes"


python3 simulator.py $n_v $n_o_s $v_v_b $v_v_e $v_v_i $o_i_v $p_s_r
