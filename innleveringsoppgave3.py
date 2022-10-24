from collections import deque
import time
import csv


startTime = time.time()
class Skuespiller:
    def __init__(self, id, navn):
        self.id = id
        self.navn = navn

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
        self.E = {}
        self.w = {}
        self.filmer = {}

        print("Start filminnlesing")
        with open("movies.tsv", encoding="mbcs") as fil:
            tsv_fil = csv.reader(fil, delimiter="\t")

            for linje in tsv_fil:
                id, tittel, rating = linje[0], linje[1], linje[2]
                self.filmer[id] = Film(tittel,rating)

        print("Start skuespillerinnlesing")
        with open("actors.tsv", encoding="mbcs") as sFil:
            tsv_fil = csv.reader(sFil, delimiter="\t")

            for linje in tsv_fil:
                id, navn, filmerSpilt = linje[0], linje[1], linje[2:len(linje)]
                skuespiller = Skuespiller(id, navn)
                self.leggTilNode(skuespiller)

                for film in filmerSpilt:
                    if film in self.filmer:
                        sk = self.filmer[film].skuespillere
                        sk.append(skuespiller)

                        if len(sk) > 1:
                            for i in range(len(sk) - 2,-1,-1):
                                self.leggTilKant(sk[i],sk[-1],self.filmer[film])

    def leggTilNode(self, sk):
        self.V[sk.id] = sk
        self.E[sk] = []

    def leggTilKant(self, node1, node2, film):
        self.E[node1].append((node2,film.rating))
        self.E[node2].append((node1,film.rating))

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




def antallNoder(graf):
    nodeteller = len(graf.V)
    

    return nodeteller

def antallKanter(graf):
    kantteller = 0

    for kant in graf.E:
        kantteller += len(graf.E[kant])

    return kantteller

def skrivUtSti(graf, idStart, idSlutt):
    path = graf.kortesteStiMellom(graf.V[idStart],graf.V[idSlutt])
    print(path[0])
    for i in range(len(path)-1):
        print(f"===[ {graf.w[path[i],path[i+1]]} ]===>  {path[i+1]}")
        
    print("")




    
def hovedprogram():
    graf = IMDB_Graf()

    endTime = time.time()
    elapsedTime = endTime - startTime

    print(f"Oppgave 1\n\nNodes: {antallNoder(graf)}\nEdges: {int(antallKanter(graf)/2)}\nRuntime:{elapsedTime} seconds\n")

    print("Oppgave 2\n")
    skrivUtSti(graf, "nm2255973", "nm0000460")
    skrivUtSti(graf, "nm0424060", "nm0000243")
    skrivUtSti(graf, "nm4689420", "nm0000365")
    skrivUtSti(graf, "nm0000288", "nm0001401")
    skrivUtSti(graf, "nm0031483", "nm0931324")
  
hovedprogram()