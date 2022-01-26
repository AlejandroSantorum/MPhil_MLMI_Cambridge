import sys, fileinput

def build_new_context_width(context_width):
    neg_list = [-i for i in range(1,context_width+1)]
    neg_list = neg_list[::-1] # reversing list
    ret = neg_list + [0] + ["+"+str(i) for i in range(1,context_width+1)]
    ret_str = "{"
    for item in ret:
        ret_str += str(item)+","
    ret_str = ret_str[:-1] + "}\n"
    return ret_str



def change_context_width(file_path, context_width):
    pattern = "FeatureElement1.ContextShiftSet"
    for line in fileinput.input(file_path, inplace=1):
        if pattern in line:
            new_line = pattern + " = "+build_new_context_width(context_width)
            line = line.replace(line, new_line)
        sys.stdout.write(line)



if __name__ == "__main__":
    file_path = sys.argv[1]
    context_width = int(sys.argv[2])

    change_context_width(file_path, context_width)