from collections import defaultdict
import csv


class Skuespiller:
    def __init__(self, id, navn):
        self.id = id
        self.navn = navn

    def __str__(self):
        return f"Name: {self.navn}"



class Film:
    def __init__(self,tittel, rating, id):
        self.tittel = tittel
        self.rating = rating
        self.id = id

    def __str__(self):
        return f"Tittel: {self.tittel}, ({self.rating})"


class IMDB_Graf:
    nodeteller = 0
    kantteller = 0
    def __init__(self):
        self.noder = {}
        self.kanter = {}
        self.kantmatrise = []
        self.nodeindekser = defaultdict()
        
        filmer = {} 
        filmerListe = {}

        sFil = open("actors.tsv", encoding="mbcs")

        fFil = open("movies.tsv", encoding="mbcs")
        
        with fFil as f:
            fFil_tsv = csv.reader(f, delimiter="\t")
            for linje in fFil_tsv:
                id = linje[0]
                tittel = linje[1]
                rating = linje[2] 

                film = Film(tittel,rating,id)
                filmer[film.id] = film
                filmerListe[film.id] = []
                self.kanter[film] = []
        with sFil as f:
            sFil_tsv = csv.reader(f, delimiter="\t")
            for linje in sFil_tsv:
                id = linje[0]
                navn = linje[1]

                skuespiller = Skuespiller(id, navn)
                self.leggTilNode(skuespiller)

                
                filmBiter = linje[2:len(linje)]
                while len(filmBiter) > 0:
                    if filmBiter[0] in filmerListe:
                        filmerListe[filmBiter.pop(0)].append(skuespiller) 
                    else:
                        filmBiter.pop(0)

                
                # for i in range(2,len(linje)):
                #     if linje[i] in filmerListe:
                #         filmerListe[linje[i]] = node 
                
        for film in filmerListe:
            if filmerListe[film] is not None:
                for i in range(len(filmerListe[film])-1):
                    for j in range(i+1,len(filmerListe[film])):
                        self.leggTilKant(filmerListe[film][i],filmerListe[film][j],filmer[film])



                    


    def leggTilNode(self,sk):
        self.nodeteller = self.nodeteller + 1
        print("N", self.nodeteller)
        if isinstance(sk, Skuespiller):
            self.noder[sk.id] = sk
            for rad in self.kantmatrise:
                rad.append(0)
            self.kantmatrise.append([0] * (len(self.kantmatrise)+1))

            self.nodeindekser[sk.id] = len(self.nodeindekser)
        else:
            raise TypeError("Kun argumenten av klassen 'Node' er tillatt")

    def leggTilKant(self,node1,node2,film):
        self.kantteller = self.kantteller + 1
        print("K", self.kantteller)
        if isinstance(node1, Skuespiller) and isinstance(node2, Skuespiller) and isinstance(film, Film):
            if node1.id in self.noder and node2.id in self.noder:
                self.kanter[film].append([node1,node2])
                self.kantmatrise[self.nodeindekser[node1.id]][self.nodeindekser[node2.id]] = film.rating
                self.kantmatrise[self.nodeindekser[node2.id]][self.nodeindekser[node1.id]] = film.rating
        else:
            raise TypeError("leggTilKant metoden aksepterer kun den rekkefølgen av typer -> Node,Node,Film")

    def skrivUtGraf(self):
        for rad in self.kantmatrise:
            for i in rad:
                print(i, end=" ")
            
def hovedprogram():
    graf = IMDB_Graf()
    # graf.skrivUtGraf()

    nodeteller = 0
    kantteller = 0
    for n in graf.noder:
        nodeteller = nodeteller+1

    for kant in graf.kanter:
        for i in graf.kanter[kant]:
            kantteller = kantteller + 1

    print("Oppgave 1\n")
    print(f"Nodes: {nodeteller}\nEdges: {kantteller}")



hovedprogram()
            

