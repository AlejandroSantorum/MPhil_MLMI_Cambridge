import matplotlib.pyplot as plt

def read_results(fpath):
    xpoints = set()

    with open(fpath, 'r') as f:
        res_dict = dict()
        for line in f:
            if line[:5] == "=====":
                config = line.split(" ")[:-1]
                mono_type = config[1] # e.g. FBK_Z_Init
                n_gaussians = int(config[2][config[2].find('=')+1:])
                xpoints.add(n_gaussians)
                if mono_type not in res_dict:
                    res_dict[mono_type] = []
            elif line[:5] == "WORD:":
                acc = line[line.find('Acc=')+len('Acc='):line.find('[')-1]
                res_dict[mono_type].append(float(acc))
    
    return res_dict, sorted(xpoints)


def plot_results(res_dict, xpoints, store_filepath):
    plt.style.use('seaborn')

    for mono_type in res_dict:
        plt.plot(xpoints, res_dict[mono_type], '-o', label=mono_type)
    
    plt.legend()
    plt.xlabel("Number of Gaussians")
    plt.ylabel("Accuracy")
    plt.savefig(store_filepath)



if __name__ == '__main__':
    FILEPATH = "./results/monophone_results.txt"
    res_dict, xpoints = read_results(FILEPATH)

    STORE_FILEPATH = "./imgs/monophone_results.png"
    plot_results(res_dict, xpoints, STORE_FILEPATH)


