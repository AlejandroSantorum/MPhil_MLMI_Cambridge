import sys, fileinput


def change_unfold(file_path, unfold_val):
    pattern = "UnfoldValue"
    for line in fileinput.input(file_path, inplace=1):
        if pattern in line:
            new_line = pattern + " = " + str(unfold_val) + "\n"
            line = line.replace(line, new_line)
        sys.stdout.write(line)



if __name__ == "__main__":
    file_path = sys.argv[1]
    unfold_val = int(sys.argv[2])

    change_unfold(file_path, unfold_val)