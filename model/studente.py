
class Studente:
    # stessi attributi del database
    def __init__(self, matricola: int, cognome: str, nome: str, CDS: str):
        self.matricola = matricola
        self.cognome = cognome
        self.nome = nome
        self.CDS = CDS

    def __str__(self):
        return f'{self.nome}, {self.cognome} ({self.matricola})'.upper()

    # qua uso la chiave primaria!
    def __eq__(self, other):
        return self.matricola == other.matricola

    def __hash__(self):
        return hash(self.matricola)