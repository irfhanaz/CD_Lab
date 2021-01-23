file_name = input("Enter file name:")
with open(file_name, "r") as fp: 
    lines = fp.readlines()
with open("new_text.txt", "w") as fp:
    for line in lines:
        fp.write(line)
with open("new_text.txt", 'a') as fp:
    fp.write("\nby your side\n")
    fp.write("lyrics by EASHA")
with open("new_text.txt", "r") as fp: 
    lines = fp.readlines()
    count = 1
    for line in lines:
        print("(", count, ") ", line)
        num_of_words = len(line.split())
        num_of_spaces = 0
        for i in line:
            if i.isspace():
                num_of_spaces += 1
        print("[Line (", count, ") has ", num_of_words, " words and ", num_of_spaces, " whitespaces.]\n\n")
        count += 1




