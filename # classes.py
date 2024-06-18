# classes.py

class Paciente:
    def __init__(self, nome, telefone):
        self.nome = nome
        self.telefone = telefone

class Consulta:
    def __init__(self, paciente, data, hora, especialidade):
        self.paciente = paciente
        self.data = data
        self.hora = hora
        self.especialidade = especialidade
