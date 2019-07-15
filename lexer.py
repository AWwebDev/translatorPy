from tabletext import to_text
import table


def lexer(file_name):
    white_space = [8, 9, 10, 13, 32]
    chars = [i for i in range(65, 90)]
    digits = [i for i in range(48, 57)]
    s_separators = [i for i in table.s_sep_dic.keys()]
    key_words = [i for i in table.key_dic.keys()]
    line = ''
    lex_list = []
    lex_list_out = []
    counter_idns = 1001
    counter_digits = 501
    counter_col = 1
    counter_row = 1
    row = 1
    col = 1

    file = open(file_name)
    ch = file.read(1)
    while ch:
        if ord(ch) in white_space:
            counter_col += 1
            if ch == "\n":
                counter_row += 1
                counter_col = 1
            ch = file.read(1)

        elif ord(ch) in chars:
            line += ch
            col = counter_col
            ch = file.read(1)
            counter_col += 1
            while ch and (ord(ch) in chars or ord(ch) in digits):
                line += ch
                ch = file.read(1)
                counter_col += 1
            if line != '':
                if line in key_words:
                    lex_list.append([line, table.key_dic[line], counter_row, col])
                    lex_list_out.append(table.key_dic[line])
                    line = ''
                else:
                    if line in table.idn_dic.keys():
                        lex_list.append([line, table.idn_dic[line], counter_row, col])
                        lex_list_out.append(table.idn_dic[line])
                        line = ''
                    else:
                        table.idn_dic[line] = counter_idns
                        lex_list.append([line, table.idn_dic[line], counter_row, col])
                        lex_list_out.append(table.idn_dic[line])
                        counter_idns += 1
                        line = ''

        elif ord(ch) in digits:
            col = counter_col
            line += ch
            ch = file.read(1)
            counter_col += 1
            while ord(ch) in digits:
                line += ch
                ch = file.read(1)
            if line in table.dig_dic.keys():
                lex_list.append([line, table.dig_dic[line], counter_row, col])
                lex_list_out.append(table.dig_dic[line])
            else:
                table.dig_dic[line] = counter_digits
                lex_list.append([line, table.dig_dic[line], counter_row, col])
                lex_list_out.append(table.dig_dic[line])
                counter_digits += 1
            line = ''
            counter_col += 1

        elif ord(ch) == 40:
            col = counter_col
            line = ch
            ch = file.read(1)
            counter_col += 1
            if ch == "*":
                flag_comment = 0
                ch = file.read(1)
                counter_col += 1
                while ch:
                    if ch == "*":
                        ch = file.read(1)
                        counter_col += 1
                        if ch == ")":
                            ch = file.read(1)
                            counter_col += 1
                            flag_comment = 1
                            break
                    else:
                        ch = file.read(1)
                        counter_col += 1
                    if ch == "\n":
                        counter_row = 1
                if flag_comment == 0:
                    print("Lexical error: unclosed comment")
                    # lex_list = []
                    # break
            else:
                lex_list.append([line, table.s_sep_dic[line], counter_row, col])
                lex_list_out.append(table.s_sep_dic[line])
                line = ''
                # ch = file.read(1)
            line = ''

        elif ch in s_separators:
            col = counter_col
            line = ch
            counter_col += 1
            lex_list.append([line, table.s_sep_dic[line], counter_row, col])
            lex_list_out.append(table.s_sep_dic[line])
            line = ''
            ch = file.read(1)

        else:
            print("Lexical error at line " + str(counter_row) + ", position " + str(counter_col) + ': unknown symbol \"' + ch + '\"')
            # lex_list = []
            ch = file.read(1)
            counter_col += 1

    if lex_list != []:
        a = to_text(lex_list)
        print(a)

    file.close()

    ret_list = [lex_list, lex_list_out]
    # print(ret_list)
    return ret_list
