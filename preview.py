import DELU, sys, os, time
print(sys.argv)

if __name__ == "__main__":
    arg = sys.argv

    if (len(arg) < 2):
        print("Invalid Arguments. Please Execute With File Path.")
        sys.exit()
    
    path = arg[1]

    if (not os.path.isfile(path)):
        print(f"Invalid File Path: {path}")
        sys.exit()

    DELU.system.auto_refresher()
    
    while __name__ == "__main__":
        with open(path, "r", encoding="utf8") as file:
            text = file.read()
        
        text = text.replace("\\n", "\n")
        text = DELU.FME.edit(text)
        os.system("cls")
        print(text)

        time.sleep(1)