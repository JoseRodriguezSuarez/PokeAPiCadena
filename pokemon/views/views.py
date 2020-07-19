from django.shortcuts import render  
import requests
import json

#Vista ejecutada desde el template; desencadeana la ejecucion de los diversos metodos del API: PokeAPI
#Metodo  inicial EVOLUTION CHAIN: se consulta la cadena de evolucion
#representada por 'id'
def buscar_cadena(request):
    resultado_busqueda ={}
    data_total={}
    id_cadena_pok = ""
    if 'id' in request.GET:
        evolucion_list=[]
        data_total=[]
       
        id_cadena_pok=request.GET['id']
        url ='https://pokeapi.co/api/v2/evolution-chain/%s' % (id_cadena_pok)
        response = requests.get(url)
        resultado_busqueda = response.json()
        url1 =url_pokemon_1(resultado_busqueda)
        evolucion_list = evoluciones(resultado_busqueda["chain"]["evolves_to"])
        #se agrega el url del primer pokemon en el indice 0, del listado de urls a consultar
        #la coleccion es toda la cadena evolutiva
        evolucion_list.insert(0 ,url1)
        #Ejecucion de las consultas, y creacion del diccionario final por pokemon, y la lista de todos los resultados
        for element in evolucion_list:
            url = element
            id = buscar_id(url)
            data = buscar_pokemon_data(id)
            labels=["Nombre","Estadisticas","Altura","Peso","Id"]
            dictT = dict (zip(labels,data))
            #print (evolucion_list)
            data_total.append(dictT) 
        

        
        print (data_total)
        print("ID buscado: "+ id_cadena_pok)
    return render(request, 'poke.html', { 
        'data_total': data_total,
        'id': id_cadena_pok,
         }
        )
#Consulta si una estructua esta vacia    
def is_empty(data_structure):
    if data_structure:
        #print("No está vacía")
        return False
    else:
        #print("Está vacía")
        return True
#Busqueda de los links del metodo pokemon-species de todos los pokemons que integran la cadena 
#menos el inicial ya que esta por fuera de la lista parametro de esta funcion
#se consulta en cada nivel de evolucion si existen mas como el caso de Eevee
#es extensible hasta el 3er nivel evolutivo aunque no existen casos

def evoluciones(lista_evoluciones):
    evol=[]
    flag = is_empty(lista_evoluciones)
    if flag == False:
        x = 0
        longs=len(lista_evoluciones)
        while x < longs:
            url=lista_evoluciones[x]["species"]["url"]
            lista_evoluciones2=lista_evoluciones[x]["evolves_to"]
            flag=is_empty(lista_evoluciones2)
            if flag == False:
                y = 0
                longs2=len(lista_evoluciones2)
                while y  < longs2:
                    url2=lista_evoluciones2[y]["species"]["url"]
                    evol.append(url2)
                    y += 1
            evol.append(url)
            x += 1
    #print(evol)
    return evol

#Se extrae el url del primer pokemon de la cadena
def url_pokemon_1(dict):
    url_pokemon_primer=dict["chain"]["species"]["url"]
    #print (url_pokemon_primer)
    return url_pokemon_primer

#Ejecuta el metodo de pokemon-Species para consultar el id del pokemon
def buscar_id(url):
    resultado_busqueda ={}
    response = requests.get(url)
    resultado_busqueda = response.json()
    id = resultado_busqueda["id"]
    #print (id)
    #print (resultado_busqueda)
    #print (type(resultado_busqueda))   
    return id

#Ejecuta el metodo Pokemon, para la consulta de la data requerida
def buscar_pokemon_data(id):
    resultado_busqueda ={}
    data=[]
    url ='https://pokeapi.co/api/v2/pokemon/%s'% (id)
    print(url)
    response = requests.get(url)
    resultado_busqueda = response.json()
    nombre=resultado_busqueda["name"]
    data.append(nombre)
    estadisticas=resultado_busqueda["stats"]
    estadisticas=pulir_estadisticas(estadisticas)
    data.append(estadisticas)
    altura=resultado_busqueda["height"]
    data.append(altura)
    peso=resultado_busqueda["weight"]
    data.append(peso)
    id = resultado_busqueda["id"]
    data.append(id)
   #print (data)
    return data

#Extrae la informacion necesaria del listado de estadisticas y las organiza en un diccionario
def pulir_estadisticas(lista_estadisticas):
    idstats=[]
    nastats=[]
    #stats=[]
    x=0
    longs=len(lista_estadisticas)
    while x<longs:
            statsiq = lista_estadisticas[x]["base_stat"]
            idstats.append(statsiq)
            nombreSt = lista_estadisticas[x]["stat"]["name"]
            nastats.append(nombreSt)
            #stats.append( [nombreSt,statsiq] )
            x += 1
    stats1 = dict (zip(nastats,idstats))
    #print (nastats)
    #print (idstats)
    #print (stats)
    #print (stats1)
    return stats1
