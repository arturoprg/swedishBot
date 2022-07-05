import unidecode
import random


class Palabras:
    def __init__(self,listaTxt = 'sueco.txt'):
        self.listaTxt = listaTxt
        [self.categorias,palabras] = self.Procesar_txt(listaTxt)
        self.dictio = self.Arreglar(palabras)


    def Procesar_txt(self,listaTxt): # Procesa el archivo de texto con los codigos (lista.txt)
        try:
            categorias = []
            palabras = []    # Array para
            nueva_cat = ""

            with open(listaTxt,encoding='utf-8') as archivo:
    	           texto = archivo.readlines()
            # Creamos un vector con los nombres y otro con los codigos
            self.max = texto[0]
            texto = texto[1:]
            for i in texto:
                if i[0] == "-":
                    categorias.append(i[1:-1].capitalize())
                    nueva_cat = "+"
                elif not (i == "\n" or i[0] == '%'):
                    palabras.append(nueva_cat+i)
                    nueva_cat = ""
        except:
            print("Error con el archivo de la lista de códigos")

        return(categorias,palabras)

    def Arreglar(self,palabras):
        try:
            # Cada elemento en dictio es un array de 3 elementos, [Palabra en sueco, Palabra en Ingles, Categoria a la que pertenece]
            cont = 0
            dictio = []
            for palabra in palabras:
                if "+" in palabra[0]:
                    palabra = palabra[1:]
                    categoria = self.categorias[cont]
                    cont = cont+1

                palabra = palabra.replace("\n","")
                palabra = palabra.split("//")[0]
                palabra = palabra.split("\t")
                while '' in palabra:
                    palabra.remove('')
                palabra.append(categoria)
                dictio.append(palabra)
        except:
            input("Error en arreglar")

        return(dictio)

    def palabras_seleccionadas(self,preguntas):
        cont = 0
        dictio2 = []
        for elemento in self.dictio:
            if elemento[-1] in preguntas:
                prob = 2**-int(elemento[2])
                rng = random.uniform(0, 1)
                if rng < prob:
                    dictio2.append(elemento[:-1])

        while(len(dictio2) > int(self.max)):
            del dictio2[random.randint(0,len(dictio2)-1)]

        return (dictio2)
