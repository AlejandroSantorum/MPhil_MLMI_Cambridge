import sys
import matplotlib.pyplot as plt





if __name__ == '__main__':
    fname_res = sys.argv[1]
    fname_plot = sys.argv[2]
    xaxis = " ".join(sys.argv[3:])

    res_dict, xpoints = read_results(fname_res)

    plot_results(res_dict, xpoints, fname_plot, xaxis)
