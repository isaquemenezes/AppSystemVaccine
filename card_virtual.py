import sys
# import pymysql as pys

def card_virtual():
	# rows, cols = int(input('Entre com a quantidade de Vacinas: ')), 5
	name = str(input('Entre com seu nome: '))

	vacine_book = []
	vacine_book.append(name)

	print(vacine_book)
	print('')

	return vacine_book

#Menu principal
def menu():
	print('')
	print('*************************************************')
	print('\t\tVACCINE DIRECTORY SYSTEM ', flush=False)
	print('*************************************************')
	print('Configurações do sistema: \n')
	print('1. Add Notificações')
	print('2. Add uma vacina')
	print('3. Remove uma existente')
	print('4. Deletar todas')
	print('5. Procurar uma vacina')
	print('6. Exibir todas as Vacinas')
	print('7. Exit ')
	choice = int(input('Entre com a sua escolha= '))
	print('')

	return choice

#add Notification
def add_vacine_notification(notif):
	new_vacine_notif = []

	for i in range(len(notif[0])):
		if i == 0:
			new_vacine_notif.append(str(input('Seu Email*: ')))
			
			if new_vacine_notif[i] == '' or new_vacine_notif[i] == ' ':
				print('Campo obrigatório!')
		
		if i == 1:
			new_vacine_notif.append(str(input('Data (yyyy/mm/dd)*: ')))

			if new_vacine_notif[i] == '' or new_vacine_notif[i] == ' ':
				print('Campo obrigatório!')
		
		if i == 2:
			new_vacine_notif.append(str(input('Local (Pais Estado Cidade): ')))
		
		if i == 3:
			new_vacine_notif.append(str(input('Telefone: ')))

	notif.append(new_vacine_notif)
	return notif



#add contacts
def add_vacine(add):
	new_vacine = []

	for i in range(len(add[0])):
		if i == 0:
			new_vacine.append(str(input('Nome da Vacina*: ')))
			
			if new_vacine[i] == '' or new_vacine[i] == ' ':
				print('Campo obrigatório!')
		
		if i == 1:
			new_vacine.append(str(input('Data (dd/mm/yyyy)*: ')))

			if new_vacine[i] == '' or new_vacine[i] == ' ':
				print('Campo obrigatório!')
		
		if i == 2:
			new_vacine.append(str(input('Local (Pais Estado Cidade): ')))
		
		if i == 3:
			new_vacine.append(str(input('Lote: ')))


	add.append(new_vacine)
	return add

#remoção de arquivos
def remove__existing(vc):
	query = str(
		input('Entre com o nome da vacina para fazer a remoção: '))

	temp = 0

	for i in range(len(vc)):
		if query == vc[i][0]:
			temp = temp +1

			print(vc.pop(i))
			print('Removido com succeso!')

			return vc

	if temp == 0:
		print('Falhou!')

		return vc


#Deleta todos os 'registros'
def delete__all(vc):
	return vc.clear()


#procura os registros
def search_existing(vc):
	choice = int(
		input('Entre com um critério \n\n1. Nome da vacina\n2. Lote \n'))

	temp = []
	check = -1

	if choice == 1:
		query = str(input('Nome: '))

		for i in range(len(vc)):
			if query == vc[i][0]:
				check = i
				temp.append(vc[i])
	
	elif choice == 2:
		query = str(input('Lote: '))

		for i in range(len(vc)):
			if query == vc[i][1]:
				check = i
				temp.append(vc[i])

	else:
		print('Entrada inválida')
		return -1

	if check == -1:
		return -1
	else:
		show_all(temp)
		return check

#Exibi todos os registros
def show_all(vc):
	if not vc:
		print('Lista estar vazia: []')

	else:
		for i in range(len(vc)):
			print(vc[i])

#Thanks
def thanks():
	print('*******************************************************')
	print('VACCINE DIRECTORY SYSTEM.')
	print('*****************************************************')
	sys.exit('Saida...')


# Programa Principal
opcao = 1
vc = card_virtual()

while opcao in (1, 2, 3, 4, 5, 6):
	opcao = menu()
	if opcao == 1:
		notif = add_vacine_notification(vc)
		print('')
		print('Success!')

	elif opcao == 2:
		add = add_vacine(vc)
		print('')
		print('Success!')
			
	elif opcao == 3:
		vc = remove__existing(vc)
		print('')
		print('Success!')

	elif opcao == 4:
		vc = delete__all(vc)
		print('')
		print('Success!')

	elif opcao == 5:
		search = search_existing(vc)

		if search == -1:
			print('A vacina não Encontrada!')
		else:
			print('Success!')

	elif opcao == 6:
		vc = show_all(vc)

	else:
		thanks()


