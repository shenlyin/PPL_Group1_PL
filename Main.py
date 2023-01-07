import Lexer_Klak

inputPath = r"C:\Users\JM\Documents\Klak Lexer\test.klk"         #Needed File Paths
outputPath = r"C:\Users\JM\Documents\Klak Lexer\Symbol_Table.txt"

def symbolTable(result):   #Output File Creation
    try:
        outfile = open(outputPath, "r")   #Checks if Output File exist
        outfile.close()
    except FileNotFoundError: outfile = open(outputPath, "w")  #File Doesn't Exist
    else: outfile = open(outputPath, "a")  #File Exists
    outfile.write("SYMBOL TABLE\n")   
    outfile.write("-----------------------------------------------------------------\n")   #Design Part
    startingSt = ['LEXEME', 'TOKEN']
    outfile.write(f'{startingSt[0]: <20}{startingSt[1]}\n')  
    for lines in result:     #Token Writing         
        for lexeme in lines:
            outfile.write(f"{lexeme[0]: <20}{lexeme[1]}\n")
    outfile.write("-----------------------------------------------------------------\n\n")  
    outfile.close()
    return

def Start(): #Starts Program
    try:
        file = open(inputPath, 'r')
    except IOError as error:
        print(f"Error: {error}")
        print("Klak File does not exist")
        exit(0)
    else:
        print("=================================================================")      #Design
        print("                    WELCOME TO KLAK LEXER                       \n") 
        ongoingMulti = 0
        result = []      #Declaration 
        print("SYMBOL TABLE")   
        print("-----------------------------------------------------------------")
        startingSt = ['LEXEME', 'TOKEN']                #Introductory Columns
        print(f'{startingSt[0]: <20}{startingSt[1]}')
        line = file.readline()  
        while line  != "":                  #Reads File per Line
            line = line.replace("\n","")
            tempList = Lexer_Klak.run(line, ongoingMulti)
            result.append(tempList[0])
            ongoingMulti = tempList[1]
            line = file.readline()
        file.close()
        symbolTable(result)     #Pass result to Output File Creation
        print("\n_Process Complete_")
        print("=================================================================")  #Ending Design

Start()  #Starts Program