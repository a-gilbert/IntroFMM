"""A plot showing two different bodies and the vectors between them
for a given origin."""
import matplotlib.pyplot as plt


def make_2body_plot():
    plt.close('all')
    fig = plt.figure(figsize=(8,8))
    ax = fig.add_subplot(111)
    #origin
    ax.plot([-1], [-1], color='k', marker='o', markersize=12)
    plt.text(-1.00, -1.15, r"$O$", fontsize=12)
    #r'
    ax.arrow(-1, -1, -0.5, 0.5, head_width=0.05, head_length=0.1, fc='k', ec='k')
    plt.text(-1.5, -.75, r"$\mathbf{r}'$", fontsize=12)
    ax.plot([-1.5 - 0.09], [-0.4], marker='o', markersize=12)
    #r
    ax.arrow(-1, -1, 2, 1, head_width=0.05, head_length=0.1, fc='k', ec='k')
    plt.text(0.75, -.25, r"$\mathbf{r}$", fontsize=12)
    ax.plot([1.12], [0.06], marker='o', markersize=12)
    #r-r'
    ax.arrow(-1.5-0.09, -0.4, abs(-1.5-1.12), abs(-0.4-0.06), head_width=0.05, head_length=0.1, fc='k', ec='k')
    plt.text(-0.5, -0.1, r"$\mathbf{r}-\mathbf{r}'$", fontsize=12)
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_axis_off()
    plt.show()