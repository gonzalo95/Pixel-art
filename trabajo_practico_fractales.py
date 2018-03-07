def main():
    '''Funcion principal del programa.'''
    
    print('BIENVENIDO! POR FAVOR INGRESE LOS DATOS SOLICITADOS A CONTINUACION PARA CREAR EL FRACTAL', '\n', '\n')
            
    colores = elegir_colores()
        
    x, y, tam_x, tam_y, esp_x, esp_y = pedir_datos()
            
    monticulos = {}

    pedir_monticulo(x, y, monticulos)     

    nombre = input('Nombre del archivo: ')+'.ppm' 

    fractal = verificar_monticulos(monticulos, x, y)
    crear_head(nombre, x, y, tam_x, tam_y, esp_x, esp_y)
    listar_celdas(fractal, x, y, colores, tam_y, esp_x, esp_y, nombre, tam_x)

#-------------------------------------------------------------

def validar_coordenadas(coor_x, coor_y, num_arena, x, y, monticulos):
    '''Recibe un diccionario, las coordenadas y cantidad de un monticulo y las dimensiones; Devuelve True si los datos son validos, False en caso contrario'''

    if x > coor_x >= 0 and y > coor_y >= 0:
        monticulos[(coor_x, coor_y)] = num_arena
        return True
    
    else:
        return False
    
#-------------------------------------------------------------

def verificar_monticulos(monticulos, x, y):
    '''Recibe el diccionario con coordenadas y cantidades y chequea que no haya valores mayores o iguales a 4'''
    while [celda for celda in monticulos.values() if celda > 3]:
        
        monticulos = estabilizar(monticulos, x, y)
        
    return monticulos      

#-------------------------------------------------------------

def estabilizar(inestable, x, y):
    '''Recibe un el diccionario con los monticulos y las dimensiones. Estabiliza las celdas con cantidad mayor o igual a 4'''
    estable={}

    for celda in [celda for celda in inestable.items() if not celda[1] > 3]:
        estable[celda[0]] = estable.get(celda[0], 0)+celda[1]
    
    for celda in [celda for celda in inestable.items() if celda[1] > 3]:
        parcial = partir_monticulo(celda)
        
        for celda in parcial.items():
            if x > celda[0][0] >= 0 and y > celda[0][1] >= 0:
                estable[celda[0]] = estable.get(celda[0], 0)+celda[1]
              
    return estable

#-------------------------------------------------------------

def partir_monticulo(tupla):
    '''Recibe una tupla con coordenadas y cantidad de una celda y se encarga de repartir la cantidad '''
    estado_parcial={}
   
    columna = tupla[0][0]
    fila = tupla[0][1]
            
    estado_parcial[(columna, fila)] = tupla[1]%4
    estado_parcial[(columna, fila-1)] = tupla[1]//4
    estado_parcial[(columna-1, fila)] = tupla[1]//4
    estado_parcial[(columna, fila+1)] = tupla[1]//4
    estado_parcial[(columna+1, fila)] = tupla[1]//4
    
    return estado_parcial

#-------------------------------------------------------------

def crear_head(nombre, x, y, tam_x, tam_y, esp_x, esp_y):
    '''Recibe el nombre del archivo, las dimensiones, los tamaños de las celdas y los espejados. Escribe las primeras 3 lineas del archivo'''
    
    with open (nombre, 'w') as archivo:
        archivo.writelines(['P3\n', str((x * tam_x) * esp_x), ' ', str((y * tam_y) * esp_y), '\n255\n' ])
        
#-------------------------------------------------------------

def listar_celdas(fractal, x, y, colores, tam_y, esp_x, esp_y, nombre, tam_x):
    '''Recibe las dimensiones, los tamaños de las celdas, los espejados, los diccionarios con los monticulos estables y colores y el nombre del archivo. Le pasa los datos de las filas a escribir_filas y espejado_y''' 
                
    for fila in range(y):
        for pixel_fila in range(tam_y):
            escribir_fila(fila, x, nombre, fractal, colores, esp_x, tam_x)

    espejar_y(fractal, x, y, colores, tam_y, esp_x, esp_y, nombre, tam_x)

#-------------------------------------------------------------
def espejar_y(fractal, x, y, colores, tam_y, esp_x, esp_y, nombre, tam_x):
    ''' Recibe los diccionarios, las dimensiones, los espejados y el nombre. Genera el espejado vertical'''
        
    for num_esp in range(1, esp_y):

        if not num_esp%2:
            for fila in range(y):
                for pixel_fila in range(tam_y):
                    escribir_fila(fila, x, nombre, fractal, colores, esp_x, tam_x)
                    
        else:
            for fila in range(y-1, -1, -1):
                for pixel_fila in range(tam_y):
                    escribir_fila(fila, x, nombre, fractal, colores, esp_x, tam_x)

#-------------------------------------------------------------
def escribir_fila(fila, x, nombre, fractal, colores, esp_x, tam_x):
    ''' Recibe el numero de fila, la dimension espejado y tamaño en x, los diccionarios de colores y monticulos estables y el nombre del archivo. Escribe los pixeles en el archivo y el espejado horizontal'''
    
    with open (nombre, 'a') as archivo:
        
        for columna in range(x):
            color = fractal.get((columna, fila), 0)
            archivo.write(colores[color] * tam_x)

        for num_esp in range(1, esp_x):

            if not num_esp%2:
                    for columna in range(x):
                        color = fractal.get((columna, fila), 0)
                        archivo.write(colores[color] * tam_x)
                        
            else:
                    for columna in range(x-1, -1, -1):
                        color = fractal.get((columna, fila), 0)
                        archivo.write(colores[color] * tam_x)

#-------------------------------------------------------------
                
def validar_datos(x, y, tam_x, tam_y, esp_x, esp_y):
    '''Valida los datos iniciales(deben ser numeros enteros mayores a 0)'''

    if not x > 0 or not y > 0:
        return False
    if not tam_x > 0 or not tam_y > 0:
        return False
    if not esp_x > 0 or not esp_y > 0:
        return False
    
    return True

#-------------------------------------------------------------
def pedir_datos():
    '''Le pide al usuario las dimensiones, los tamaños de las celdas y los espejados'''
    try:
        x = int(input('\nIngrese la cantidad de columnas(horizontal): '))
        y = int(input('Ingrese la cantidad de filas(vertical): '))
        tam_x = int(input('Cantidad de pixeles horizontales por celda: '))
        tam_y = int(input('Cantidad de pixeles verticales por celda: '))
        esp_x = int(input('Espejado en x: '))
        esp_y = int(input('Espejado en y: ')) 
        if not validar_datos(x, y, tam_x, tam_y, esp_x, esp_y):
            raise ValueError
        
    except ValueError:
        print('\nLos datos ingresados anteriormente deben ser numeros mayores a 0')
        return pedir_datos()
    
    return x, y, tam_x, tam_y, esp_x, esp_y
            
#-------------------------------------------------------------
def pedir_monticulo(x, y, monticulos):
    '''Le pide al usuario las coordenadas y cantidades de un monticulo'''
    while True:  
        try:    
            coor_x = int(input('Columna del monticulo: '))
            coor_y = int(input('Fila del monticulo: '))
            num_arena = int(input('Cantidad de arena: '))
    
            if not validar_coordenadas(coor_x, coor_y, num_arena, x, y, monticulos):
                print('\nCoordenadas fuera de rango \n')
                
        except KeyError:
            print('\nNumero no admitido, intente de nuevo\n')
            
        respuesta = input('Desea agregar otro monticulo: ')
        if respuesta == 'no':
            break
            
#-------------------------------------------------------------
def elegir_colores():
    '''Se encarga de preguntarle al usuario si desea utilizar los colores por defecto o si desea personalizarlos'''
    respuesta = input('¿Usar colores por defecto?(negro,magenta, rojo y amarillo): ')

    if respuesta == 'si':
        dic_colores = {0:'0 0 0\n', 1:'255 0 255\n', 2:'255 0 0\n', 3:'255 255 0\n'}

    else:
        dic_colores = listar_colores()

    return dic_colores

#-------------------------------------------------------------
def listar_colores():
    '''Pre condicion: el numero ingresado debe estar entre 1 y 7 inclusive
        Le permite al usuario elegir los colores del fratal ingresando el numero asignado al color'''
    
    listado_colores=['255 0 0\n', '0 255 0\n', '0 0 255\n', '0 0 0\n', '255 255 0\n', '255 0 255\n', '255 255 255\n', '0, 255, 255\n']
    dic_colores={}

    print('\nElija cuatro colores de esta lista\n')
    print('1 = Rojo', '2 = Verde', '3 = Azul', '4 = Negro', '5 = Amarillo', '6 = Magenta', '7 = Blanco', '8 = Cyan', sep='\n', end='\n\n')

    while True:
        try:
            primero=int(input('Primer color: '))
            dic_colores[0] = listado_colores[primero-1]
            segundo=int(input('Segundo color: '))
            dic_colores[1] = listado_colores[segundo-1]
            tercero=int(input('Tercero color: '))
            dic_colores[2] = listado_colores[tercero-1]
            cuarto=int(input('Cuarto color: '))
            dic_colores[3] = listado_colores[cuarto-1]
            if True:
                break
        except IndexError:
            print('\nEl numero ingresado no pertenece a la lista\n')
        except ValueError:
            print('\nUsted debe ingresar un numero\n')
            
    return dic_colores
#-------------------------------------------------------------

main()