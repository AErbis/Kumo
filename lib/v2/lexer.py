from rply import LexerGenerator
lg = LexerGenerator()
lg.add("ELLIPSIS", r"\.\.\.")
lg.add("NUMBER", r"\d+")
lg.add("EQUALS", r"==")
lg.add("LBRACE", r"{")
lg.add("RBRACE", r"}")
lg.add("LPAREN", r"\(")
lg.add("RPAREN", r"\)")
lg.add("LACUTE", r"<")
lg.add("RACUTE", r">")
lg.add("OR", r"\|")
lg.add("MESSAGE", r"message")
lg.add("OPTIONAL", r"optional")
lg.add("QUEUE", r"queue")
lg.add("C2S", r"c2s")
lg.add("S2C", r"s2c")
lg.add("BI", r"s<->c")
lg.add("IF", r"if")
lg.add("ELSE", r"else")
lg.add("IDENTIFIER", r"[a-zA-Z_][a-zA-Z_0-9]*")
lg.add("SEMICOLON", r";")
lg.add("COLON", r":")
lg.add("COMMA", r",")
lg.add("DOT", r".")
lg.ignore(r"\s+")  # Ignore whitespace
lg.ignore(r"#.*\n")  # Ignore comments

