from database.DB_connect import get_connection
from model.corso import Corso
from model.studente import Studente


class DAO:

    @staticmethod
    def getAllCorsi():
        conn = get_connection()
        if conn is None: return None

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select * from corso"""

        cursor.execute(query)

        for row in cursor:
            result.append(Corso(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getIscrittiByCorso(codins):
        conn = get_connection()
        if conn is None: return None

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
                select s.matricola, s.cognome, s.nome, s.CDS  
                from studente s
                join iscrizione i on s.matricola = i.matricola
                where i.codins = %s
                """

        cursor.execute(query, (codins,))

        for row in cursor:
            result.append(Studente(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllStudenti():
        conn = get_connection()
        if conn is None: return None

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select * from studente"""

        cursor.execute(query)

        for row in cursor:
            result.append(Studente(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getCorsiByMatricola(matr_int):
        conn = get_connection()
        if conn is None: return None

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
                select c.codins, c.crediti, c.nome, c.pd 
                from corso c, iscrizione i
                where c.codins = i.codins 
                and i.matricola = %s
                order by pd asc
                """

        cursor.execute(query, (matr_int,))

        for row in cursor:
            result.append(Corso(**row))

        cursor.close()
        conn.close()
        return result



