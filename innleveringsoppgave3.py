import time
import csv


startTime = time.time()
class Skuespiller:
    def __init__(self, id, navn):
        self.id = id
        self.navn = navn

    def __str__(self):
        return f"Name: {self.navn}"

class Film:
    def __init__(self,tittel, rating):
        self.tittel = tittel
        self.rating = rating
        self.skuespillere = []

    def __str__(self):
        return f"Tittel: {self.tittel}, ({self.rating})"


class IMDB_Graf:
    def __init__(self):
        self.V = set()
        self.E = {}
        self.w = {}
        filmer = {}

        print("Start filminnlesing")
        with open("movies.tsv", encoding="mbcs") as fil:
            tsv_fil = csv.reader(fil, delimiter="\t")

            for linje in tsv_fil:
                id, tittel, rating = linje[0], linje[1], linje[2]
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
                                self.leggTilKant(sk[i],sk[-1],filmer[film].rating)

    def leggTilNode(self, sk):
        self.V.add(sk)
        self.E[sk] = []

    def leggTilKant(self, node1, node2, vekt):
        self.E[node1].append((node2,vekt))
        self.E[node2].append((node1,vekt))

        self.w[(node1,node2)] = vekt
        self.w[(node2,node1)] = vekt
def antallNoder(graf):
    nodeteller = len(graf.V)
    

    return nodeteller

def antallKanter(graf):
    kantteller = 0

    for kant in graf.E:
        kantteller += len(graf.E[kant])

    return kantteller

    
def hovedprogram():
    graf = IMDB_Graf()

    endTime = time.time()
    elapsedTime = endTime - startTime

    print(f"Oppgave 1\n\nNodes: {antallNoder(graf)}\nEdges: {int(antallKanter(graf)/2)}\nRuntime:{elapsedTime} seconds")
    

    
hovedprogram()