import lexer

lexems = []

if __name__ == '__main__':
    lexems = lexer.lexer("test1.txt")
    print(lexems)