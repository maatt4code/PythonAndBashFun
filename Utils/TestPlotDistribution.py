import numpy as np
from scipy.stats import skewnorm
import scipy.stats as st
import matplotlib.pyplot as plt

def plot_skewed_data(data):
    # generate histogram using data
    num_bins = 200
    bins = np.linspace(min(data), max(data), num_bins)
    _, bins = np.histogram(data, bins=bins, density=True)
    bin_centers = 0.5 * (bins[1:] + bins[:-1])

    # get PDF from data by fitting it to skewnorm
    a, loc, scale = skewnorm.fit(data)
    pdf = st.skewnorm.pdf(bin_centers, a, loc, scale)

    # plot
    kwargs = dict(normed=True, edgecolor='black', linewidth=1.2, alpha=0.5, bins=20, stacked=True)
    # kwargs = dict(alpha=0.5, bins=20, normed=True, histtype='stepfilled', stacked=False, edgecolor='black', linewidth=1.2)
    fig, ax = plt.subplots(1, 1)
    ax.plot(bin_centers, pdf, 'r-', lw=5, alpha=0.6, label='skewnorm pdf')
    # ax.plot(bin_centers, histogram, )
    # Newer version of matplotlib uses density rather than normed
    ax.hist(data, **kwargs, color='g', label="Histogram of samples (normalized)")
    ax.axvline(x=np.percentile(data, 1), color='red', ls=':', lw=2, label='1 pc')
    ax.axvline(x=np.percentile(data, 50), color='red', ls=':', lw=2, label='mean')
    ax.axvline(x=np.percentile(data, 99), color='red', ls=':', lw=2, label='99 pc')
    print("%f :: %f" % (skewnorm.ppf(0.01, a), skewnorm.ppf(0.99, a)))
    ax.legend(loc='best', frameon=True)
    plt.show()


# Generate skewed data - a == 0 means normal
ka = 4
data = skewnorm.rvs(ka, size=1000)
plot_skewed_data(data)
