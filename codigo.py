#MODULOS-----------------------------------
from fractions import Fraction #para fracciones
import math #para logaritmos
import sys
import operator #para ordenar

##FUNCIONES---------------------------------

def entropia(fuente_inf):
    entropia = 0
    for valor in fuente_inf.values(): #Me va dando cada probabilidad de la fuente (psubi) iterara tantas veces como valores tenga la fuente, es decir, ya son las m veces que quiero iterar
        entropia = entropia + (valor * math.log(Fraction(1, valor),2)) #logaritmo en base 2 del inverso de la probabilidad para esa iteracion

    return entropia

def fuente_informacion_freq_absolutas(nombre_archivo):
    
    fuente_informacion = {} #diccionario que sera mi fuente (alfabeto + frecuencias)
    
    
    
    with open(nombre_archivo, 'r', encoding='utf8') as f: #open abre el archivo; r en modo lectura; f el descriptor de fichero; importante decirle que es utf8 el fichero que sino no carga las ñ ni ´´

        linea = f.readline() #leo primera linea del archivo


        while linea: #mientras que siga habiendo líneas
            #Cojo caracter a caracter de la línea
            for caracter in linea:
                #print(caracter)


                    #Miro si es el caracter de fin de línea en cuyo caso lo agregaré como un doble espacio separado, dos espacios simples vaya, no un nuevo símbolo que sea "  "
                if caracter == "\n":    
                        
                    caracter = " " #convierto el \n en un espacio
                    for i in range(0,2): #0 incluido, 2 excluido --> 2 iteraciones
                        if " " in fuente_informacion: #si ya he añadido antes un espacio
                            fuente_informacion[" "] = fuente_informacion[" "] + 1 #si ya estaba el simbolo solo le sumo una ocurrencia 
                        else:
                            fuente_informacion[" "] = 1 #si es la primera ocurrencia, añado al diccionario el espacio (" ") con una ocurrencia
                   
                else: #si no es el de fin de linea es otro pero que tampoco esta en el alfabeto actualmente

                    #miro si el caracter esta ya en el alfabeto
                    if caracter in fuente_informacion:


                        fuente_informacion[caracter] = fuente_informacion[caracter]+1  #si está le sumo uno a su nº de ocurencias
                    
                    else:
                        
                        fuente_informacion[caracter] = 1  #simplemente le pongo una ocurrencia (al ponerle 1 ocurrencia se añaden la clave y el valor, es decir el caracter y el 1)



            #sigo leyendo la siguiente
            linea = f.readline()
        



      

    #TENIENDO YA EL ALFABETO Y LAS FRECUENCIAS ABS EN EL DICCIONARIO DE NOMBRE fuente_informacion {caracter : freq} las devuelvo
    return fuente_informacion

def fuente_informacion_probabilidades(fuente_freq_abs):

    fuente_de_informacion = {}  

                #alfabeto = []  #defino dos listas para tener separadas ambas partes de la fuente 
                #probabilidades = []


    total_frecuencias = sum(fuente_freq_abs.values()) #sumo los valores de todas las claves del diccionario, es decir, las frecuencias absolutas de todos los simbolos (=TOTAL).
    print("TOTAL = ", total_frecuencias)
    print()
                #OTRA POSIBILIDAD:
                #posicion = 0
                #for i in fuente_freq_abs.keys():
                #    alfabeto.append(i)
                #    posicion = posicion + 1

                #posicion = 0
                #for j in fuente_freq_abs.values():
                #    probabilidades.append(Fraction(j,total_frecuencias))
                #    posicion = posicion + 1


                #print(alfabeto)
                #print (probabilidades)

    fuente_de_informacion = fuente_freq_abs.copy()  #copio tal cual la fuente


    for clave, valor in fuente_de_informacion.items():  #Clave itera las claves del diccionario una a una (fuente_de_informacion['L'] = 1/219) y valor itera por los valores del diccionario, así puedo sobreescribir
        fuente_de_informacion[clave] = Fraction(valor, total_frecuencias) #mantengo el simbolo del alfabeto y el valor para ese simbolo lo reemplazo con la probabilidad (freq relativa)
    
    #IMPORTANTE! 30/219 == 10/73 No nos liemos
    #print(fuente_de_informacion)
    
    return fuente_de_informacion

def montar_particion_base(fuente_de_informacion, codificacion_numentrada, longitud_mensaje):
    extremos_superiores = []
    extremos_inferiores = []

    contador  = 0

    for clave, valor in fuente_de_informacion.items():  #Clave itera las claves del diccionario una a una (fuente_de_informacion['L'] = 1/7) y valor itera por los valores del diccionario
        if contador == 0:
            extremos_inferiores.append(0) #el primer extremo inferior es 0
            extremos_superiores.append(valor+extremos_inferiores[contador])
            contador = contador + 1
            continue #ir a la segunda iteracion del for directamente, porque lo de abajo se aplica a partir de esa y no para la primera (podria poner un else tmb)
        
        extremos_inferiores.append(extremos_superiores[contador-1]) #es el extremo superior del anterior símbolo
        extremos_superiores.append(valor+extremos_inferiores[contador])
        contador = contador + 1

    #YA TENEMOS LA PARTICION BASE HECHA
    print("Extremos Inferiores", extremos_inferiores)
    print()
    print("Extremos Superiores", extremos_superiores)
   
    # 1. Dado el número, localizamos en que intervalo de la particion base estaría comprendido
    # Como los intervalos se asignan de 0 a 1 de manera creciente voy recorriendo los extremos superiores y cuando encuentre el primero que sea menor el numero que ese extremo superior, en ese intervalo va
    print()
    print("Fraccion correspondiente al numero Codificacion", codificacion_numentrada)
    print()

    mensaje = ""

    ###############################################ITERATIVO TANTAS VECES COMO LONGITUD DEL MENSAJE 
    
    for x in range(0, longitud_mensaje): # 0 incluido 3 excluido (long 3)
        i = 0
        letra = ""
        H = 0 #extremos superior e inferior del intervalo a deshacer (en el que ya he decodificado vaya)
        L = 0


        #recorro las claves de la fuente (== particion, porque tiene el mismo nº)
        for simbolo in fuente_de_informacion.keys(): #como sé que la fuente de informacion tiene el mismo tamaño que la particion base, pues aprovecho y así me va iterando por la fuente al ponerla aqui y puedo coger el simbolo cuando enasille el intervalo ("simbolo" sera la letra correspondiente en esa iteracion al intervalo en el que paramos)
            if(codificacion_numentrada < extremos_superiores[i]):
                #se encasilla dentro de él, luego la letra en esa posicion i es la decodificacion
                letra = simbolo
                H = extremos_superiores[i]
                L = extremos_inferiores[i]
                break #salgo del bucle porque ya decodifiqué la letra
            i = i+1
        
        #La letra decodificada la adjunto al mensaje
        
        mensaje = mensaje + letra
        print(letra)

        #actualizo el numero de la codificacion, dando un paso hacia atras en los intervalos
        codificacion_numentrada = Fraction((codificacion_numentrada-L),(H-L))
        print("Cod. Actualizada para localizar en subintervalo", codificacion_numentrada)

    
    ######################### con el nuevo numentrada vuelvo arriba a buscar el subintervalo
    print()
    print("MENSAJE DECODIFICADO:")
    print(mensaje)








################################################################################################################################

    # 1. Leer Texto / Alfabeto del archivo + Fuente Información Frecuencias 


fuente_freq_abs = fuente_informacion_freq_absolutas('/Users/mario/Desktop/Practica_2_SI/datos_2.txt')
print()
print("Freqs. Abs = ", fuente_freq_abs)
print()
     
         
    # 2. Fuente de Información (Alfabeto + probabilidades/Frecuencia Relativa)

#ENTRADA MANUAL CON FRECUENCIAS
#fuente_freq_abs = {}
#fuente_freq_abs = {'A':12, 'B':2, 'C':3, 'D':1, 'E':2, 'F':3, 'G':1, 'H':2, 'I':3, 'J':1, 'K':2, 'L':3, 'M':1, 'N':2, 'Ñ':3, 'O':1, 'P':2, 'Q':3, 'R':1, 'S':2, 'T':3, 'U':1, 'V':2, 'W':3, 'X':1, 'Y':2, 'Z':3}
#fuente_freq_abs = {'E':4, 'T':1, 'A':4, 'R':2, 'S':3}

fuente_de_informacion = fuente_informacion_probabilidades(fuente_freq_abs)

#ENTRADA MANUAL CON PROBABILIDADES
#fuente_de_informacion = {}
#fuente_de_informacion = {'S':Fraction(3, 29), 'E':Fraction(6, 29), 'C':Fraction(2, 29), 'R':Fraction(3, 29), 'T':Fraction(2, 29), 'O':Fraction(4, 29), ' ':Fraction(4, 29), 'D':Fraction(1, 29), 'U':Fraction(2, 29), 'N':Fraction(1, 29), 'G':Fraction(1, 29)}

print("Fuente de Informacion = ", fuente_de_informacion)
print()


    # 3. Partición Base

#-------->>>> ENTRADA NUMERO DECIMAL DECODIFICAR y LONGITUD <<<<--------------------#

codificacion_numentrada = Fraction('0.96402816270036736770957975564255630564009') #lo pongo así para conservar todas las cifras, si lo guardo en una variable regular se pierden, así se mantiene en forma exacta (fracción)
longitud_mensaje = 27
montar_particion_base(fuente_de_informacion, codificacion_numentrada, longitud_mensaje) #tenemos, (el alfabeto + las probabilidades); la lista de extremos superiores; la lista de extremos inferiores


    #4. Entropía

entropia = entropia(fuente_de_informacion)
print()
print("ENTROPÍA = ", entropia)
print()
