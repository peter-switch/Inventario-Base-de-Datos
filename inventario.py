# El objetivo es diseñar una aplicación capaz de realizar operaciones CRUD (Crear, Leer, Actualizar y Eliminar) sobre un conjunto de productos.
# Cada producto tendrá atributos como nombre, cantidad, precio y categoría, y la aplicación deberá permitir a los usuarios gestionar esta información
# a través de un menú interactivo por consola.
# Durante este reto, aplicarás conceptos como el diseño de clases orientadas a objetos, 
# conexión a bases de datos con la biblioteca mysql-connector-python, validación de entradas y manejo de excepciones.
# Además, se espera que implementes una interfaz de usuario sencilla y funcional que permita realizar las operaciones con fluidez y control de errores.

import mysql.connector
from mysql.connector import pooling, Error
#Importamos bibliotecas para trabajar con mysql, el módulo para hacer pooling y otro para trabajar los errores

class Conexion:

    def __init__(self):
        #Valores necesarios para conectar a la base de datos
        self.host=""
        self.database="u762720325_pruebas_python"
        self.user="u762720325_admin"
        self.password=""

        #Estos 2 valores son para crear el pool de conexiones
        self.pool_name="pool"
        self.pool_size=5

        #Vamos a crear el pool de conexiones gestionando los posibles errores con try except
        try:
            #para crear el pool es necesario usar la siguiente instrucción:
            pool=pooling.MySQLConnectionPool(

                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                pool_name=self.pool_name,
                pool_size=pool_size

            )

            print="¡Pool de conexiones cerado con exito!"


        except Error as e:

            print(f"Error al crear el pool: {e}")

    #Creamos le método para conectar a traves del pool
    def crear_conexion(self):
        pass