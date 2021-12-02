import sys
import matplotlib.pyplot as plt

def read_results(fpath):
    xpoints = set()

    with open(fpath, 'r') as f:
        res_dict = dict()
        for line in f:
            if line[:5] == "=====":
                config = line.split(" ")[:-1]
                acc_type = config[1] # Train, Validation or Test
                value = int(config[2][config[2].find('=')+1:])
                xpoints.add(value)
                if acc_type not in res_dict:
                    res_dict[acc_type] = []
            elif line[:5] == "WORD:":
                acc = line[line.find('Acc=')+len('Acc='):line.find('[')-1]
                res_dict[acc_type].append(float(acc))
            else:
                acc = line[line.find('Accuracy = ')+len('Accuracy = '):line.find('[')-2]
                res_dict[acc_type].append(float(acc))


    return res_dict, sorted(xpoints)


def plot_results(res_dict, xpoints, store_filepath, xaxis):
    plt.style.use('seaborn')

    fig, ax = plt.subplots(1, 2)
    fig.set_size_inches(16, 7)
    fig.set_dpi(120)

    ax[0].plot(xpoints, res_dict['Train'], '-o', label='Train')
    ax[0].plot(xpoints, res_dict['Validation'], '-o', label='Validation')
    ax[0].set_xlabel(xaxis)
    ax[0].set_ylabel("Accuracy")
    ax[0].legend()

    ax[1].plot(xpoints, res_dict['Test'], '-o', label='Test')
    ax[1].set_xlabel(xaxis)
    ax[1].set_ylabel("Accuracy")
    ax[1].legend()

    plt.savefig(store_filepath)



if __name__ == "__main__":
    fname_res = sys.argv[1]
    fname_plot = sys.argv[2]
    xaxis = " ".join(sys.argv[3:])

    res_dict, xpoints = read_results(fname_res)

    plot_results(res_dict, xpoints, fname_plot, xaxis)