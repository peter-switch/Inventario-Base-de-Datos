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
        self.host=""
        self.database="u762720325_pruebas_python"
        self.user="u762720325_admin"
        self.password=""

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
        self.conexion=conexion
        
            
    def insertar_producto(self,nombre,cantidad,precio,categoria):

        try:

            conn=self.conexion.obtener_conexion() #Obtenemos la conexión del pool

            cursor=conn.cursor() #A partir de aquí ya podemos trabajar con el cursor y consultas sql
            
            valores=(nombre,cantidad,precio,categoria)

            sql="INSERT INTO productos (nombre, cantidad, precio, categoria) VALUES (%s,%s,%s,%s)"

            
            
            cursor.execute(sql,valores)
            conn.commit() #Confirma los cambios
            
            print("\nProducto añadido correctamente")

        except Error as e:
            
            print(f"Error al insertar producto {e}")
            

        finally:
            #Una vez procesada la consulta en la bbdd cerramos cursor y devolvemos la conexión al pool.
            cursor.close()
            conn.close()

    def ver_productos(self):
        try:

            conn=self.conexion.obtener_conexion()
            cursor=conn.cursor()
            sql="SELECT * FROM productos ORDER BY cantidad"
            cursor.execute(sql)
            resultado=cursor.fetchall()
            for producto in resultado:
                print(f"Producto: {producto[0]} - Precio: {producto[1]} - Cantidad: {producto[2]} - Categoria: {producto[3]}")


        except Error as e:
            print(f"Error al hacer SELECT: {e}")
        
        finally:
            cursor.close()
            conn.close()

    def borrar_producto(self,nombre):

        try:

            conn=self.conexion.obtener_conexion()
            cursor=conn.cursor()
            sql="DELETE FROM productos WHERE nombre=%s"
            valor=(nombre,)#Necesitamos que sea una tupla para poder añadirlo al cursor
            cursor.execute(sql,valor)
            conn.commit() #Confirma los cambios
            print("Producto eliminado correctamente")


        except Error as e:
            print(f"Error al eliminar producto: {e}")
        
        finally:
            cursor.close()
            conn.close()

    def actualizar_producto(self,nuevo_nombre,nuevo_precio,nueva_cantidad,nueva_categoria,nombre_actual):

        try:

            conn=self.conexion.obtener_conexion()
            cursor=conn.cursor()
            sql="UPDATE productos SET nombre = %s, precio = %s, cantidad = %s, categoria = %s WHERE nombre = %s"
            valor=(nuevo_nombre,nuevo_precio,nueva_cantidad,nueva_categoria,nombre_actual)#Necesitamos que sea una tupla para poder añadirlo al cursor
            cursor.execute(sql,valor)
            conn.commit()  #guardar cambios
            print("Producto actualizado")


        except Error as e:
            print(f"Error al actualizar producto: {e}")
        
        finally:
            cursor.close()
            conn.close()

class Menu:
    #Recibe en el constructor el objeto inventario para poder trabajar con él
    def __init__(self,inventario):
        self.inventario=inventario

    def mostrar_menu(self):
        
        print("\n***Menú Invetario***")
        while True:

            print("""
01. Ver listado de productos.
02. Insertar nuevos productos.
03. Actualizar un producto.
04. Eliminar un producto.
05. Salir
            """)
            opcion=int(input("Selecciona opción: "))

            if opcion==1:
                self.inventario.ver_productos()

            elif opcion==2:
                nombre=input("Nombre: ")
                cantidad=int(input("Cantidad: "))
                precio=float(input("Precio :"))
                categoria=input("Categoría: ")
                self.inventario.insertar_producto(nombre,cantidad,precio,categoria)


            elif opcion == 3:
                nombre_actual = input("Nombre del producto que quieres actualizar: ")
                nuevo_nombre = input("Nuevo nombre: ")
                nuevo_precio = float(input("Nuevo precio: "))
                nueva_cantidad = int(input("Nueva cantidad: "))
                nueva_categoria = input("Nueva categoría: ")
                self.inventario.actualizar_producto(nuevo_nombre,nueva_cantidad,nueva_categoria,nombre_actual)


            elif opcion==4:
                nombre=input("Nombre del producto a eliminar: ")
                self.inventario.borrar_producto(nombre)

            #salimos del menú
            elif opcion==5:
                break
    
if __name__ =="__main__": #Si inventario.py se está ejecutando directamente (no importado en otro archivo), entonces haz esto..
    conexion=Conexion()
    inventario=Inventario(conexion)
    menu=Menu(inventario)
    menu.mostrar_menu()

              



            
        

         
             







