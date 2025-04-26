# El objetivo es diseñar una aplicación capaz de realizar operaciones CRUD (Crear, Leer, Actualizar y Eliminar) sobre un conjunto de productos.
# Cada producto tendrá atributos como nombre, cantidad, precio y categoría, y la aplicación deberá permitir a los usuarios gestionar esta información
# a través de un menú interactivo por consola.
# Durante este reto, aplicarás conceptos como el diseño de clases orientadas a objetos, 
# conexión a bases de datos con la biblioteca mysql-connector-python, validación de entradas y manejo de excepciones.
# Además, se espera que implementes una interfaz de usuario sencilla y funcional que permita realizar las operaciones con fluidez y control de errores.

import mysql.connector
from mysql.connector import pooling, Error

#Importamos bibliotecas para trabajar con mysql, el módulo para hacer pooling y otro para trabajar los errores
#Para que funcionen las libreriras primero hay que instalar mysql por terminal con el comando: pip install mysql-connector-python

class Conexion:

    def __init__(self):
        #Valores necesarios para conectar a la base de datos
        self.host="rizos.pro"
        self.database="u762720325_pruebas_python"
        self.user="u762720325_admin"
        self.password="IBMpython99@@@"

        #Estos 2 valores son para crear el pool de conexiones
        self.pool_name="pool_conexiones"
        self.pool_size=5

        #Creamos la variable donde almacenaremos el objeto pool con el valor None para poder
        #manejar excepciones en la conexión

        self.pool=None

    def crear_pool(self):

        #Vamos a crear el pool de conexiones gestionando los posibles errores con try except
        try:
            #para crear el pool es necesario usar la siguiente instrucción:
            self.pool=pooling.MySQLConnectionPool(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                pool_name=self.pool_name,
                pool_size=self.pool_size
            )

            print("¡POOL CREADO CON ÉXITO!")

        except Error as e:

            print(f"* ERROR AL CREAR EL POOL: {e}")

    #Creamos le método para conectar a traves del pool
    def obtener_conexion(self):
        #Para obtener conexión primero hay que crear el pool
        #Si está vacío lo creamos llamando al método crear_pool
        if self.pool==None:
            print(f"El pool aún no ha sido creado. Voy a crearlo por ti.")
            self.crear_pool()



        try:
                conn=self.pool.get_connection()
                #lo que hace get_connection() es sacar una de las 5 conexiones disponibles del pool, ya lista para usar
                #y guardarla en conn
                print("Conexión obtenida del pool")
                return conn #Importante retornar el objeto conexion obtenido para poder trabajar con él

        except Error as e:

            print(f"Error al obtener conexión del pool: {e}")

    
    class Inventario:
         
        def __init__(self,conexion):
            
         
             

#Creamos el objeto conexión
conexion=Conexion()
#Obtenemos la conexión del pool
conn=conexion.obtener_conexion()

#A partir de aquí ya podemos trabajar con el cursor y consultas sql
cursor=conn.cursor()
cursor.execute("SELECT * FROM productos")
resultados=cursor.fetchall()
for productos in resultados:
     print(productos)





