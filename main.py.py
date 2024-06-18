import json
from datetime import datetime

# Arquivos para armazenar os dados
ARQUIVO_PACIENTES = 'pacientes.json'
ARQUIVO_AGENDAMENTOS = 'agendamentos.json'

def carregar_dados():
    """Carrega os dados dos arquivos JSON."""
    try:
        with open(ARQUIVO_PACIENTES, 'r') as file:
            pacientes = json.load(file)
    except FileNotFoundError:
        pacientes = []

    try:
        with open(ARQUIVO_AGENDAMENTOS, 'r') as file:
            agendamentos = json.load(file)
    except FileNotFoundError:
        agendamentos = []

    return pacientes, agendamentos

def salvar_dados(pacientes, agendamentos):
    """Salva os dados nos arquivos JSON."""
    with open(ARQUIVO_PACIENTES, 'w') as file:
        json.dump(pacientes, file)
    
    with open(ARQUIVO_AGENDAMENTOS, 'w') as file:
        json.dump(agendamentos, file)

def cadastrar_paciente(pacientes, agendamentos):
    """Cadastra um novo paciente."""
    nome = input("Digite o nome do paciente: ")
    telefone = input("Digite o telefone do paciente: ")

    # Verifica se o paciente já está cadastrado pelo telefone
    for paciente in pacientes:
        if paciente['telefone'] == telefone:
            print("Paciente já cadastrado!")
            return

    # Adiciona o paciente à lista de pacientes cadastrados
    pacientes.append({'nome': nome, 'telefone': telefone})
    salvar_dados(pacientes, agendamentos)
    print("Paciente cadastrado com sucesso")

def marcar_consulta(pacientes, agendamentos):
    """Marca uma consulta para um paciente."""
    if not pacientes:
        print("Nenhum paciente cadastrado!")
        return

    # Exibe a lista de pacientes cadastrados para seleção
    for i, paciente in enumerate(pacientes):
        print(f"{i + 1}. {paciente['nome']}")

    paciente_index = int(input("Selecione o número do paciente: ")) - 1

    if paciente_index < 0 or paciente_index >= len(pacientes):
        print("Número de paciente inválido!")
        return

    paciente = pacientes[paciente_index]

    data_hora = input("Digite a data e hora da consulta (dd/mm/yyyy HH:MM): ")

    try:
        # Converte a data e hora para o formato correto
        dia, mes, ano_hora = data_hora.split('/')
        ano, hora = ano_hora.split(' ')
        data_consulta = f"{dia}/{mes}/{ano} {hora}"
        data_consulta_datetime = datetime.strptime(data_consulta, "%d/%m/%Y %H:%M")
    except ValueError:
        print("Formato de data e hora inválido. Use dd/mm/yyyy HH:MM.")
        return

    if data_consulta_datetime < datetime.now():
        print("Não é possível agendar consultas retroativas!")
        return

    # Verifica se a data e hora da consulta já estão ocupadas
    for agendamento in agendamentos:
        if agendamento['data_hora'] == data_consulta and agendamento['paciente'] == paciente['nome']:
            print("Consulta já marcada para este dia e hora!")
            return

    # Adiciona o agendamento à lista de agendamentos
    agendamentos.append({
        'paciente': paciente['nome'],
        'data_hora': data_consulta,
    })
    salvar_dados(pacientes, agendamentos)
    print("Consulta marcada com sucesso")

def cancelar_consulta(pacientes, agendamentos):
    """Cancela uma consulta marcada."""
    if not agendamentos:
        print("Nenhuma consulta agendada!")
        return

    # Exibe a lista de agendamentos para seleção
    for i, agendamento in enumerate(agendamentos):
        print(f"{i + 1}. {agendamento['paciente']} - {agendamento['data_hora']}")

    agendamento_index = int(input("Selecione o número do agendamento a ser cancelado: ")) - 1

    if agendamento_index < 0 or agendamento_index >= len(agendamentos):
        print("Número de agendamento inválido!")
        return

    # Remove o agendamento selecionado da lista de agendamentos
    agendamento = agendamentos.pop(agendamento_index)
    salvar_dados(pacientes, agendamentos)
    print("Consulta cancelada com sucesso")

def menu():
    """Menu principal do sistema."""
    pacientes, agendamentos = carregar_dados()

    while True:
        print("\nMenu:")
        print("1. Cadastrar paciente")
        print("2. Marcar consulta")
        print("3. Cancelar consulta")
        print("4. Sair")

        opcao = input("Selecione uma opção: ")

        if opcao == '1':
            cadastrar_paciente(pacientes, agendamentos)
        elif opcao == '2':
            marcar_consulta(pacientes, agendamentos)
        elif opcao == '3':
            cancelar_consulta(pacientes, agendamentos)
        elif opcao == '4':
            break
        else:
            print("Opção inválida, tente novamente.")

if __name__ == "__main__":
    menu()
