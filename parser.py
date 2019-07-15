from lexer import *
from tree import *
# from tabletext import *

error_table = {"Wrong delimiter": -1, "Wrong key_word": -2, "No such identifier": -3, "Wrong integer": -4,
               "Must be empty": -5, "Missing lexema \'unsigned-integer\'": -6, "Semantical error: label is already declareted": -7}


temp = lexer("test2.txt")
lex_list = temp[1]
lex_list_err = temp[0]
tree = Tree()


def scan(dictionary, value):
    for key, v in dictionary.items():
        if v == value:
            return key


def err(err_number, err_pos):
    tree.add(err_number)
    tree.current_element = tree.current_element.parent_element
    tree.print_tree()
    print(scan(error_table, err_number))
    print(' line :' + str(lex_list_err[err_pos][2]) + ' column: ' + str(lex_list_err[err_pos][3]))
    print('lexema: ' + str(lex_list[err_pos]))
    quit()


def declaration_list_proc(i):
    tree.add('declarations-list')
    lexem = lex_list[i]
    if lexem == 41:
        tree.add('< empty >')
        tree.current_element = tree.current_element.parent_element
    else:
        err(-5, i)
    lexem = lex_list[i]
    tree.current_element = tree.current_element.parent_element
    return i


def parameters_list_proc(i):
    tree.add('parameters-list')
    lexem = lex_list[i]
    if lexem == 40:
        tree.add(scan(table.s_sep_dic, lexem))
        tree.current_element = tree.current_element.parent_element
        i += 1
        i = declaration_list_proc(i)
        lexem = lex_list[i]
        if lexem == 41:
            tree.add(scan(table.s_sep_dic, lexem))
            tree.current_element = tree.current_element.parent_element
            i+=1
        else:
            err(-1, i)
    else:
        tree.add('< empty >')
        tree.current_element = tree.current_element.parent_element
        # i += 1
        print(i)
    tree.current_element = tree.current_element.parent_element
    return i


def label_list_proc(i):
    tree.add('labels-list')
    lexem = lex_list[i]
    if lexem == 44:
        tree.add(scan(table.s_sep_dic, lexem))
        tree.current_element = tree.current_element.parent_element
        i += 1
        lexem = lex_list[i]
        if scan(table.dig_dic, lexem):
            tree.add('unsigned-integer')
            tree.add(scan(table.dig_dic, lexem))
            tree.current_element = tree.current_element.parent_element
            tree.current_element = tree.current_element.parent_element
            i += 1
            i = label_list_proc(i)
    else:
        tree.add('< empty >')
        tree.current_element = tree.current_element.parent_element
    tree.current_element = tree.current_element.parent_element
    return i


def label_declarations_proc(i):
    tree.add('label-declarations')
    lexem = lex_list[i]
    if lexem == 405:
        tree.add(scan(table.key_dic, lexem))
        tree.current_element = tree.current_element.parent_element
        i += 1
        lexem = lex_list[i]
        tree.add('unsigned-integer')
        if scan(table.dig_dic, lexem):
            tree.add(scan(table.dig_dic, lexem))
            tree.current_element = tree.current_element.parent_element
            tree.current_element = tree.current_element.parent_element
            i += 1
            i = label_list_proc(i)
        else:
            err(-6, i)
        lexem = lex_list[i]
        if lexem == 59:
            tree.add(scan(table.s_sep_dic, lexem))
            tree.current_element = tree.current_element.parent_element
        else:
            err(-1, i)
        i += 1
    elif lexem == 402:
        tree.add('< empty >')
        tree.current_element = tree.current_element.parent_element
    else:
        err(-2, i)
    tree.current_element = tree.current_element.parent_element


    # lexem = lex_list[i]
    return i


def declarations_proc(i):
    tree.add('declarations')
    i = label_declarations_proc(i)
    tree.current_element = tree.current_element.parent_element
    return i

def statement_list_proc(i):
    tree.add('statements-list')
    lexem = lex_list[i]
    if lexem == 403:
        tree.add('< empty >')
        tree.current_element = tree.current_element.parent_element
    else:
        err(-5, i)
    tree.current_element = tree.current_element.parent_element
    return i

# def statement_list_proc(i):
#     lexem = lex_list[i]
#     if lexem == 1002:
#         tree.add('statements-list')
#         tree.add('st')
#         tree.add(scan(table.idn_dic, lexem))
#         tree.current_element = tree.current_element.parent_element
#         i += 1
#         if lex_list[i] == 1002 or lex_list[i] == 407:
#             i = statement_list_proc(i)
#         elif lex_list[i] == 403 or lex_list[i] == 1003:
#             tree.add('statements-list')
#             tree.add('< empty >')
#             tree.current_element = tree.current_element.parent_element
#             tree.current_element = tree.current_element.parent_element
#         lexem = lex_list[i]
#     elif lex_list[i] == 407:
#         tree.add('statements-list')
#         tree.add('st')
#         tree.add(scan(table.key_dic, 407))
#         tree.current_element = tree.current_element.parent_element
#         tree.current_element = tree.current_element.parent_element
#         i += 1
#         if lex_list[i] == 1002:
#             i = statement_list_proc(i)
#         elif lex_list[i] == 403 or lex_list[i] == 1003:
#             tree.add('statements-list')
#             tree.add('< empty >')
#             tree.current_element = tree.current_element.parent_element
#             tree.current_element = tree.current_element.parent_element
#             # tree.current_element = tree.current_element.parent_element
#         lexem = lex_list[i]
#
#         tree.current_element = tree.current_element.parent_element

    if lexem == 1003:
        tree.add(scan(table.idn_dic, lexem))
        tree.current_element = tree.current_element.parent_element
        tree.current_element = tree.current_element.parent_element
        i += 1
        if lex_list[i] == 1002:
            i = statement_list_proc(i)
        elif lex_list[i] == 403 or lex_list[i] == 1003:
            tree.add('statements-list')
            tree.add('< empty >')
            tree.current_element = tree.current_element.parent_element
            tree.current_element = tree.current_element.parent_element
        elif lex_list[i] == 407:
            tree.add('statements-list')
            tree.add('st')
            tree.add(scan(table.key_dic, 407))
            tree.current_element = tree.current_element.parent_element
            tree.current_element = tree.current_element.parent_element
            i += 1
            if lex_list[i] == 1002:
                i = statement_list_proc(i)
            elif lex_list[i] == 403 or lex_list[i] == 1003:
                tree.add('statements-list')
                tree.add('< empty >')
                tree.current_element = tree.current_element.parent_element
                tree.current_element = tree.current_element.parent_element
            lexem = lex_list[i]
            tree.current_element = tree.current_element.parent_element
        tree.current_element = tree.current_element.parent_element

    # elif lexem == 403:
    #     tree.add('statements-list')
    #     tree.add('< empty >')
    #     tree.current_element = tree.current_element.parent_element
    #     tree.current_element = tree.current_element.parent_element
    # else:
    #     err(-5, i)
    print(lexem)
    return i


def block_proc(i):
    tree.add('block')
    lexem = lex_list[i]
    i = declarations_proc(i)
    lexem = lex_list[i]
    if lexem == 402:
        tree.add(scan(table.key_dic, lexem))
        tree.current_element = tree.current_element.parent_element
    else:
        err(-2, i)
    i += 1
    i = statement_list_proc(i)
    lexem = lex_list[i]

    if lexem == 403:
        tree.add(scan(table.key_dic, lexem))
        tree.current_element = tree.current_element.parent_element
    else:
        err(-2, i)
    tree.current_element = tree.current_element.parent_element
    return i


def procedure_identifier_proc(i):
    lexem = lex_list[i]
    tree.add('procedure-identifier')
    tree.add('identifier')
    if lexem >= 1000:
        tree.add(scan(table.idn_dic, lexem))
        tree.current_element = tree.current_element.parent_element
    else:
        err(-3, i)
    tree.current_element = tree.current_element.parent_element
    tree.current_element = tree.current_element.parent_element


def program_proc():
    tree.add('program')
    i = 0
    lexem = lex_list[i]
    if lexem == 401:
        tree.add(scan(table.key_dic, lexem))
        tree.current_element = tree.current_element.parent_element
        i += 1
        lexem = lex_list[i]
        procedure_identifier_proc(i)
        i += 1
        lexem = lex_list[i]
        if lexem == 59:
            tree.add(scan(table.s_sep_dic, lexem))
            tree.current_element = tree.current_element.parent_element
        else:
            err(-1, i)
        i += 1
        i = block_proc(i)
        i += 1
        lexem = lex_list[i]
        if lexem == 46:
            tree.add(scan(table.s_sep_dic, lexem))
            tree.current_element = tree.current_element.parent_element
        else:
            err(-1, i)
            #################
    elif lexem == 404:
        tree.add(scan(table.key_dic, lexem))
        tree.current_element = tree.current_element.parent_element
        i += 1
        lexem = lex_list[i]
        procedure_identifier_proc(i)
        i += 1
        i = parameters_list_proc(i)
        # i += 1
        lexem = lex_list[i]
        if lexem == 59:
            tree.add(scan(table.s_sep_dic, lexem))
            tree.current_element = tree.current_element.parent_element
        else:
            err(-1, i)
        i += 1
        i = block_proc(i)
        i += 1
        lexem = lex_list[i]
        # print(lexem)
        if lexem == 59:
            tree.add(scan(table.s_sep_dic, lexem))
            tree.current_element = tree.current_element.parent_element
        else:
            err(-1, i)
    else:
        err(-2, i)
    tree.current_element = tree.current_element.parent_element

def signal_program_proc():
    if lex_list:
        program_proc()
        print(lex_list)
        tree.print_tree()
        print()
        print(error_table)
        print()
        tree.listing()
        # print(lex_list[])
    return tree


if __name__ == '__main__':
    # print(lex_list)
    signal_program_proc()
