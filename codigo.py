# dado que la funcion SHA1 solo toma caracteres (72 bits) de entrada
# y devuelve un resultado con 40, es logico pensar que la funcion es
# periodica en algun momento.
# la idea entonces es encontar una colision de hash, calcular la
# frecuencia de la periodicidad de la funcion, y finalmente usar
# my_func(r,n) con una entrada equivalente mucho menor, calculable.

# la funcion dada, con un par de modificaciones para
# hacerla compatible con python 3.6.2.
# es totalmente equivalente a la original.
import hashlib
def my_func(r, n):
    for i in range(n):
        r = r.encode('utf-8')
        r = hashlib.sha1(r[:9]).hexdigest()
    return r



# la funcion externa que resuelve el problema mas eficientemente.
def my_func2(r, n):
    
    # primero obtenemos la colision de hash, solo nos interesa la posicion
    # datos es una lista debido a que obtiene dos valores resultantes. Es
    # un vector, matematicamente hablando.
    datos = colisionar(r)

    # llamaremos SEMILLA al n en el que ocurre la primer colision.
    # llamaremos INCREMENTO al n de la segunda colision menos el
    # de la primera. Es decir n_2 - semilla. Este dato nos indica
    # cada cuanto la funcion vuelve a valer my_func(r,semilla).
    incremento = datos[0]
    semilla = datos[1]

    # aqui finalmente se hace el calculo, hallamos n2 que es el equivalente
    # al n dado para my_func(r,n).
    # // es una division entera, basicamente truncamos el numero para sacar
    # desde donde comienza la i-esima repeticion de la funcion
    n2 = (( n - semilla ) // incremento) * incremento + semilla
    
    # esto es, entonces, el desplazamiento que habria desde la i-esima
    # colision y el numero dado.
    # n = n2 + desplz
    desplz = n - n2

    # notese que usamos "desplz + semilla + incremento" en vez de solo
    # "desplz + semilla", esto es debido a que la periodicidad comienza
    # desde que ocurre la colision, es decir, la segunda vez que aparece
    # un valor que antes habia aparecido.
    my_func(r, desplz + semilla + incremento)




# esta es la magia del algoritmo y donde se pone mas tedioso, debido a su
# naturaleza recursiva e incremental, esta basado en una tecnica llamada
# "Ataque de cumpleaños".
# la misma propone que la probabilidad de encontrar una colision no es lineal
# a la cantidad de operaciones sino mucho mayor, haciendo que pese a que con
# n! de operaciones como maximo, la probabilidad de encontrar una colision es
# exponencial a la cantidad de elementos analizados.
# es entonces, un metodo probabilistico de encontrar una colision, por lo que
# no se puede determinar la cantidad de iteraciones necesarias.
#
# https://es.wikipedia.org/wiki/Ataque_de_cumplea%C3%B1os
# https://es.wikipedia.org/wiki/Paradoja_del_cumplea%C3%B1os
def colisionar(r):
    # un diccionario de claves de hash, implementado con una lista
    dic = [""]
    colision = False
    i=1 # indice que indica la iteracion actual
    k=0 # indice para buscar hacia atras
    while (colision==False):
        r = r.encode('utf-8') # pequeño bug de codificacion :)
        r = hashlib.sha1(r[:9]).hexdigest()

        # ahora la buscamos en el diccionario
        for j in range(len(dic)):

            # si encuentra una colision
            if (dic[j]==r):
                k=j
                colision=True

        # y agrega r al diccionario de hashs
        dic.append(r)
        # aumentamos el paso en 1
        i+=1

    # una vez que colisione se sale del ciclo while y nos quedamos con los
    # indices i y k que indican cuales son los que colisionaron.
    # como son dos resultados, para devolverlos necesitamos un vector de
    # dos elementos, donde sus componentes seran:
    # resultado = [ incremento, semilla ]
    resultado = [i-k,k]
    return resultado

# la mayor carga de trabajo la tiene el colisionador, que luego de muestras
# practicas ha resuelto el problema en unos muy relativos 40 minutos sobre un
# Core 2 Duo en Windows 10.
# una vez obtenidas la semilla y el incremento, el orden computacional es:
#
# (n - n2)/2 + semilla + incremento
#
# se vuelve muy eficiente si se quieren calcular los resultados de la funcion
# multiples veces para un mismo string de entrada, dado que se pueden reciclar
# la semilla y el incremento.
