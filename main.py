# import requests as req # el modulo resquests es utilizado para extraer datos de apis y páginas web en este caso cogemos los datos de las pagina "https://datos.comunidad.madrid/catalogo/dataset/7da43feb-8d4d-47e0-abd5-3d022d29d09e/resource/ead67556-7e7d-45ee-9ae5-68765e1ebf7a/download/covid19_tia_muni_y_distritos.json"
import json # sirve para convertir objetos python en: JavaScript Object Notation o sea para poder manejar datos de forma serializada en archivos .json
import os # nos permite al acceso de funcionalidades del sistema operativo, por ejemplo la declaración de cwd (usualemente usado y que significa current working directory) es util para no tener que escribir la ruta completa de los archivos que manejamos en el programa.
import time # modulo para trabajar con fechas y horas
from std import Statistics # del modulo std importamos una de sus funciones que es Statistics que nos sirve para poder hacer calculos estadísticos
import matplotlib.pyplot as plt 

cwd = os.path.dirname(__file__) #creamos la variable cwd y le asignamos, usando el módulo os, la ruta del directorio en el que estamos trabajando y que es donde están nuestros archivos.
cct = "casos_confirmados_totales" #creamos la variable cct y le asignamo un string que nos servirá para escribir como leyenda cuando representemos los datos totales
fi = "fecha_informe" #creamos la variable fi y le asignamo un string que nos servirá para escribir como leyenda cuando representemos los datos totales
# res = req.get("https://datos.comunidad.madrid/catalogo/dataset/7da43feb-8d4d-47e0-abd5-3d022d29d09e/resource/ead67556-7e7d-45ee-9ae5-68765e1ebf7a/download/covid19_tia_muni_y_distritos.json").json()


# with open("covid.json", "w", encoding="utf8") as file:
#     json.dump(res, file, ensure_ascii=False, indent=4)

def get_data():
    with open(f"{cwd}/covid.json", encoding="utf8") as file:
        return json.load(file)["data"]


data = get_data()

start = time.perf_counter()
def get_total(dataset, date):
    result = 0
    mun_by_date = filter(lambda mun: mun["fecha_informe"].split(" ")[0] == date, dataset)
    # sum(map(lambda mun: mun["casos_confirmados_totales"] if mun["fecha_informe"].split(" ")[0] == date and mun["casos_confirmados_totales"] else 0, dataset))
    for mun in mun_by_date:
        try:
            result += mun["casos_confirmados_totales"]
        except KeyError:
            continue
    return result

finish = time.perf_counter()

def get_worst(dataset):
    filtered_list = []
    for mun in dataset:
        try:
            mun[cct]
            filtered_list.append(mun)
        except KeyError:
            continue
    
    result = sorted(filtered_list, key= lambda mun: mun[cct] ,reverse=True)
    print("RESULTADO: ",len(result))
    [print(f"{mun['municipio_distrito']}: {mun[cct]}") for mun in result[0:10]]

# get_worst(data[0:199])

data_2 = []

for mun in data:
    try:
        mun[cct]
        data_2.append(mun)
    except KeyError:
        continue

# start = time.perf_counter()

def create_y(dataset):
    result = {}
    for mun in dataset:
        date = mun[fi].split(" ")[0]
        try:
            result[date]
            try:
                result[date] += mun[cct]
            except KeyError:
                continue                
        except KeyError:
            try:
                result[date] = 0
                result[date] += mun[cct]
            except KeyError:
                continue
    return result


Y =create_y(data)
Y = dict(sorted(Y.items(), key= lambda tupla: tupla[0]))

dates = list(Y.keys())
Y = list(Y.values())
X = [num for num in range(1, len(Y) + 1)]


covid_data = Statistics(X, Y)
covid_data.rxy + 2

Y_until65 = Y[:66]
X_until65 = [num for num in range(1, len(Y_until65) + 1)]
# plt.plot(X_until65, Y_until65)
# plt.ylabel("confirmados")
# plt.xlabel("dias")
# plt.show()

Y_after65 = Y[66:]
X_after65 = [num for num in range(67, len(Y) + 1)]

after65 = Statistics(X_after65, Y_after65)
print(after65.rxy)
print(after65.prediction(137))

# plt.plot(X_after65, Y_after65)
# plt.ylabel("confirmados")
# plt.xlabel("dias")
# plt.show()








# plt.plot(X, Y)
# plt.ylabel("confirmados")
# plt.xlabel("dias")
# plt.show()















