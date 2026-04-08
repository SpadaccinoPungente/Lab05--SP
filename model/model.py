from database.corso_DAO import CorsoDAO
from database.studente_DAO import StudenteDAO


class Model:
    def __init__(self):
        pass

    def get_all_corsi(self):
        return CorsoDAO.get_all_corsi()

    def get_studenti_by_corso(self, corso):
        return StudenteDAO.get_studenti_by_corso(corso)

    def get_studente_by_matricola(self, matricola):
        return StudenteDAO.get_studente_by_matricola(matricola)

    def get_corsi_for_studente(self, matricola):
        return CorsoDAO.get_corsi_for_studente(matricola)

    def iscrivi_studente(self, matricola: str, codins: str) -> bool:
        return StudenteDAO.iscrivi_studente(matricola, codins)

