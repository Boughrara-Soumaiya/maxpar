from bibli import Task, TaskSystem


# --- Déclaration des variables globales dans le fichier de test ---
X = 0
Y = 0
Z = 0

# --- Définition des fonctions de chaque tâche ---
def t1_run():
    global X
    X = 1
    print("T1 exécutée")

def t2_run():
    global X, Y, Z
    if X is None or Y is None:
        print("Les variables X ou Y ne sont pas initialisées.")
        return
    Z = X + Y
    print("T2 exécutée")

def t3_run():
    global Y
    Y = 2
    print("T3 exécuté")

def t4_run():
    global X, Y, Z
    if X is None or Z is None:
        print("Les variables X ou Z ne sont pas initialisées.")
        return
    Y = X + Z
    print(f"t4 exécutée")

def t5_run():
    global X, Y
    if Y is None:
        print("La variable Y n'est pas initialisée.")
        return
    X = Y
    print(f"t5 exécutée ")

def t6_run():
    global Z
    Z = 8
    print(f"t6 exécutée ")

def t7_run():
    global Y, Z
    if Y is None or Z is None:
        print("Les variables Y ou Z ne sont pas initialisées.")
        return
    Y = Y + Z
    print(f"t7 exécutée ")


# --- Création des instances de Task ---
t1 = Task("t1", [], ["X"], run=t1_run)
t2 = Task("t2",["X","Y"], ["Z"], run=t2_run)
t3 = Task("t3",[], ["Y"], run=t3_run)
t4 = Task("t4",["X","Z"], ["Y"], run=t4_run)
t5 = Task("t5",["Y"], ["X"], run=t5_run)
t6 = Task("t6",[], ["Z"], run=t6_run)
t7 = Task("t7",["Z"], ["Y"], run=t7_run)

# --- Définir les dépendances ---
dependencies = {
    "t1" : [],
    "t2" : ["t1","t3"],
    "t3" : [],
    "t4" : ["t1","t6"],
    "t5" : ["t3"],
    "t6" : [],
    "t7" : ["t2"],
}

if __name__ == '__main__':
    try:
        print("Début de l'exécution du bloc try.")
        task_system = TaskSystem([t1, t2, t3, t4, t5, t6, t7], dependencies)

        niveaux = task_system.decoupage()
        print("Découpage des tâches en niveaux :")
        for i, niveau in enumerate(niveaux):
            print(f"Niveau {i} : {', '.join(niveau)}")

        print("\nExécution des tâches séquentiellement :")
        task_system.runSeq()

        print("\nExécution des tâches parallèlement :")
        task_system.run()

        print("\nGraphique de dépendance :")
        task_system.draw()

        print("\nTest de Déterminisme :")
        task_system.detTestRnd(globals(), nbTests=3, nbExec=5)

        print("\nLe coût est :")
        task_system.parCost()

    except ValueError as e: 
        print(f"Erreur détectée : {e}")
