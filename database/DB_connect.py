import pathlib
import mysql.connector
from mysql.connector import errorcode


class DB_connect:
    """Classe utilizzata per creare e gestire un pool di connessioni al database.
    Implementa un metodo di classe che funziona come factory per fornire le connessioni dal pool."""

    # Manteniamo il pool di connessioni come attributo di classe, non di istanza
    _cnxpool = None

    def __init__(self):
        raise RuntimeError("NON creare un'istanza -> usare il metodo di classe get_connection()!")

    @classmethod
    def get_connection(cls, pool_name="my_pool", pool_size=3) -> mysql.connector.pooling.PooledMySQLConnection:
        """Metodo factory per fornire le connessioni dal pool. Inizializza anche il pool
        se non esiste.

        :param pool_name: Nome del pool
        :param pool_size: Numero di connessioni nel pool
        :return: Connessione al database (mysql.connector.pooling.PooledMySQLConnection)
        """
        if cls._cnxpool is None:
            try:
                cls._cnxpool = mysql.connector.pooling.MySQLConnectionPool(
                    pool_name=pool_name,
                    pool_size=pool_size,
                    option_files=f"{pathlib.Path(__file__).resolve().parent}/connector.cnf"
                )
                return cls._cnxpool.get_connection()
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                    print("Ops! C'è qualcosa che non va con username o password!")
                    return None
                elif err.errno == errorcode.ER_BAD_DB_ERROR:
                    print("Il database ricercato non esiste.")
                    return None
                else:
                    print(err)
                    return None
        else:
            return cls._cnxpool.get_connection()
