from parser import *

wrong_identifier = []
proc_identifier = []
labels = []
label_identifier = []
key = []
goto_identifier = []
count_proc_identifier = 0


def labels_proc(node):
	if node.leaves[0].leaves[3].val == 'block':
		korn = node.leaves[0].leaves[3].leaves[0].leaves[0]
	else:
		korn = node.leaves[0].leaves[4].leaves[0].leaves[0]
	if korn.val == 'label-declarations':
		buff = []
		if korn.leaves[1].leaves[0].val not in buff:
			labels.append(korn.leaves[1].leaves[0].val)
			buff.append(korn.leaves[1].leaves[0].val)
		else:
			print('Semantical error: label' + str(korn.leaves[1].leaves[0].val) + 'is already declareted')
		korn = korn.leaves[2]
		while korn.leaves[0].val != '< empty >':
			# if korn.leaves[1].leaves[0].val not in buff:
			# print(buff.count(korn.leaves[1].leaves[0].val))
			if buff.count(korn.leaves[1].leaves[0].val) < 3:
				labels.append(korn.leaves[1].leaves[0].val)
				buff.append(korn.leaves[1].leaves[0].val)
				korn = korn.leaves[2]
			else:
				print('Semantical error: label \"' + str(korn.leaves[1].leaves[0].val) + '\" is already declareted')
				break
	return labels


def goto_proc(i):
	for i in label_identifier:
		if i not in goto_identifier:
			goto_identifier.append(i)
	# print(goto_identifier)
	return goto_identifier


def kompile(tree):
	tree = signal_program_proc()
	print("\n\n====================CODE=========================")

	if tree.root.leaves[0].leaves[1].val == "procedure-identifier":
		ident = tree.root.leaves[0].leaves[1].leaves[0].leaves[0].val
		if (ident in proc_identifier):
			wrong_identifier.append(ident)
		proc_identifier.append(ident)
	if tree.root.leaves[0].leaves[0].val == "PROGRAM" or tree.root.leaves[0].leaves[0].val == "PROCEDURE":
		key.append(tree.root.leaves[0].leaves[0].val)
	for i in range(0, len(labels_proc(tree.root))):
		label_identifier.append('$' + str(labels[i]))
	generator(tree.root)


def generator(node):
	if node.leaves[0].leaves[0].val == 'PROGRAM':
		tmp = '; '
		if proc_identifier[count_proc_identifier] != 'PROC' and proc_identifier[count_proc_identifier] != 'DATA' and proc_identifier[count_proc_identifier] != 'SEGMENT' and proc_identifier[count_proc_identifier] != 'CODE' and proc_identifier[count_proc_identifier] != 'ASSUME' and proc_identifier[count_proc_identifier] != 'LABEL':
			tmp += proc_identifier[count_proc_identifier]
		else:
			print('Semantical error: word \'' + proc_identifier[count_proc_identifier] + '\' is wrong name , probably reserved' )
		tmp += '\nDATA SEGMENT\n'
		for i in range(0, len(label_identifier)):
			tmp += '\tlabel ' + str(label_identifier[i]) + '\n'
		tmp += 'DATA ENDS\n'
		tmp += '\n\tASSUME cs:codes\n\n'

		if node.leaves[0].leaves[3].leaves[1].val == 'BEGIN':
			tmp += 'CODE SEGMENT\n'
		for i in goto_proc(i):
			tmp += 'GOTO ' + i + '\n'
		tmp += '\n'
		if node.leaves[0].leaves[3].leaves[3].val == 'END':
			tmp += 'CODE ENDS\n'

		tmp += 'END ' + proc_identifier[count_proc_identifier]
		print(tmp)

	if node.leaves[0].leaves[0].val == 'PROCEDURE':
		tmp = '; '
		if proc_identifier[count_proc_identifier] != 'PROC' and proc_identifier[count_proc_identifier] != 'PROCEDURE' and proc_identifier[count_proc_identifier] != 'DATA' and proc_identifier[count_proc_identifier] != 'SEGMENT' and proc_identifier[count_proc_identifier] != 'CODE' and proc_identifier[count_proc_identifier] != 'ASSUME' and proc_identifier[count_proc_identifier] != 'LABEL':
			tmp += proc_identifier[count_proc_identifier]
		else:
			print('Semantical error: word \'' + proc_identifier[count_proc_identifier] + '\' is wrong name, probably reserved')
		tmp += '\nDATA SEGMENT\n'
		for i in range(0, len(label_identifier)):
			tmp += '\tlabel ' + str(label_identifier[i]) + '\n'
		tmp += 'DATA ENDS\n'
		tmp += '\n\tASSUME cs:codes\n'
		if node.leaves[0].leaves[4].leaves[1].val == 'BEGIN':
			tmp += '\nCODE SEGMENT\n'
			tmp += proc_identifier[count_proc_identifier] + ' proc\n\n'
		for i in goto_proc(i):
			tmp += 'GOTO ' + i + '\n'
		if node.leaves[0].leaves[4].leaves[3].val == 'END':
			tmp += proc_identifier[count_proc_identifier] + ' ENDP\n'
			tmp += 'CODE ENDS\n'

		tmp += 'END ' + proc_identifier[count_proc_identifier]
		print(tmp)


if __name__ == '__main__':
    kompile('test.txt')