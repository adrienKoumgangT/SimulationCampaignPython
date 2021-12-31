# SimulationCampaignPython


## Présentation du projet

### Introduction 

Le but de ce projet est d'utiliser un simulateur fourni pour mener une campagne de simulation: exécuter
le simulateur avec de nombreux paramètres différents, collecter et manipuler les données produites par
le simulateur, obtenir des graphiques résumant l'impact des paramètres suivis sur les indicateurs choisis.

Ce simulateur est écrit en Java et modélise la propagation d'un virus dans une population.
Il est fournit sous la forme d'un fichier Virus.jar qui intègre toutes les bibliothèques
nécessaires. On peut lancer le simulateur avec les paramètres par défaut avec la commande
(Java doit etre installé sur la machine qui exécute):

```
java -jar Virus.jar
```

Le code source du simulateur est fourni en annexe. Ce code source est fourni à titre indicatif
pour comprendre la signification de chaque paramètre passé au simulateur.


### 1. La collecte des données expérimentales.

Réalisation en Python et en utilisant la bibliothèque `subprocess` un programme qui exécute
plusieurs fois le simulateur avec les paramètres de simulation. Ces exécutions multiples
sont utilisées pour obtenir des intervalles de confiance suffisants lors de la phase de
visualisation des données expérimentales. Les résultats intermédiares sont stockés dans
un ensemble de fichiers pour l'ensemble des simulations menées (pour un ensemble de paramètres
donné).

Dans un deuxième temps, on réalise en Python un programme qui exécute le simulateur en faisant
varier un paramètre de la simulation, en réalisant plusieurs simulations pour chaque ensemble
de paramètres. Les résultats intermédiaires sont stockés dans un ensemble de fichiers
pour l'ensemble des simulations menées.


### 2. Manipulation des données expérimentales

A l'aide des fichiers produits précédemment, on réalise en Python et en utilisant les
bibliothèques `numpy` et `pandas` un programme qui permette d'obtenir les informations
suivantes:
- Quel est l'impact du nombre initial d'infectés sur:
  - la durée de l'épidémie
  - la proportion maximale de la population qui est infectée
  - la distribution des multi-infections
- Quel est l'impact du rayon de mobilité sur:
  - la durée de l'épidémie
  - la proportion de la population qui est infectée
  - la distribution des multi-infections
- Quel est l'impact de la proportion de vaccinés sur:
  - la durée de l'épidémie
  - la proportion de la population qui est infectée
  - la distribution des multi-infections
- Quel est l'impact de l'efficacité vaccinale sur:
  - la durée de l'épidémie
  - la proportion de la population qui est infectée
  - la distributuin des multi-infections
- Quel est l'impact de la durée d'infection sur
  - la durée de l'épidémie
  - la proportion de la population qui est infectée
  - la distribution des multi-infections
- Quel est l'impact de la durée de contagiosité sur:
  - la durée de l'épidémie
  - la proportion de la population qui est infectée
  - la distribution des multi-infections
- Quel est l'impact de la durée d'immunité sur:
  - la durée de l'épidémie
  - la proportion de la population qui est infectée
  - la distribution des multi-infections
- Quel est l'impact de la densité de population sur:
  - la durée de l'épidémie
  - la proportion de la population qui est infectée
  - la distribution des multi-infections
Les informations ainsi produites sont stockés dans plusieurs fichiers.


### 3. Tracer des données expérimentales

A l'aide des fichiers produits précédemment, on réalise en Python et en utilisant la bibliothèque
`matplotlib` un programme qui produit des graphiques pertinents pour évaluer l'impact des paramètres
suivis (nombre initial d'infectés, rayon de mobilité, proportion de vaccinés, efficacité
vaccinale, durée de contagiosité, durée d'immunité, densité de population) sur les indicateurs
sélectionnéEs (la durée de l'épidémie, la proportion de la population qui est infectée,
la distribution des multi-infections). Les graphiques ainsi produits devront figurer dans
votre rapport.


## Présentation du code du simulateur (Virus.jar)

### Annexe 1. Fichier Virus.java

```java
import io.jbotsim.ui.JViewer;

public class Virus { 
    public static void main(String[] args){ 
        int nb_nodes = 100; 
        int snapshot = 10; 
        int nb_snapshots = -1; 
        int width = 1000; 
        int height = 1000; 
        int gui = 1; 
        int infected = 2; 
        int vaccinated = 0; 
        int printout = VirusTopology.CATEGORIES; 
        int show_parameters = 1; 
        int stop_all_sane = 0; 
        int infection_period = 100; 
        int contagion_period = 200; 
        int immune_period = 300; 
        int travel_distance = 200; 
        int vaccine_efficiency = 2;
 
        if(args.length > 0) { 
            for(String s:args) { 
                String[] option = s.split("="); 
                if(option[0].equals("-nb_nodes")) { 
                    nb_nodes = Integer.parseInt(option[1]); 
                } 
                if(option[0].equals("-snapshot_period")) { 
                    snapshot = Integer.parseInt(option[1]); 
                } 
                if(option[0].equals("-nb_snapshots")) { 
                    nb_snapshots = Integer.parseInt(option[1]); 
                } 
                if(option[0].equals("-width")) { 
                    width = Integer.parseInt(option[1]); 
                } 
                if(option[0].equals("-height")) { 
                    height = Integer.parseInt(option[1]); 
                } 
                if(option[0].equals("-gui")) { 
                    gui = Integer.parseInt(option[1]); 
                } 
                if(option[0].equals("-nb_infected")) { 
                    infected = Integer.parseInt(option[1]); 
                } 
                if(option[0].equals("-nb_vaccinated")) { 
                    vaccinated = Integer.parseInt(option[1]); 
                } 
                if(option[0].equals("-vaccine_efficiency")) { 
                    vaccine_efficiency = Integer.parseInt(option[1]); 
                } 
                if(option[0].equals("-infection_period")) { 
                    infection_period = Integer.parseInt(option[1]); 
                } 
                if(option[0].equals("-contagion_period")) { 
                    contagion_period = Integer.parseInt(option[1]); 
                } 
                if(option[0].equals("-immune_period")) { 
                    immune_period = Integer.parseInt(option[1]); 
                } 
                if(option[0].equals("-travel_distance")) { 
                    travel_distance = Integer.parseInt(option[1]); 
                } 
                if(option[0].equals("-printout")) { 
                    printout = Integer.parseInt(option[1]); 
                } 
                if(option[0].equals("-stop_all_sane")) { 
                    stop_all_sane = Integer.parseInt(option[1]); 
                } 
                if(option[0].equals("-show_parameters")) { 
                    show_parameters = Integer.parseInt(option[1]); 
                }
                if(option[0].equals("-help")) {
                    System.out.println("Parameters:");
                    System.out.println(" -contagion_period: [=X] nodes contaminate others for X time units on average (default 200)");
                    System.out.println(" -gui: [=0] do not show GUI");
                    System.out.println(" [=1]* show GUI (default)");
                    System.out.println(" -height: [=X] area is X units tall (default 1000)");
                    System.out.println(" -help: show this message");
                    System.out.println(" -immune_period: [=X] nodes remain immune for X time units on average (default 300)");
                    System.out.println(" -infection_period: [=X] nodes get infected if they remain close to an infected node for X time units on average (default 100)"); 
                    System.out.println(" -nb_infected: [=X] initial number of infected nodes (default 2)"); 
                    System.out.println(" -nb_vaccinated: [=X] initial number of vaccinated nodes (default 0)"); 
                    System.out.println(" -nb_nodes: [=X] initial number of total nodes (default 120)"); 
                    System.out.println(" -nb_snapshots: [=X] total number of snapshots before simulation stops (default -1: infinite)"); 
                    System.out.println(" -printout: [=0] do not print anything"); 
                    System.out.println(" [=1]* print #sane, #infected, #immune (default)"); 
                    System.out.println(" [=2] print the status of every node"); 
                    System.out.println(" -show_parameters: [=0] do not show parameters");
                    System.out.println(" [=1]* show parameters (default)"); 
                    System.out.println(" -snapshot_period: [=X] make a snapshot every X time units (default 10)"); 
                    System.out.println(" -stop_all_sane: [=0]* do not stop the simulation when all nodes are sane (default)"); 
                    System.out.println(" [=1] stop the simulation when all nodes are sane"); 
                    System.out.println(" -travel_distance: [=X] nodes can move within a X*X square (default 200)"); 
                    System.out.println(" -vaccine_efficiency:[=X] efficiency of the vaccine (default 2)"); 
                    System.out.println(" -width: [=X] area is X units wide (default 1000)"); 
                } 
            } 
        }
        if(show_parameters!=0) { 
            System.out.println("-----"); 
            System.out.println("Simulation parameters:"); 
            System.out.println("Using " + nb_nodes + " nodes."); 
            System.out.println("Using " + snapshot + " snapshot period."); 
            System.out.println("Using " + nb_snapshots + " as maximum number of snapshots."); 
            System.out.println("Using " + width + " as maximum number of snapshots."); 
            System.out.println("Using " + height + " as height."); 
            System.out.println("Using " + gui + " as GUI option."); 
            System.out.println("Using " + infected + " infected nodes initially."); 
            System.out.println("Using " + vaccinated + " vaccinated nodes initially."); 
            System.out.println("Using " + vaccine_efficiency + " as vaccine efficiency."); 
            System.out.println("Using " + infection_period + " as infection period."); 
            System.out.println("Using " + contagion_period + " as contagion period."); 
            System.out.println("Using " + immune_period + " as immune period."); 
            System.out.println("Using " + travel_distance + " as travel distance."); 
            System.out.println("Using " + printout + " as printout option."); 
            System.out.println("Using " + stop_all_sane + " as stop_all_sane condition."); 
            System.out.println("-----");
        }
        
        VirusTopology tp = new VirusTopology(snapshot, nb_snapshots, printout, stop_all_sane ); 
        tp.setDefaultNodeModel(VirusNode.class);
        tp.setDimensions(width,height);
        tp.generateNodes(nb_nodes, travel_distance);
        tp.infectNodes(infected);
        tp.vaccineNodes(vaccinated);
        VirusNode.setParameters(infection_period, contagion_period, 
        immune_period, travel_distance, vaccine_efficiency); 
        if(gui == 1) { 
            new JViewer(tp); 
        } 
        tp.start(); 
    } 
}
```

### Annexe 2. Fichier VirusTopology.java

```java
import io.jbotsim.core.Topology;
import io.jbotsim.core.Node;
import java.util.concurrent.ThreadLocalRandom;

public class VirusTopology extends Topology {
    public static final int NOTHING = 0;
    public static final int CATEGORIES = 1;
    public static final int NODES = 2;
    int snapshot_period = 10;
    int nb_snapshots = -1;
    int remaining_clock = 0;
    int printout = CATEGORIES;
    int stop_all_sane = 0;

    VirusTopology( int snapshot, int nb_max_snapshots, int print, int stop ) {
        snapshot_period = snapshot;
        nb_snapshots = nb_max_snapshots;
        printout = print;
        stop_all_sane = stop;
    }

    public void generateNodes(int nb, int distance) {
        for(int i=0; i<nb; i++) {
            int x = ThreadLocalRandom.current().nextInt(distance/2, getWidth()-distance/2);
            int y = ThreadLocalRandom.current().nextInt(distance/2, getHeight()-distance/2);
            addNode(x,y);
        }
    }

    public void infectNodes(int nb) {
        for(int i = 0; i<nb; i++) {
            int id = ThreadLocalRandom.current().nextInt(0, getNodes().size());
            ((VirusNode)findNodeById(id)).setStatus(VirusNode.INFECTED);
        }
    }

    public void vaccineNodes(int nb) {
        for(int i = 0; i<nb; i++) {
            int id = ThreadLocalRandom.current().nextInt(0, getNodes().size());
            ((VirusNode)findNodeById(id)).setStatus(VirusNode.VACCINE_SANE);
        }
    }

    public boolean isAllSane() {
        for(Node n: getNodes()) {
            VirusNode vn = (VirusNode)n;
            if(!vn.isSane() && !vn.isVaccineSane()) {
                return false;
            }
        }
        return true;
    }

    public void printCategories() {
        int nb_sane = 0;
        int nb_infected = 0;
        int nb_immune = 0;
        for(Node n: getNodes()) {
            VirusNode vn = (VirusNode)n;
            if(vn.isSane() || vn.isVaccineSane()) {
                nb_sane++;
            }
            else {
                if(vn.isInfected() || vn.isVaccineInfected()) {
                  nb_infected++;
                }
                else {
                    if(vn.isImmune() || vn.isVaccineImmune()) {
                        nb_immune++;
                    }
                }
            }
        }

        System.out.println("" + nb_sane + " " + nb_infected + " " + nb_immune);
    }

    public void printNodes() {
        for(Node n: getNodes()) {
            VirusNode vn = (VirusNode)n;
            if(vn.isSane()) {
                System.out.print("0 ");
            }
            else {
                if(vn.isInfected()) {
                    System.out.print("1 ");
                }
                else {
                    if(vn.isImmune()) {
                        System.out.print("2 ");
                    }
                    else {
                        if(vn.isVaccineSane()) {
                            System.out.print("3 ");
                        }
                        else {
                            if(vn.isVaccineInfected()) {
                                System.out.print("4 ");
                            }
                            else {
                                if(vn.isVaccineImmune()) {
                                    System.out.print("5 ");
                                }
                            }
                        }
                    }
                }
            }
        }
        System.out.println();
    }

    @Override
    public void onClock() {
        if(nb_snapshots == 0) {
            System.exit(0);
        }
        if( stop_all_sane != 0 ) {
            if(isAllSane()) {
                System.exit(0);
            }
        }
        if( remaining_clock == 0 ) {
            pause();
            if(printout == CATEGORIES) {
                printCategories();
            }
            else {
                if(printout == NODES) {
                    printNodes();
                }
            }
            remaining_clock = snapshot_period;
            if(nb_snapshots != -1) {
                nb_snapshots--;
            }
            resume();
        }
       else {
            remaining_clock--;
       }
    }
}
```


### Annexe 3. Fichier VirusNode.java

```java
import io.jbotsim.core.Node; 
import io.jbotsim.core.Message; 
import io.jbotsim.core.Color; 
import io.jbotsim.core.Point; 
import java.util.concurrent.ThreadLocalRandom;

public class VirusNode extends Node{ 
    static final int SANE = 0; 
    static final int INFECTED = 1; 
    static final int IMMUNE = 2; 
    static final int VACCINE_SANE = 3; 
    static final int VACCINE_INFECTED = 4; 
    static final int VACCINE_IMMUNE = 5; 
    static final Color all_colors[] = { Color.green, Color.red, Color.blue, Color.yellow, Color.magenta, Color.orange }; 
    static int infection_period = 100; 
    static int contagion_period = 200; 
    static int immune_period = 300; 
    static int travel_distance = 100; 
    static int vaccine_efficiency = 9;
 
    static void setParameters( int infection, int contagion, int immune, int distance, int vaccine ) { 
        infection_period = infection; 
        contagion_period = contagion; 
        immune_period = immune; 
        travel_distance = distance; 
        vaccine_efficiency = vaccine; 
    } 
 
    int status = 0; 
    int contact_since = 0; 
    int infected_since = 0; 
    int immune_since = 0; 
    int distance = 0; 
    Point initial_coord = null; 
    int infection_period_random = 0; 
    int contagion_period_random = 0; 
    int immune_period_random = 0; 
    int vaccine_efficiency_random = 0; 
    
    void setStatus(int s) { 
        status = s; 
        setColor( all_colors[status] ); 
    }

    boolean isSane() { return status == SANE; }
    boolean isInfected() { return status == INFECTED; }
    boolean isImmune() { return status == IMMUNE; }
    boolean isVaccineSane() { return status == VACCINE_SANE; } 
    boolean isVaccineInfected() { return status == VACCINE_INFECTED; } 
    boolean isVaccineImmune() { return status == VACCINE_IMMUNE; } 

    public void randomizeDestination() {
        int next_x = ThreadLocalRandom.current().nextInt((int)initial_coord.x - (int)(travel_distance/2), (int)initial_coord.x + (int)(travel_distance/2)); 
        int next_y = ThreadLocalRandom.current().nextInt((int)initial_coord.y - (int)(travel_distance/2), (int)initial_coord.y + (int)(travel_distance/2)); 
        setDirection(new Point(next_x,next_y));
        distance = (int)Math.round(distance(next_x,next_y)); 
    }
 
    public void randomizePeriods() { 
        vaccine_efficiency_random = ThreadLocalRandom.current().nextInt(vaccine_efficiency - 1, vaccine_efficiency + 1); 
        infection_period_random = ThreadLocalRandom.current().nextInt(infection_period - infection_period/3, infection_period + infection_period/3); 
        contagion_period_random = ThreadLocalRandom.current().nextInt(contagion_period - contagion_period/3, contagion_period + contagion_period/3); 
        immune_period_random = ThreadLocalRandom.current().nextInt(immune_period - immune_period/3, immune_period + immune_period/3); 
    }
 
    @Override
    public void onStart() { 
        // JBotSim executes this method on each node upon initialization
        initial_coord = getLocation(); 
        randomizeDestination(); 
        randomizePeriods(); 
    } 
  
    @Override
    public void onSelection() { 
        // JBotSim executes this method on a selected node
        if( isSane() ) { 
            setStatus(INFECTED); 
        } 
    } 
 
    boolean canBeInfected() { 
        for(Node node: getNeighbors()){ 
            if(((VirusNode)node).isInfected()){ 
                return true; 
            } 
        }
        return false; 
    }
 
    @Override
    public void onClock() { 
        // JBotSim executes this method on each node in each round
        if( isSane() ) { 
            if (canBeInfected()) { 
                contact_since++;
                if (contact_since > infection_period_random) { 
                    contact_since = 0; 
                    setStatus(INFECTED); 
                } 
            } else { 
                contact_since = 0; 
            } 
        } 
        else { 
            if( isInfected() ) { 
                infected_since++; 
                if (infected_since > contagion_period_random ) { 
                    infected_since = 0; 
                    setStatus(IMMUNE); 
                } 
            }
            else { 
                if( isImmune() ) { 
                    immune_since++; 
                    if(immune_since > immune_period_random ) { 
                        immune_since = 0; 
                        setStatus(SANE); 
                        randomizePeriods(); 
                    } 
                }
                else { 
                    if( isVaccineSane() ) { 
                        if(canBeInfected()) { 
                            contact_since++; 
                            if(contact_since > infection_period_random*vaccine_efficiency_random) { 
                                contact_since = 0; 
                                setStatus(VACCINE_INFECTED); 
                            } 
                        } 
                        else { 
                            contact_since = 0; 
                        } 
                    } 
                    if( isVaccineInfected() ) { 
                        infected_since++; 
                        if(infected_since > contagion_period_random/vaccine_efficiency_random) { 
                            infected_since = 0; 
                            setStatus(VACCINE_IMMUNE); 
                        } 
                    } 
                    else { 
                        if( isVaccineImmune()) { 
                            immune_since++; 
                            if(immune_since > immune_period_random*vaccine_efficiency_random) { 
                                immune_since = 0; 
                                setStatus(VACCINE_SANE); 
                                randomizePeriods(); 
                            } 
                        } 
                    } 
                } 
            } 
        } 
        setStatus(status); 
        move(1); 
        distance--; 
        if( distance <= 0) { 
            randomizeDestination(); 
        } 
    } 
}
```


## Présentation des parties principales de 'Simulation Campaign'

### La simulation

Elle se fait grace au code source [simulator.py](src/simulator/simulator.py).
Ce fichier python permet l'exécution d'un ensemble de simulation en fonction d'une variable passé en ligne de
commande au programme et aussi d'un ensemble de paramètres, tout aussi passé en ligne de commande lors du lancement
de l'exécution du programme. La syntax générale d'exécution du programme de simulation est la suivante:
> python3 -name_var=name [-number_of_simulation=x]
>                         [-variable_value_begin=x] [-variable_value_end=x] [-var_value_incremented=x]
>                         [-other_interest_var=list_var]
>                         [-path_save_result=pathname]

- name_var: [name] name of the variable of interest
  - [=0] for nb nodes
  - [=1] for nb infected
  - [=2] for travel distance
  - [=3] for nb vaccinated
  - [=4] for vaccine efficiency
  - [=5] for infection period
  - [=6] for contagion period
  - [=7] for immune period
  - [=x] number of simulations to do for each value of the variable of interest
- variable_value_begin:  [=x] initial value for variable simulation for the simulations
- variable_value_end:    [=x] final value for variable simulation for the simulations
- var_value_incremented: [=x] increment value for variable simulation
- other_interest_var:    [=list_var] list of other parameters to switch to the simulator. ex: -stop_all_sane=1,-gui=0,-printout=2
- path_save_result:      [=pathname] path to directory where save file to result of the simulator

Ces informations peuvent etre obtenu depuis le code source en l'exécutant sans arguments.

Pour ce projet, nous nous sommes interesés à 8 variables et créer des fichiers 'bash' pour chacune d'elle
enfin d'y passer des paramètres exact pour leur simulation:
- contagion_period ([var_contagion_period_simulation.sh](src/simulator/var_contagion_period_simulation.sh)):
  - name_var = 6
  - nombre de simulations = 50
  - valeur de début = 150
  - valeur de fin = 300
  - shift = 10
  - paramètres à passer au simulateur: '-stop_all_sane=1, -gui=0, -printout=2'
  - dossiers de sauvegardes des fichiers résultats des simulations : 'result_simulations/contagion_period'
- immune_period ([var_immune_period_simulation.sh](src/simulator/var_immune_period_simulation.sh))
  - name_var = 7
  - nombre de simulations = 100
  - valeur de début = 200
  - valeur de fin = 400
  - shift = 20
  - paramètres à passer au simulateur: '-stop_all_sane=1, -gui=0, -printout=2'
  - dossiers de sauvegardes des fichiers résultats des simulations : 'result_simulations/immune_period'
- nb_infected ([var_nb_infected_simulation.sh](src/simulator/var_nb_infected_simulation.sh))
  - name_var = 1
  - nombre de simulations = 100
  - valeur de début = 1
  - valeur de fin = 10
  - shift = 1
  - paramètres à passer au simulateur: '-stop_all_sane=1, -gui=0, -printout=2'
  - dossiers de sauvegardes des fichiers résultats des simulations : 'result_simulations/nb_infected'
- infection_period ([var_infection_period_simulation.sh](src/simulator/var_infection_period_simulation.sh))
  - name_var = 5
  - nombre de simulations = 100
  - valeur de début = 50
  - valeur de fin = 150
  - shift = 10
  - paramètres à passer au simulateur: '-stop_all_sane=1, -gui=0, -printout=2'
  - dossiers de sauvegardes des fichiers résultats des simulations : 'result_simulations/infection_period'
- nb_nodes ([var_nb_nodes_simulation.sh](src/simulator/var_nb_nodes_simulation.sh))
  - name_var = 0
  - nombre de simulations = 100
  - valeur de début = 100
  - valeur de fin = 150
  - shift = 10
  - paramètres à passer au simulateur: '-stop_all_sane=1, -gui=0, -printout=2'
  - dossiers de sauvegardes des fichiers résultats des simulations : 'result_simulations/nb_nodes'
- travel_distance ([var_travel_distance_simulation.sh](src/simulator/var_travel_distance_simulation.sh))
  - name_var = 2
  - nombre de simulations = 100
  - valeur de début = 150
  - valeur de fin = 250
  - shift = 10
  - paramètres à passer au simulateur: '-stop_all_sane=1, -gui=0, -printout=2'
  - dossiers de sauvegardes des fichiers résultats des simulations : 'result_simulations/travel_distance'
- nb_vaccinated ([var_nb_vaccinated_simulation.sh](src/simulator/var_nb_vaccinated_simulation.sh))
  - name_var = 3
  - nombre de simulations = 100
  - valeur de début = 0
  - valeur de fin = 10
  - shift = 1
  - paramètres à passer au simulateur: '-stop_all_sane=1, -gui=0, -printout=2'
  - dossiers de sauvegardes des fichiers résultats des simulations : 'result_simulations/nb_vaccinated'
- vaccine_efficiency ([var_vaccine_efficiency_simulation.sh](src/simulator/var_vaccine_efficiency._simulation.sh))
  - name_var = 4
  - nombre de simulations = 100
  - valeur de début = 1
  - valeur de fin = 10
  - shift = 1
  - paramètres à passer au simulateur: '-stop_all_sane=1, -gui=0, -printout=2'
  - dossiers de sauvegardes des fichiers résultats des simulations : 'result_simulations/vaccine_efficiency'

Le programme de simulation offre un feedback de 2 niveaux :
- le premier : il affiche les paramètres passés au simulateur
- le deuxième : pour chaque valeur de la variable de simulation, il indique à quelle simulation il se situe

Nous avons choisit d'implementer le simulateur de cette manière enfin de permettre la simulation précise d'une variable
ainsi que de ses valeurs aux choix. (Ceci dû au tant que prend les simulations, cela nous a permit de lancer une
simulation puis de l'arreter pour la relancer plus tard, donnant ainsi une grande flexibilité dans l'exécution des
simulations)

### L'analyse des simulations

Elle se fait grâce au code source [analyse.py](src/analyse/analyse.py).
Ici, l'analyse des fichiers résultats de la simulation se fait en parallèle pour chaque variable.
Ainsi on a un thread qui s'occupe de l'analyse de chaque variable.

L'analyse des fichiers est orienté principalement sur 3 points :
- Calcul de la durée de chaque simulation. Et elle se fait grâce à la fonction 'calcul_during_epidemic'.
Ici nous avons choisi de calculer la durée en nombre de snapshot, ainsi la durée n'est point exprimé en temps mais en nb shapshot.
- La proportion (max ou pas) de la population infectée. Et elle se fait grâce à la fonction 'calcul_proportion_population_infected'.
Ici nous faisons le calcul en déterminant le nombre d'infecté que nous avons à un moment t (ici fesant référence à un snapshot)
et pour la proportion simple, nous prenons la valeur moyenne et pour celle max, nous prennons le maximum obtenu.
  - Le cas de calcul de la proportion max fait référence à la simulation du nombre initial d'infecté
- La proportion des multi-infections. Et elle se fait grâce à la fonction 'calcul_proportion_multi_infection'.
Ici nous faisons le calcul en déterminant le nombre de fois qu'un node est infecté durant toute la durée de la simulation.

Les résultats ainsi obtenus (sous forme de tableaux) sont sauvegardés dans des fichiers:
- nb_infected:
  - dossier: result_analyse/nb_infected
  - durée: infected_during.csv
  - proportion population infected: infected_proportion.csv
  - multi infection: infected_multi_infection.csv
- travel_distance:
  - dossier: result_analyse/travel_distance
  - durée: travel_distance_during.csv
  - proportion population infected: travel_distance_proportion.csv
  - multi infection: travel_distance_multi_infection.csv
- nb_vaccinated:
  - dossier: result_analyse/nb_vaccinated
  - durée: vaccinated_during.csv
  - proportion population infected: vaccinated_proportion.csv
  - multi infection: vaccinated_multi_infection.csv
- vaccine_efficiency:
  - dossier: result_analyse/vaccine_efficiency
  - durée: vaccine_efficiency_during.csv
  - proportion population infected: vaccine_efficiency_proportion.csv
  - multi infection: vaccine_efficiency_multi_infection.csv
- infection_period:
  - dossier: result_analyse/infection_period
  - durée: infection_period_during.csv
  - proportion population infected: infection_period_proportion.csv
  - multi infection: infection_period_multi_infection.csv
- contagion_period:
  - dossier: result_analyse/contagion_period
  - durée: contagion_period_during.csv
  - proportion population infected: contagion_period_proportion.csv
  - multi infection: contagion_period_multi_infection.csv
- immune_period:
  - dossier: result_analyse/immune_period
  - durée: immune_period_during.csv
  - proportion population infected: immune_period_proportion.csv
  - multi infection: immune_period_multi_infection.csv
- nb_nodes:
  - dossier: result_analyse/nb_nodes
  - durée: nodes_during.csv
  - proportion population infected: nodes_proportion.csv
  - multi infection: nodes_multi_infection.csv

### Data graph

Elle se fait grâce au code source [analyse.py](src/analyse/analyse.py) et se fait directement après l'analyse des simulations.
Les résultats ainsi obtenus (graph) sont sauvegardés dans des fichiers:
- nb_infected:
  - dossier: result_analyse/nb_infected
  - durée: infected_during.pdf
  - proportion population infected: infected_proportion.pdf
  - multi infection: infected_multi_infection.pdf
- travel_distance:
  - dossier: result_analyse/travel_distance
  - durée: travel_distance_during.pdf
  - proportion population infected: travel_distance_proportion.pdf
  - multi infection: travel_distance_multi_infection.pdf
- nb_vaccinated:
  - dossier: result_analyse/nb_vaccinated
  - durée: vaccinated_during.pdf
  - proportion population infected: vaccinated_proportion.pdf
  - multi infection: vaccinated_multi_infection.pdf
- vaccine_efficiency:
  - dossier: result_analyse/vaccine_efficiency
  - durée: vaccine_efficiency_during.pdf
  - proportion population infected: vaccine_efficiency_proportion.pdf
  - multi infection: vaccine_efficiency_multi_infection.pdf
- infection_period:
  - dossier: result_analyse/infection_period
  - durée: infection_period_during.pdf
  - proportion population infected: infection_period_proportion.pdf
  - multi infection: infection_period_multi_infection.pdf
- contagion_period:
  - dossier: result_analyse/contagion_period
  - durée: contagion_period_during.pdf
  - proportion population infected: contagion_period_proportion.pdf
  - multi infection: contagion_period_multi_infection.pdf
- immune_period:
  - dossier: result_analyse/immune_period
  - durée: immune_period_during.pdf
  - proportion population infected: immune_period_proportion.pdf
  - multi infection: immune_period_multi_infection.pdf
- nb_nodes:
  - dossier: result_analyse/nb_nodes
  - durée: nodes_during.pdf
  - proportion population infected: nodes_proportion.pdf
  - multi infection: nodes_multi_infection.pdf
