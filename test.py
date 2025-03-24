from bibli import Task, TaskSystem

# --- Déclaration des variables globales ---
X = 0
Y = 0
Z = 0

def t1_run():
    global X
    X = X + 1
    print(f"t1 exécutée ")

def t2_run():
    global X, Y
    Y = Y + X
    print(f"t2 exécutée ")

def t3_run():
    global X, Y, Z
    Z = X + Y
    print(f"t3 exécutée ")

def t4_run():
    global X, Z
    Z = Z - X
    print(f"t4 exécutée")

def t5_run():
    global Z
    Z = Z + Z
    print(f"t5 exécutée ")

def t6_run():
    global Y, X , Z
    Y = X - Z
    print(f"t6 exécutée ")

def t7_run():
    print(f"t7 exécutée ")

# ---CRÉATION DES INSTANCE DE TASK---
t1 = Task("t1", [], ["A"], run=t1_run)
t2 = Task("t2",["A","C"], ["B"], run=t2_run)
t3 = Task("t3",[], ["C"], run=t3_run)
t4 = Task("t4",["A","F"], ["D"], run=t4_run)
t5 = Task("t5",["C"], ["E"], run=t5_run)
t6 = Task("t6",[], ["F"], run=t6_run)
t7 = Task("t7",["B"], ["G"], run=t7_run)


# ---DÉFINIR LES DÉPENDANCES DES TÂCHES---
dependencies = {
   "t1" : [],
    "t2" : ["t1","t3"],
    "t3" : [],
    "t4" : ["t1","t6"],
    "t5" : ["t3"],
    "t6" : [],
    "t7" : ["t2"],
}
""" dependencies = {
      "t1" : [],
     "t2" : ["t1", "t9"],
 } """
""" dependencies = {
    "t1" : ["t2"],
    "t2" : ["t1"],
} """


try:
    task_system = TaskSystem([t1, t2, t3, t4, t5, t6, t7], dependencies)

    niveaux = task_system.decoupage()
    print("Découpage des tâches en niveaux :")
    for i, niveau in enumerate(niveaux, start=0):
        print(f"Niveau {i} : {', '.join(niveau)}")

    # Exécuter les tâches séquentiellement
    print("\nExécution des tâches séquentiellement :")
    task_system.runSeq()

    # Exécution des tâches en même temps
    print("\nExécution des tâches parallèlement :")
    task_system.run()

    # Exécution des tâches en même temps
    print("\nGraphique de dépendance :")
    task_system.draw()

    # Exécution du test de determinisme
    print("\nTest de déterminisme selon les conditions de Bernstein :")
    task_system.detTestRnd()
    
    # Exécution du coût de temps de chaque éxecution (runSeq et run)
    print("\nLe coût est :")
    task_system.parCost()

except ValueError as e: 
    print(f"Erreur détectée : {e}")