import json
import csv
import operator

# TUTORIAL DE COMO USAR ISSO
# ESSE PROGRAMA REQUERE UM JSON DO PORTAL DA CAPES
# COMO PEGAR ESSE JSON?
# - Faça sua pesquisa no portal da capes e filtre apenas artigos (Não se esqueça de ir até o fim da página para aplicar os filtros)
# - Abra o inspetor de rede do seu navegador e observe as requisições ao recarregar a pagina
# - procure um GET de status 200 que seja do arquivo pnxs?blendFacetsSeparately=... e retorne um json
# - tente reenviar a requisição mudando o parâmetro limit para um numero maior do que sua quantidade de respostas
# - salve o json que foi retornado como res.jon e coloque junto desse programa
# - rode o programa




class Artigo:
    def formatAuthors(self, authors):
        s = ""
        for a in authors:
            na = ""
            l = a.upper().replace(",","").split(" ")
            for n in l:
                if (len(na) == 0):
                    na += n
                else:
                    na += f" {n[0]}."
            na = na if len(s) == 0 else ";"+na
            s += na
            pass

        return s

    def formatedDate(self):
        s = "" + self.date
        m = ""
        d = ""
        months = ['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez']
        y = s[:4]
        if len(s) > 5:
            m = months[int(s[4:6])-1] + " "
            if len(s) > 7:
                d = s [6:] + " "
        return f"{d}{m}{y}."

    def __init__(self, d) -> None:
        self.authors = d["addata"]["au"]
        self.title = d["sort"]["title"][0]
        self.pub = d["display"]["ispartof"][0]
        self.date = d["sort"]["creationdate"][0]
        self.year = self.date[:4]
        self.description = d["search"]["description"][0]
        self.formatedAuthors = self.formatAuthors(self.authors)
        self.link = "https://rnp-primo.hosted.exlibrisgroup.com/permalink/f/vsvpiv/"+d["control"]["recordid"][0]

    
    def __str__(self) -> str:
        return f"{self.formatedAuthors} {self.title}. {self.pub}, {self.formatedDate()}"

    def toRow(self):
        return [self.title, self.formatedAuthors, self.year, self.description, self.__str__(), self.link]
    

# Opening JSON file
f = open('res.json')


data = json.load(f)
fs = open('planilha.csv', 'w', encoding='UTF8', newline='')
writer = csv.writer(fs)
  

b = data["docs"]
lista = []
writer.writerow(["Titulo", "Autores", "Ano", "Resumo", "Referência ABNT", "link"])



for i in b:
    artigo = Artigo(i["pnx"])
    lista.append(artigo)

lista.sort(key=operator.attrgetter('title'))

for i in range(len(lista)):
    artigo = lista[i]
    writer.writerow(artigo.toRow())


# close the file
fs.close()
f.close()