DIGITS = "0123456789"      #Character Sets Comparisons
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
OSYMBOLS = "~`!@#$&_\\:"
IDLIST = DIGITS + LETTERS + "_"

class Lexer:
    def __init__(self, text, ongoingMulti_):  #Constructor
        self.douBoolPass = None
        self.text = text
        self.pos = -1
        self.current_char = None
        self.ongoingMulti = ongoingMulti_
        self.advance()

    def advance(self):   #Reads Next Character
        self.lastpos = self.pos
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None #Return "None" if last character

    def StringChk(self): #String Checking
        self.endQt = 0
        stringTxt = ''
        self.advance()
        while self.current_char != None:  #Collects characters inside of double-quotations
            if self.current_char == "\"":
                self.endQt = 1
                self.tokens.append([stringTxt, 'STRING'])  #Create tokens
                self.tokens.append(['\"', 'CLOSE_DOUBLEQT'])
                break
            else:
                stringTxt += self.current_char
            self.advance()
        if self.endQt == 0: self.tokens.append([stringTxt, 'STRING']) #No Closing double-quotations

    def CharChk(self): #Character Checking
        self.advance()
        if self.current_char == '\'': self.tokens.append(['\'', 'CLOSE_SINGLEQT']) #Empty Character Declaration
        else: 
            if self.current_char != None: #Character Declared
                self.tokens.append([self.current_char, 'CHARACTER'])
                self.advance()
                if self.current_char == '\'': self.tokens.append(['\'', 'CLOSE_SINGLEQT']) #Closing single-quotation 


    def SingleOpe(self): #Single-Digit Operation Checking
        singleCharPos = 0                                                      
        if self.lastpos == len(self.text)-1: self.current_char = self.text[self.lastpos]  #If One character only or last character reached 
        else:
            singleCharPos = self.pos - 1
            self.current_char = self.text[singleCharPos]
            while self.current_char in ' \t':  #Goes back to the symbol
                singleCharPos -= 1
                self.current_char = self.text[singleCharPos]
        self.pos = singleCharPos
        if self.current_char == "<":  #Single Operators token creation
            self.tokens.append(['<', 'OPE_LT'])
            self.advance()
        elif self.current_char == ">": 
            self.tokens.append(['>', 'OPE_GT'])
            self.advance()
        elif self.current_char == "=":
            self.tokens.append(['=', 'OPE_ASS'])
            self.advance()
        elif self.current_char == "!":
            self.tokens.append(['!', 'UNRECOGNIZED'])
            self.advance()
        elif self.current_char == "/":
            self.tokens.append(['/', '/'])
            self.advance()
        elif self.current_char == "+":
            self.tokens.append(['+', '+'])
            self.advance()
        elif self.current_char == "-":
            self.tokens.append(['-', '-'])
            self.advance()

    def DoubleOpeChk(self):  #Double-Digit Operation Checking
        try:
            lastChar = self.text[self.pos - 1]  
        except IndexError:   #One-Digit Operator
            self.SingleOpe()
        else:
            if self.dotPass == 1:    #Comments Creation
                self.dotPass = 0
                if self.current_char == ".":
                    lastChar = self.text[self.pos + 1]
                    if lastChar == ".":  #Multi-Line Comment detected
                        self.tokens.append(['...', 'OPEN_MULTI_COMMENT'])
                        self.pos += 1
                        self.FMultiCmnt()
                    else:               #Single-Line Comment detected
                        self.tokens.append(['..', 'SINGLE_COMMENT'])
                        self.SinglCmnt()
                else:   #Single dot 
                    self.tokens.append(['.', 'UNRECOGNIZED'])

            elif self.douBoolPass == 1:  #Boolean Operation Creation
                self.douBoolPass = 0
                if self.current_char == "=":  #"Or Equal" to Boolean Operators
                    if lastChar == "<":
                        self.tokens.append(['<=', 'OPE_LTEQUAL'])
                    elif lastChar == ">":
                        self.tokens.append(['>=', 'OPE_GTEQUAL'])
                    elif lastChar == "=":
                        self.tokens.append(['==', 'OPE_EQUALTO'])
                    elif lastChar == "!":
                        self.tokens.append(['!=', 'OPE_NEQUALTO'])
                    self.advance()
                else:
                    self.SingleOpe()    #Single Boolean Operators

            elif self.divPass == 1: #Division Operators
                self.divPass = 0
                if self.current_char == "/":
                    self.tokens.append(['//', 'OPE_INTDIV'])
                    self.advance()
                else:
                    self.SingleOpe()

            elif self.addPass == 1:  #Addition Symbol Detected
                self.addPass = 0
                if lastChar == "+" and self.current_char == "=":      
                    self.tokens.append(['+=', 'OPE_ADDASS']) #Addition Assignment Operator
                    self.advance()
                else: self.SingleOpe()  #Addition Operator

            elif self.subPass  == 1: #Subtraction Symbol Detected
                self.subPass = 0
                if lastChar == "-" and self.current_char == "=": 
                    self.tokens.append(['-=', 'OPE_SUBASS']) #Subtraction Assignment Operator
                    self.advance()
                else: self.SingleOpe() #Subtraction Operator

    def SinglCmnt(self):   #Single-Line Comment Checking
        max = len(self.text)
        cmntTxt = ''
        if (self.pos + 1) == max - 1:  #No Comment inputted
            self.advance()
        else:
            self.advance()
            while self.pos < max:      #Collects Succeeding Characters
                cmntTxt += self.current_char
                self.advance()
            self.tokens.append([cmntTxt, 'COMMENT'])  #Makes Comment token
            self.advance()

    def FMultiCmnt(self): #Multi-Line Comment Checking
        try:
            self.current_char = self.text[self.pos + 1]   
        except IndexError:   #No succeeding Comments 
            self.ongoingMulti = 1   #Multi-line not closed
            self.advance()
        else:       
            self.pos += 1     #Starting Adjustments
            self.SMultiCmnt()   #Pass collected Comment

    def SMultiCmnt(self):  #Main Creation of multi-line Comments  
        cmntText = ''      
        end = 0
        max = len(self.text)
        try:
            while self.pos < max:  #Collects all characters
                if self.current_char == "." and self.text[self.pos + 1] == "." and self.text[self.pos + 2] == ".":  #Closed Multi-Line Comment 
                    if self.pos != 0 and cmntText !='': self.tokens.append([cmntText, 'COMMENT'])
                    self.tokens.append(['...', 'CLOSE_MULTI_COMMENT'])            
                    self.pos += 2
                    end = 1
                    break
                else:  
                    cmntText += self.current_char
                self.advance()
        except IndexError: #text reading almost finished
            while self.pos < max:  
                cmntText += self.current_char
                self.advance()
            self.tokens.append([cmntText, 'COMMENT'])
            self.ongoingMulti = 1   #Multi-Line C not closed
        else:
            if end != 1: #Multi-Line C not closed
                self.tokens.append([cmntText, 'COMMENT'])
                self.ongoingMulti = 1 
            else:       #Multi-Line closed
                self.ongoingMulti = 0

    def make_Tokens(self):   #Creates Tokens
        self.tokens = []
        self.douBoolPass = 0  #Declaration of needed Variables
        self.divPass = 0
        self.dotPass = 0
        self.addPass = 0
        self.subPass = 0
        while self.current_char != None: #Loops until end of text
            if self.ongoingMulti == 1:  #Multi-Line C not closed
                self.SMultiCmnt()
                self.advance()
            elif self.current_char in ' \t': #Spaces detected
                self.advance()
            elif self.douBoolPass == 1 or self.divPass == 1 or self.dotPass == 1 or self.addPass == 1 or self.subPass == 1:  #Probable Double Operator detected
                self.DoubleOpeChk()
            elif self.current_char == '+':
                self.addPass = 1
                self.advance()
            elif self.current_char == '-':                           #Single Character Detection
                self.subPass = 1
                self.advance()
            elif self.current_char == '*':
                self.tokens.append(['*', 'OPE_MUL'])
                self.advance()
            elif self.current_char == '/':    #Division Operator Detected
                self.divPass = 1
                self.advance()
            elif self.current_char == '%':
                self.tokens.append(['%', 'OPE_MOD'])
                self.advance()
            elif self.current_char in '<>=!': #Boolean Operator Detected
                self.douBoolPass = 1
                self.advance()
            elif self.current_char == '.':    #Probable Comment Detected
                self.dotPass = 1
                self.advance()
            elif self.current_char == '^':
                self.tokens.append(['^', 'OPE_EXP'])
                self.advance()
            elif self.current_char == '(':
                self.tokens.append(['(', 'OPEN_PAREN'])
                self.advance()
            elif self.current_char == ')':
                self.tokens.append([')', 'CLOSE_PAREN'])
                self.advance()
            elif self.current_char == '[':
                self.tokens.append(['[', 'OPEN_SQR'])
                self.advance()
            elif self.current_char == ']':
                self.tokens.append([']', 'CLOSE_SQR'])
                self.advance()
            elif self.current_char == ',':
                self.tokens.append([',', 'COMMA'])
                self.advance()
            elif self.current_char == ';':
                self.tokens.append([';', 'SEMICOLON'])
                self.advance()
            elif self.current_char == "\"":     #String Detected
                self.tokens.append(['\"', 'OPEN_DOUBLEQT'])
                self.StringChk()
                self.advance()
            elif self.current_char == "\'":     #Character Detected
                self.tokens.append(['\'', 'OPEN_SINGLEQT'])
                self.CharChk()
                self.advance()
            elif self.current_char in DIGITS:   #Digits Detected 
                self.tokens.append(self.make_Number())
            elif self.current_char in LETTERS:  #Letters Detected
                self.tokens.append(self.make_Word())
            elif self.current_char in OSYMBOLS: 
                self.tokens.append([self.current_char,'UNRECOGNIZED'])
                self.advance()
            else:
                self.advance()

        if self.douBoolPass == 1 or self.divPass == 1 or self.dotPass == 1 or self.addPass==1 or self.subPass==1: 
            self.DoubleOpeChk()  #Unresolved Operators
        
        for i in self.tokens:   #Output Tokens
            print(f'{i[0]: <20}{i[1]}')

        return self.tokens, self.ongoingMulti   #Give Tokens to Object

    def make_Number(self):   #Integer or Float Creation
        num_str = ''
        dot_count = 0
        while self.current_char != None and self.current_char in DIGITS + '.':  #Collection of Numerical Characters
            if self.current_char == '.':   #Float Detected
                dot_count += 1
            if dot_count == 2: break
            num_str += self.current_char
            self.advance()
        if dot_count == 0:   #Output
            return ([int(num_str), 'INTEGER'])
        else:
            return ([float(num_str), 'FLOAT'])

    def make_Identifier(self, key_str):
        invalid = 0
        while self.current_char != None and self.current_char not in " \t" :  #Terminates if space detected
            if self.current_char in OSYMBOLS and self.current_char != "_": invalid = 1 #Checks invalid Characters
            key_str += self.current_char  #Collects Characters
            self.advance()
        
        if invalid ==0: return ([key_str, 'IDENTIFIER']) #Output
        else: return ([key_str, 'INVALID']) 

    def make_Word(self):  #Built-in Functions or User-Defined Identifiers Creation

        if self.current_char == 'i': 
            self.advance()
            if self.current_char == 'l':
                self.advance()
                if self.current_char == 'i':
                    self.advance()
                    if self.current_char == 'm':
                        self.advance()
                        if self.current_char == 'b':
                            self.advance()
                            if self.current_char == 'a':
                                self.advance()
                                if self.current_char == 'g':
                                    self.advance()
                                    if self.current_char == None or self.current_char in " \t":
                                        return (["ilimbag", 'KEYWORD'])
                                    elif self.current_char == 's':
                                        self.advance()
                                        if self.current_char == None or self.current_char in " \t":
                                            return (["ilimbags", 'KEYWORD'])
                                        else: return self.make_Identifier("ilimbags")
                                    else: return self.make_Identifier("ilimbag")
                                else: return self.make_Identifier("ilimba")
                            else: return self.make_Identifier("ilimb")
                        else: return self.make_Identifier("ilim")    
                    else: return self.make_Identifier("ili")
                else: return self.make_Identifier("il")
            else: return self.make_Identifier("i")

        elif self.current_char == 'l':
            self.advance()
            if self.current_char == 'a':
                self.advance()
                if self.current_char == 'g':
                    self.advance()
                    if self.current_char == 'y':
                        self.advance()
                        if self.current_char == 'a':
                            self.advance()
                            if self.current_char == 'n':
                                self.advance()
                                if self.current_char == None or self.current_char in " \t":
                                    return (["lagyan", 'KEYWORD'])
                                else: return self.make_Identifier("lagyan")
                            else: return self.make_Identifier("lagya")
                        else: return self.make_Identifier("lagy")
                    else: return self.make_Identifier("lag")
                else: return self.make_Identifier("la")
            if self.current_char == 'u':
                self.advance()
                if self.current_char == 't':
                    self.advance()
                    if self.current_char == 'a':
                        self.advance()
                        if self.current_char == 'n':
                            self.advance()
                            if self.current_char == 'g':
                                self.advance()
                                if self.current_char == None or self.current_char in " \t":
                                    return (["lutang", 'RESERVE WORD'])
                                else: return self.make_Identifier("lutang")
                            else: return self.make_Identifier("lutan")
                        else: return self.make_Identifier("luta")
                    else: return self.make_Identifier("lut")
                else: return self.make_Identifier("lu")                   
            else: return self.make_Identifier("l") 

        elif self.current_char == 'h':
            self.advance()
            if self.current_char == 'a':
                self.advance()
                if self.current_char == 'b':
                    self.advance()
                    if self.current_char == 'a':
                        self.advance()
                        if self.current_char == 'n':
                            self.advance()
                            if self.current_char == 'g':
                                self.advance()
                                if self.current_char == None or self.current_char in " \t":
                                    return (["habang", 'KEYWORD'])
                                else: return self.make_Identifier("habang")
                            else: return self.make_Identifier("haban")
                        else: return self.make_Identifier("haba")
                    else: return self.make_Identifier("hab")
                else: return self.make_Identifier("ha")
            else: return self.make_Identifier("h")

        elif self.current_char == 'i': 
            self.advance()
            if self.current_char == 'l': 
                self.advance()
                if self.current_char == 'a': 
                    self.advance()
                    if self.current_char == 'b': 
                        self.advance()
                        if self.current_char == 'a': 
                            self.advance()
                            if self.current_char == 's': 
                                self.advance()
                                if self.current_char == None or self.current_char in " \t":
                                    return (["ilabas", 'KEYWORD'])
                                else: return self.make_Identifier("ilabas")
                            else: return self.make_Identifier("ilaba")
                        else: return self.make_Identifier("ilab")
                    else: return self.make_Identifier("ila")          
                else: return self.make_Identifier("il")
            else: return self.make_Identifier("i")

        elif self.current_char == 'l': 
            self.advance()
            if self.current_char == 'a': 
                self.advance()
                if self.current_char == 'b': 
                    self.advance()
                    if self.current_char == 'a': 
                        self.advance()
                        if self.current_char == 's': 
                            self.advance()
                            if self.current_char == 'm': 
                                self.advance()
                                if self.current_char == 'u': 
                                    self.advance()
                                    if self.current_char == 'n': 
                                        self.advance()
                                        if self.current_char == 'a': 
                                            self.advance()
                                            if self.current_char == None or self.current_char in " \t":
                                                return (["labasmuna", 'KEYWORD'])
                                            else: return self.make_Identifier("labasmuna")
                                        else: return self.make_Identifier("labasmun")
                                    else: return self.make_Identifier("labasmu")
                                else: return self.make_Identifier("labasm")
                            else: return self.make_Identifier("labas")
                        else: return self.make_Identifier("laba")
                    else: return self.make_Identifier("lab")          
                else: return self.make_Identifier("la")
            else: return self.make_Identifier("l")

        elif self.current_char == 'w': 
            self.advance()
            if self.current_char == 'a': 
                self.advance()
                if self.current_char == 'l': 
                    self.advance()
                    if self.current_char == 'a': 
                        self.advance()
                        if self.current_char == None or self.current_char in " \t":
                            return (["wala", 'KEYWORD'])
                        else: return self.make_Identifier("wala")   
                    else: return self.make_Identifier("wal")          
                else: return self.make_Identifier("wa")
            else: return self.make_Identifier("w")
        
        elif self.current_char == 'k': 
            self.advance()
            if self.current_char == 'u': 
                self.advance()
                if self.current_char == 'n': 
                    self.advance()
                    if self.current_char == 'g': 
                        self.advance()
                        if self.current_char == None or self.current_char in " \t":
                            return (["kung", 'KEYWORD'])
                        else: return self.make_Identifier("kung")  
                    else: return self.make_Identifier("kun")          
                else: return self.make_Identifier("ku")
            if self.current_char == 'a':
                self.advance()
                if self.current_char == 'r':
                    self.advance()
                    if self.current_char == 'a':
                        self.advance()
                        if self.current_char == 'k':
                            self.advance()
                            if self.current_char == 't':
                                self.advance()
                                if self.current_char == 'e':
                                    self.advance()
                                    if self.current_char == 'r':
                                        self.advance()
                                        if self.current_char == None or self.current_char in " \t":
                                             return (["karakter", 'RESERVE WORD'])
                                        else: return self.make_Identifier("karakter")
                                    else: return self.make_Identifier("karakte")
                                else: return self.make_Identifier("karakt")
                            else: return self.make_Identifier("karak")
                        else: return self.make_Identifier("kara")
                    else: return self.make_Identifier("kar")
                else: return self.make_Identifier("ka")
            else: return self.make_Identifier("k")

        elif self.current_char == 'n':
            self.advance()
            if self.current_char == 'u':
                self.advance()
                if self.current_char == 'm':
                    self.advance()
                    if self.current_char == 'e':
                        self.advance()
                        if self.current_char == 'r':
                            self.advance()
                            if self.current_char == 'o':
                                self.advance()
                                if self.current_char == None or self.current_char in " \t":
                                    return (["numero", 'RESERVE WORD'])
                                else: return self.make_Identifier("numero")
                            else: return self.make_Identifier("numer")
                        else: return self.make_Identifier("nume")
                    else: return self.make_Identifier("num")
                else: return self.make_Identifier("nu")
            else: return self.make_Identifier("n")

        elif self.current_char == 's':
            self.advance()
            if self.current_char == 'a':
                self.advance()
                if self.current_char == 'l':
                    self.advance()
                    if self.current_char == 'i':
                        self.advance()
                        if self.current_char == 't':
                            self.advance()
                            if self.current_char == 'a':
                                self.advance()
                                if self.current_char == None or self.current_char in " \t":
                                    return (["salita", 'RESERVE WORD'])
                                else: return self.make_Identifier("salita")
                            else: return self.make_Identifier("salit")
                        else: return self.make_Identifier("sali")
                    else: return self.make_Identifier("sal")
                else: return self.make_Identifier("sa")
            else: return self.make_Identifier("s")


def run(text, multiLine):         #Starts Program
    lexer = Lexer(text, multiLine)
    result = lexer.make_Tokens()

    return result      #Give Tokens to Object
