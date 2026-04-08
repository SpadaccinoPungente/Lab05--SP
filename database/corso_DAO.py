from database.DB_connect import DB_connect
from model.corso import Corso


class CorsoDAO:

    @staticmethod
    def get_all_corsi():
        """
        Interroga il database e restituisce una lista con tutti i corsi
        """

        result = []
        cnx = DB_connect.get_connection()

        if cnx is None:
            print("Errore di connessione al database.")
            return result

        cursor = cnx.cursor(dictionary=True)

        query = """
                SELECT c.codins, c.crediti, c.nome, c.pd
                FROM corso c
                """

        try:
            cursor.execute(query)
            result = [Corso(**row) for row in cursor]

        except Exception as e: print(f"Errore nell'esecuzione della query: {e}")

        finally:
            cursor.close()
            cnx.close()

        return result

    @staticmethod
    def get_corsi_for_studente(matricola: str):
        """
        Cerca i corsi a cui è iscritto uno studente tramite la sua matricola.
        Restituisce una lista di oggetti Corso, eventualmente vuota.
        """

        result = []
        cnx = DB_connect.get_connection()

        if cnx is None:
            print("Errore di connessione al database.")
            return result

        cursor = cnx.cursor(dictionary=True)

        query = """
                SELECT c.codins, c.crediti, c.nome, c.pd
                FROM iscrizione i, \
                     corso c
                WHERE i.codins = c.codins
                  AND i.matricola = %s
                """

        try:
            cursor.execute(query, (matricola,))
            result = [Corso(**row) for row in cursor]

        except Exception as e: print(f"Errore nell'esecuzione della query: {e}")

        finally:
            cursor.close()
            cnx.close()

        return result