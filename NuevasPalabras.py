import unidecode
import random
listaTxt = 'sueco.txt'



def Procesar_txt(): # Procesa el archivo de texto con los codigos (lista.txt)
    try:
        categorias = []
        palabras = []    # Array para
        nueva_cat = ""

        with open(listaTxt,encoding='utf-8') as archivo:
	           texto = archivo.readlines()
        # Creamos un vector con los nombres y otro con los codigos
        for i in texto:
            if i[0] == "-":
                categorias.append(i[1:-1])
                nueva_cat = "+"
            elif not (i == "\n" or i[0] == '%'):
                palabras.append(nueva_cat+i)
                nueva_cat = ""
    except:
        input("Error con el archivo de la lista de códigos")

    return(categorias,palabras)

def Arreglar(palabras,categorias):
    try:
        #if input("Las preguntas en: E o S?   ").upper() == "E":
        #    ingles = False
        #else:
        #    ingles = True
        ingles = False # Quitar esta linea si se descomentan las lineas anteriores
        cont = 0
        dictio = {}
        for palabra in palabras:
            valor = ""
            val = ""
            clave = ""
            i = 0
            j = 0
            while not palabra[i:i+1] == "\t" and i < len(palabra):
                i = i+1
            clave = palabra[:i]
            for letra in palabra[i:-1]:
                if not letra == "\t":
                    val = val + letra
            while not val[j:j+1] == "\\" and j < len(val):
                j = j+1
            valor = val[:j]

            if clave[0] == "+":
                dictio[categorias[cont]] = ''
                cont = cont + 1
                clave = clave[1:]

            if ingles:
                clave1 = clave
                valor1 = valor
            else:
                clave1 = valor
                valor1 = clave

            if len(clave1)>1:
                clave1 = clave1[0].upper()+clave1[1:].lower()
            if len(valor1)>1:
                valor1 = valor1[0].upper()+valor1[1:].lower()
            dictio[clave1] = valor1
    except:
        input("Error en arreglar")

    return(dictio)

def Inicio(categorias):
    no = False
    nueva = False
    nuevas_cat = []

    while not no:
        print("Estas son las categorias:")
        for i in range(len(categorias)):
            print(f"{i+1}) {categorias[i]}")
        print("Nueva")
        resp = input("\nA que categoria quieres añadir? (escribe el número)\n")
        try:
            if int(resp) in range(len(categorias)+1):
                preguntas = categorias[int(resp)-1]
                no = True
            else:
                print("Ese número no es válido\n")
        except:
            if resp.upper() == "NUEVA":
                nueva = True
            else:
                print("Esa categoría no existe\n")

        if nueva:
            salir = False
            while not salir:
                nueva_cat = input("\nCuál es el nombre de la nueva categoría?\n")

                if not (nueva_cat in categorias):   # Añade una nueva Cat
                    categorias.append(nueva_cat)
                    nuevas_cat.append(nueva_cat)
                    salir = True

                elif nueva_cat.upper() == "SALIR":  # Salir de nueva Cat
                    salir = True
                else:
                    print("Esa categoria ya existe\n")
            nueva = False
    return(preguntas,nuevas_cat)

def palabras_seleccionadas(dictio,preguntas):
    cont = 0
    dictio2 = {}
    voc = False
    for i in dictio:
        if voc and not dictio.get(i) == '':
            dictio2[i] = dictio.get(i)
        if dictio.get(i) == '':
            voc = False
            try:
                if i == preguntas:
                    voc = True
            except:
                pass
    return (dictio2)

def Escribir_txt(dictio,preguntas,nuevas_cat):
    sueco = list(dictio.values())
    ingles = list(dictio.keys())

    with open(listaTxt,encoding='utf-8') as archivo:
        texto = archivo.readlines()

    for i in nuevas_cat:
        texto.append("-"+i+"\n")

    for i in range(len(texto)):
        if texto[i] == ("-" + preguntas+"\n"):
            break

    for j in range(len(dictio)):
        texto.insert(i+1,sueco[j]+"\t\t"+ingles[j]+"\t\t"+"0"+"\n")

    file1 = open(listaTxt,"w")
    file1.writelines(texto)
    file1.close()

    return()

def main():
    salir = False
    dictioNuevas = {}
    [categorias,palabras] = Procesar_txt()
    dictio = Arreglar(palabras,categorias)
    [preguntas,nuevas_cat] = Inicio(categorias)

    dictio2 = palabras_seleccionadas(dictio,preguntas)
    sueco = list(dictio2.keys())
    while not salir:
        nueva_pal_1 = input("\nEscribe la nueva palabra en Sueco: ")
        nueva_pal_2 = input("Ingles: ")
        nueva_pal = nueva_pal_1+" - "+nueva_pal_2
        if "SALIR - " in nueva_pal.upper():
            salir = True
        else:
            try:
                for i in range(len(nueva_pal)):
                    if nueva_pal[i] == "-":
                        break
                es_nueva = True
                for word in dictio2.keys():
                    if nueva_pal[i+2:].upper() == word[:-1].upper():
                        print(f"{nueva_pal[i+2:]} ya está en la lista\n")
                        es_nueva = False
                        break
                for word in dictio2.values():
                    if nueva_pal[:i-1].upper() == word[:-1].upper():
                        print(f"{nueva_pal[:i-1]} ya está en la lista\n")
                        es_nueva = False
                        break
                if es_nueva:
                    dictio2[nueva_pal[i+2:]] = nueva_pal[:i-1]
                    dictioNuevas[nueva_pal[i+2:]] = nueva_pal[:i-1]
            except:
                print("Palabras incorrectas")

    Escribir_txt(dictioNuevas,preguntas,nuevas_cat)
    return()

try:
    main()
except:
    input("Error fatal")
