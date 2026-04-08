import mysql.connector

from database.DB_connect import DB_connect
from model.studente import Studente


class StudenteDAO:

    @staticmethod
    def get_studenti_by_corso(codins: str) -> list[Studente]:
        """
        Interroga il database e restituisce una lista di oggetti Studente
        iscritti al corso specificato dal codins.
        """

        result = []
        cnx = DB_connect.get_connection()

        if cnx is None:
            print("Errore di connessione al database.")
            return result

        cursor = cnx.cursor(dictionary=True)

        query = """
                SELECT s.matricola, s.nome, s.cognome, s.CDS
                FROM studente s, \
                     iscrizione i
                WHERE s.matricola = i.matricola
                  AND i.codins = %s
                """

        try:
            # Eseguo la query passando il parametro codins in una tupla
            cursor.execute(query, (codins,))

            # Scorro i risultati e creo gli oggetti Studente con il dictionary unpacking
            for row in cursor: result.append(Studente(**row))

        except Exception as e: print(f"Errore nell'esecuzione della query: {e}")

        finally:
            cursor.close()
            cnx.close()

        return result

    @staticmethod
    def get_studente_by_matricola(matricola: str):
        """
        Cerca uno studente tramite la sua matricola.
        Restituisce un oggetto Studente se trovato, altrimenti None.
        """

        result = None
        cnx = DB_connect.get_connection()

        if cnx is None:
            print("Errore di connessione al database.")
            return result

        cursor = cnx.cursor(dictionary=True)

        query = "SELECT * FROM studente WHERE matricola = %s"

        try:
            cursor.execute(query, (matricola,))

            row = cursor.fetchone()

            if row is not None: result = Studente(**row)

        except Exception as e:
            print(f"Errore nell'esecuzione della query: {e}")

        finally:
            cursor.close()
            cnx.close()

        return result

    @staticmethod
    def iscrivi_studente(matricola: str, codins: str) -> bool:
        """
        Iscrive uno studente a un corso.
        Restituisce True se l'inserimento va a buon fine, False se era già iscritto.
        """
        cnx = DB_connect.get_connection()

        if cnx is None:
            print("Errore di connessione al database.")
            return False

        cursor = cnx.cursor()

        query = "INSERT INTO iscrizione (matricola, codins) VALUES (%s, %s)"

        try:
            cursor.execute(query, (matricola, codins))
            cnx.commit() # FONDAMENTALE: conferma l'inserimento nel database!
            return True

        except mysql.connector.IntegrityError:
            # Intercettiamo l'errore di chiave primaria duplicata (studente già iscritto)
            return False

        except Exception as e:
            print(f"Errore nell'esecuzione della query: {e}")
            # Se è un altro tipo di errore, annulliamo eventuali modifiche parziali
            cnx.rollback()
            return False

        finally:
            cursor.close()
            cnx.close()
