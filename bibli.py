import threading
import networkx as nx
import matplotlib.pyplot as plt
import time


#---===PROJET PARALLÉLISATION MAXIMALE AUTOMATIQUE===---
# NOM : BOUGHRARA  Prénom : Soumaiya 

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
        self.tasks = {task.name : task for task in tasks}
        self.dependencies = dependencies
        self.validate()

# ---===LISTE DES DEPENDANCES===---
    def getDependencies(self, task_name):
        return list(self.dependencies.get(task_name, []))
    
    # ---===VÉRIFICATION DE LA CONFORMITER DES TÂCHES ET DES DEPENDANCES===---
    def validate(self):
        tous_nom_taches = set(self.tasks.keys())

        for task_name, deps in self.dependencies.items():
            if task_name not in tous_nom_taches:
                raise ValueError(f"Tâche inconnue: {task_name}")
        for dep in deps:
            if dep not in tous_nom_taches:
                raise ValueError(f"Dépendance invalide: {task_name} dépend d'une tâche qui n'existe pas '{dep}'.")
        
# ---===DÉCOUPAGE DES TACHES EN NIVEAU===---
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

# ---===ÉXECUTION DES TÂCHES EN SÉQUENTIELLE===---
    def runSeq(self):
        executed = set()  
        while len(executed) < len(self.tasks):
            for task_name, task in self.tasks.items():
                if task_name not in executed and all(dep in executed for dep in self.dependencies.get(task_name, [])):
                    task.run()  
                    executed.add(task_name)  

# ---===EXÉCUTION DES TÂCHES PAR NIVEAU (PARALLELISME)===---
    def run(self):
        niveaux = self.decoupage()
        for niveau in niveaux:
            threads = []
            for task_name in niveau:
                task = self.tasks[task_name]
                t = threading.Thread(target=task.run)
                threads.append(t)
                t.start()
            for t in threads:
                t.join()

# ---===MÉTTHODE DRAW===---
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
    def detTestRnd(self):
        for task_name, task in self.tasks.items():
            for copy_task_name, copy_task in self.tasks.items():
                if task_name != copy_task_name:
                    # Condition 1 : 
                    if not task.reads.isdisjoint(copy_task.writes):
                        print(f"Conflit 1 : {task_name} lit une donnée écrite par {copy_task_name}")
                        return False
                    # Condition 2 : 
                    if not task.writes.isdisjoint(copy_task.reads) or not task.writes.isdisjoint(copy_task.writes):
                        print(f"Conflit 2 : {task_name} écrit sur une donnée lue ou écrite par {copy_task_name}")
                        return False

        print("Aucun conflit")
        return True

# ---===MÉTHODE DU COÛT===---
    def parCost(self, n=5):
        seq = []
        par= []

        for _ in range(n):
            # Mesurer le temps d'exécution en séquentiel
            start = time.perf_counter()
            self.runSeq()
            end = time.perf_counter()
            seq.append(end - start)

            # Mesurer le temps d'exécution en parallèle
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
    

