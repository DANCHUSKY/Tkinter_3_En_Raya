import sqlite3
import os


class Database:

    def __init__(self):
        # Establece la ruta del archivo de base de datos
        db_file = './database/data.db'

        # Verifica si el directorio existe, si no, lo crea
        if not os.path.exists(os.path.dirname(db_file)):
            os.makedirs(os.path.dirname(db_file))

        # Verifica si la base de datos existe, si no, la crea
        if not os.path.exists(db_file):
            self.__create_database(db_file)

        # Inicializa la conexión a la base de datos y el cursor
        self.Conexion = sqlite3.connect(db_file)
        self.cursor = self.Conexion.cursor()

    def __create_database(self, db_file):
        # Crea la base de datos y la tabla
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()

        # Define la sentencia SQL para crear la tabla jugador
        create_table_sql = """
            CREATE TABLE jugador (
                nick TEXT PRIMARY KEY,
                password TEXT NOT NULL,
                victorias INT DEFAULT 0
            );
        """

        # Ejecuta la sentencia SQL para crear la tabla
        cursor.execute(create_table_sql)

        # Cierra la conexión
        connection.close()

    def __Select(self, sql, datos):
        # Abre la conexión
        self.Conexion = sqlite3.connect('./database/data.db')
        self.cursor = self.Conexion.cursor()

        x = self.Conexion.execute(sql, datos).fetchall()

        # Cierra la conexión
        self.cerrarConexion()

        if x:
            return x
        else:
            return 1

    def __Insert(self, sql, datos):
        # Abre la conexión
        self.Conexion = sqlite3.connect('./database/data.db')
        self.cursor = self.Conexion.cursor()

        x = self.Conexion.execute(sql,datos)
        self.Conexion.commit()

        # Cierra la conexión
        self.cerrarConexion()

        if x:
            return True
        else:
            return False

    def __Update(self, sql, datos):
        # Abre la conexión
        self.Conexion = sqlite3.connect('./database/data.db')
        self.cursor = self.Conexion.cursor()

        x = self.Conexion.execute(sql, (datos,))
        self.Conexion.commit()

        # Cierra la conexión
        self.cerrarConexion()

        if x:
            return True
        else:
            return False

    def cerrarConexion(self):
        # Cierra la conexión
        self.Conexion.close()

    def insertPlayer(self, user, password):
        sql = "INSERT INTO Jugador (nick, password) VALUES (?, ?)"
        datos = (user, password)

        # Llama al método __Insert que abrirá y cerrará la conexión
        x = self.__Insert(sql, datos)

        if x:
            return "Jugador creado correctamente"
        else:
            return "Error al crear jugador"

    def existPlayer(self, user):
        sql = "SELECT * FROM Jugador WHERE nick = ?;"
        datos = (user)

        x = self.__Select(sql, datos)

        if x != 1:
            return True
        else:
            return False

    def loginPlayer(self, user, password):
        sql = "SELECT * FROM Jugador WHERE nick = ? AND password = ?;"
        datos = (user, password)

        # Llama al método __Select que abrirá y cerrará la conexión
        x = self.__Select(sql, datos)

        if x != 1:
            return True
        else:
            return False

    def createPlayer(self, playerName, password):
        if self.existPlayer(playerName):
            return "El jugador ya existe"
        else:
            sql = "INSERT INTO Jugador (nick, password) VALUES (?, ?)"
            datos = (playerName, password)

            x = self.__Insert(sql, datos)
            return "Jugador creado correctamente"

    def updatePassword(self, playerName, oldPassword, newPassword):
        if self.existPlayer(playerName):
            sql = "UPDATE Jugador SET password = ? WHERE nick = ? AND password = ?"
            datos = (newPassword, playerName, oldPassword)

            x = self.__Update(sql, datos)
            if x:
                return "Contraseña actualizada correctamente"
            else:
                return "Error al actualizar la contraseña"
        else:
            return "Usuario o contraseña incorrectos para la actualización de la contraseña"

    def incrementarVictorias(self, playerName):
        # Verificar si el jugador existe
        if self.existPlayer(playerName):
            # Incrementar las victorias en 1
            sql = "UPDATE Jugador SET victorias = victorias + 1 WHERE nick = ?"
            datos = (playerName,)

            # Llama al método __Update que abrirá y cerrará la conexión
            self.__Update(sql, datos)
        else:
            print(f"El jugador {playerName} no existe")
