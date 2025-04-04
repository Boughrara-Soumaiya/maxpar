import threading
import networkx as nx
import time
import random
import matplotlib.pyplot as plt

#---===PROJET PARALLÉLISATION MAXIMALE AUTOMATIQUE===---
# NOM : BOUGHRARA  Prénom : Soumaiya n°:20210765
# NOM : NGUYEN     Prénom : Hieu     n°:20211906 

#---===CLASS TASK===---
class Task: 
    def __init__(self, name, reads=None, writes=None, run=None):
        self.name = name
        self.reads = set(reads) if reads else set()
        self.writes = set(writes) if writes else set()
        self.run = run

#---===CLASS TASKSYSTEM===---
class TaskSystem:
    def __init__(self, tasks, dependencies):
        self.tasks = {task.name: task for task in tasks}
        self.dependencies = dependencies
        self.validate()

    # ---===LISTE DES DEPENDANCES===---
    def getDependencies(self, task_name):
        return list(self.dependencies.get(task_name, []))
    
    # ---===VÉRIFICATION DE LA CONFORMITÉ DES TÂCHES ET DES DEPENDANCES===---
    def validate(self):
        tous_nom_taches = set(self.tasks.keys())
        for task_name, deps in self.dependencies.items():
            if task_name not in tous_nom_taches:
                raise ValueError(f"Tâche inconnue: {task_name}")
            for dep in deps:
                if dep not in tous_nom_taches:
                    raise ValueError(f"Dépendance invalide: {task_name} dépend d'une tâche qui n'existe pas '{dep}'.")

    # ---===DÉCOUPAGE DES TÂCHES EN NIVEAUX===---
    def decoupage(self):
        taches_restantes = set(self.tasks)
        taches_resolues = set()
        niveaux = []
        MAX_ITERATIONS = 1000
        iterations = 0
        
        while taches_restantes:
            iterations += 1
            if iterations > MAX_ITERATIONS:
                raise Exception("Limite d'itérations atteinte, arrêt de la boucle.")
            
            niveau = {task for task in taches_restantes if all(dep in taches_resolues for dep in self.dependencies.get(task, []))}
            
            if not niveau:
                raise Exception("Aucune tâche n'est résolue à ce niveau, peut-être une dépendance circulaire.")
         
            niveaux.append(list(niveau))
            taches_resolues.update(niveau)
            taches_restantes -= niveau
        
        return niveaux

    # ---===EXÉCUTION DES TÂCHES EN SÉQUENTIELLE===---
    def runSeq(self):
        executed = set()  
        while len(executed) < len(self.tasks):
            for task_name, task in self.tasks.items():
                if task_name not in executed and all(dep in executed for dep in self.dependencies.get(task_name, [])):
                    task.run()
                    executed.add(task_name)

    # ---===EXÉCUTION DES TÂCHES PAR NIVEAUX (PARALLELISME)===---
    def run(self):
        niveaux = self.decoupage()
        for niveau in niveaux:
            threads = []
            random.shuffle(niveau)
            for task_name in niveau:
                task = self.tasks[task_name]
                t = threading.Thread(target=task.run)
                threads.append(t)
                t.start()
            for t in threads:
                t.join()

 # ---===MÉTHODE DRAW===---
    def draw(self):
        G = nx.DiGraph()
        
        for task, deps in self.dependencies.items():
            for dep in deps:
                G.add_edge(dep, task)
        pos = nx.nx_agraph.graphviz_layout(G, prog="dot")
       
        plt.figure(figsize=(8, 6))
        nx.draw(G, pos, with_labels=True, node_color="lightgreen", edge_color="green",
                node_size=2000, font_size=10, font_weight="bold", arrows=True, arrowsize=15)
       
        plt.title("Arbre des dépendances")
        plt.show()

    # ---===MÉTHODE DETERMINISTE===---

    def setGlobalVariables(self, x, y, z):
        global X, Y, Z
        X = x
        Y = y
        Z = z

    def getGlobalVariables(self):
        global X, Y, Z
        return {"X": X, "Y": Y, "Z": Z}
    
    def allSame(self, lst):
        first = lst[0]
        for element in lst:
            if element != first:
                return False
        return True
    
    def detTestRnd(self, globals_dict, nbTests=5, nbExec=5):

        for test_i in range(nbTests):
            x = random.randint(0, 100)
            y = random.randint(0, 100)
            z = None

            globals_dict['X'] = x
            globals_dict['Y'] = y
            globals_dict['Z'] = z
            
            print(f"\nTEST {test_i+1}: état initial -> X={x}, Y={y}, Z={z}", end="\n\n")

            resultat_chaque_exec = []

            for exec_i in range(nbExec):
                self.setGlobalVariables(x, y, z)
                self.run()    
                final_state = self.getGlobalVariables()
                resultat_chaque_exec.append(final_state)

                print(f"\nTEST {test_i+1}: état final -> X={x}, Y={y}, Z={z}", end="\n\n")

            if not self.allSame(resultat_chaque_exec):
                print(f"Non déterministe pour l'initialisation X={x}, Y={y}, Z={z}/n")
                print("États finaux observés :", resultat_chaque_exec)
                print("nguyen")
                return False
        print("\nAucune divergence détectée : le système semble déterministe.")
        return True


    # ---===MÉTHODE DU COÛT===---
    def parCost(self, n=5):
        seq = []
        par = []
       
        for _ in range(n):
            start = time.perf_counter()
            self.runSeq()
            end = time.perf_counter()
            seq.append(end - start)
           
            start = time.perf_counter()
            self.run()
            end = time.perf_counter()
            par.append(end - start)
        
        moyenneSeq = sum(seq) / n
        moyennePara = sum(par) / n
        gain = moyenneSeq / moyennePara if moyennePara > 0 else float('inf')
        
        print("\nComparaison des temps d'exécution")
        print(f"Temps moyen séquentiel : {moyenneSeq:.4f} s")
        print(f"Temps moyen parallèle  : {moyennePara:.4f} s")
        print(f"gain : {gain:.2f}x")
        return moyenneSeq, moyennePara, gain

   