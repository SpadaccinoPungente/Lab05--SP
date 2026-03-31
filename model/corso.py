
class Corso:
    # stessi attributi del database
    def __init__(self, codins: str, crediti: int, nome: str, pd: int):
        self.codins = codins
        self.crediti = crediti
        self.nome = nome
        self.pd = pd

    def __str__(self):
        return f"{self.nome} ({self.codins})"

    # qua uso la chiave primaria!
    def __eq__(self, other):
        return self.codins == other.codins

    def __hash__(self):
        return hash(self.codins)