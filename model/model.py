from database.DAO import DAO


class Model:
    def __init__(self):
        self._idMapStudenti = {s.matricola: s for s in DAO.getAllStudenti()}

    def getAllCorsi(self):
        return DAO.getAllCorsi()

    def getIscrittiByCorso(self, codins):
        return DAO.getIscrittiByCorso(codins)

    def getStudente(self, matr_int):
        return self._idMapStudenti.get(matr_int, None)

    def getCorsiByMatricola(self, matr_int):
        return DAO.getCorsiByMatricola(matr_int)