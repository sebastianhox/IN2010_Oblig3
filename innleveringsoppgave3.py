from collections import defaultdict, deque
from heapq import heappop, heappush
import time
import csv


startTime = time.time()        
class Skuespiller:
    def __init__(self, id, navn):
        self.id = id
        self.navn = navn

    def __lt__(self, sk):
        return self.navn < sk.navn

    def __str__(self):
        return f"{self.navn}"

class Film:
    def __init__(self,tittel, rating):
        self.tittel = tittel
        self.rating = rating
        self.skuespillere = []

    def __str__(self):
        return f"{self.tittel}, ({self.rating})"


class IMDB_Graf:
    def __init__(self):
        self.V = {}
        self.E = defaultdict(set)
        self.w = {}
        self.nodeIndekser = {}
        filmer = {}

        print("Start filminnlesing")
        with open("movies.tsv", encoding="mbcs") as fil:
            tsv_fil = csv.reader(fil, delimiter="\t")

            for linje in tsv_fil:
                id, tittel, rating = linje[0], linje[1], float(linje[2])
                filmer[id] = Film(tittel,rating)

        print("Start skuespillerinnlesing")
        with open("actors.tsv", encoding="mbcs") as sFil:
            tsv_fil = csv.reader(sFil, delimiter="\t")

            for linje in tsv_fil:
                id, navn, filmerSpilt = linje[0], linje[1], linje[2:len(linje)]
                skuespiller = Skuespiller(id, navn)
                self.leggTilNode(skuespiller)

                for film in filmerSpilt:
                    if film in filmer:
                        sk = filmer[film].skuespillere
                        sk.append(skuespiller)

                        if len(sk) > 1:
                            for i in range(len(sk) - 2,-1,-1):
                                self.leggTilKant(sk[i],sk[-1],filmer[film])

    def leggTilNode(self, sk):
        self.V[sk.id] = sk
        self.nodeIndekser[sk] = len(self.nodeIndekser)

    def leggTilKant(self, node1, node2, film):
        self.E[node1].add((node2,film.rating))
        self.E[node2].add((node1,film.rating))

        self.w[(node1,node2)] = film
        self.w[(node2,node1)] = film
    
    def kortesteStiMellom(self, node1, node2):
        parents = {node1: None}
        queue = deque([node1])
        path = []

        while queue:
            v = deque.popleft(queue)
            for u in self.E[v]:
                if u[0] not in parents:
                    parents[u[0]] = v
                    queue.append(u[0])

        v = node2

        if node2 not in parents:
            return path

        while v:
            path.append(v)
            v = parents[v]
        return path[::-1]

    def chillesteVeiMellom(self, node1, node2):
        dict = defaultdict(lambda: float('inf'))
        queue = [(0, node1)]
        dict[node1] = 0
        parents = {} 
        path = []

        parents[node1] = None
        while queue:
            cost, v = heappop(queue)
            for u in self.E[v]:
                c = cost + (10 - self.w[(v, u[0])].rating)
                if c < dict[u[0]]:
                    dict[u[0]] = c
                    heappush(queue, (c, u[0]))
                    parents[u[0]] = v
        
        v = node2

        if node2 not in parents:
            return path

        while v:
            path.append(v)
            v = parents[v]
        totalvekt = dict[node2]
        liste = [totalvekt, path[::-1]]
        return liste

    def finnKomponenter(self):
        paths = []
        visited = set()


        for v in self.V:
            if self.V[v] not in visited:
                paths.append(self.BFS(self.V[v], visited))

        return paths
    def BFS(self, v, visited):
        queue = deque([v])
        result = set()
        
        while queue:
            v = deque.popleft(queue)
            result.add(v)
            for u in self.E[v]:
                if u[0] not in visited:
                    visited.add(u[0])
                    queue.append(u[0])

        return result
            
def antallNoder(graf):
    nodeteller = len(graf.V)
    

    return nodeteller

def antallKanter(graf):
    kantteller = 0

    for kant in graf.E:
        kantteller += len(graf.E[kant])

    return kantteller

def skrivUtKortesteSti(graf, idStart, idSlutt):
    path = graf.kortesteStiMellom(graf.V[idStart],graf.V[idSlutt])
    print(path[0])
    for i in range(len(path)-1):
        print(f"===[ {graf.w[(path[i],path[i+1])]} ]===>  {path[i+1]}")
        
    print("")

def skrivUtChillesteVei(graf, idStart, idSlutt):
    liste = graf.chillesteVeiMellom(graf.V[idStart],graf.V[idSlutt])
    totalvekt = liste[0]
    path = liste[1]
    print(path[0])
    for i in range(len(path)-1):
        print(f"===[ {graf.w[(path[i],path[i+1])]} ]===>  {path[i+1]}")
        
    print("Total weight:",totalvekt)
    print("")

def hovedprogram():
    graf = IMDB_Graf()

    print(f"Oppgave 1\n\nNodes: {antallNoder(graf)}\nEdges: {int(antallKanter(graf)/2)}\n")

    print("Oppgave 2\n")
    skrivUtKortesteSti(graf, "nm2255973", "nm0000460")
    skrivUtKortesteSti(graf, "nm0424060", "nm0000243")
    skrivUtKortesteSti(graf, "nm4689420", "nm0000365")
    skrivUtKortesteSti(graf, "nm0000288", "nm0001401")
    skrivUtKortesteSti(graf, "nm0031483", "nm0931324")

    print("Oppgave 3\n")

    skrivUtChillesteVei(graf, "nm2255973", "nm0000460")
    skrivUtChillesteVei(graf, "nm0424060", "nm0000243")
    skrivUtChillesteVei(graf, "nm4689420", "nm0000365")
    skrivUtChillesteVei(graf, "nm0000288", "nm0001401")
    skrivUtChillesteVei(graf, "nm0031483", "nm0931324")

    

    komponenter = graf.finnKomponenter()
    dict = defaultdict(lambda: 0)


    for komp in komponenter:
        dict[len(komp)] = dict[len(komp)] + 1

    print("Oppgave 4\n")
    for k in dict:
        print("There are",dict[k],"components of size",k)

    endTime = time.time()
    elapsedTime = endTime - startTime

    print("\n\nRuntime:",elapsedTime)

  
hovedprogram()