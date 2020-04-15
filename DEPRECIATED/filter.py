from scipy.stats import iqr
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator
import numpy as np
import matplotlib.font_manager as ftman
import sys

def reject_outliers(data):
    Phi_Original = data[0]
    Psi_Original = data[1]

    data_transformed = mirror_data(data)
    Phi_Copy = data_transformed[0]
    Psi_Copy = data_transformed[1]

    Phi_transformed = False
    Psi_transformed = False

    if np.ptp(Phi_Copy) < np.ptp(Phi_Original):
        Phi = Phi_Copy
        Phi_transformed = True
    else:
        Phi = Phi_Original

    if np.ptp(Psi_Copy) < np.ptp(Psi_Original):
        Psi = Psi_Copy
        Psi_transformed = True
    else:
        Psi = Psi_Original

    iqr_Phi = iqr(Phi)
    iqr_Psi = iqr(Psi)
    Q1_Phi = np.percentile(Phi, 25)
    Q3_Phi = np.percentile(Phi, 75)
    Q1_Psi = np.percentile(Psi, 25)
    Q3_Psi = np.percentile(Psi, 75)
    range_kept_Phi = [Q1_Phi - 1.5 * iqr_Phi, Q3_Phi + 1.5 * iqr_Phi]
    range_kept_Psi = [Q1_Psi - 1.5 * iqr_Psi, Q3_Psi + 1.5 * iqr_Psi]
    Phi_filter = np.all([Phi > range_kept_Phi[0], Phi < range_kept_Phi[1]], axis = 0)
    Psi_filter = np.all([Psi > range_kept_Psi[0], Psi < range_kept_Psi[1]], axis = 0)
    All_filter = np.all([Phi_filter, Psi_filter], axis = 0)
    data_filtered = np.array([Phi_Original[All_filter], Psi_Original[All_filter]])

    if Phi_transformed and range_kept_Phi[1] > 180:
        range_kept_Phi[1] = range_kept_Phi[1] - 360
    if Psi_transformed and range_kept_Psi[1] > 180:
        range_kept_Psi[1] = range_kept_Psi[1] - 360

    return data_filtered, range_kept_Phi, range_kept_Psi

def mirror_data(data):
    data_to_return = np.copy(data)
    for i in range(len(data)):
        for j in range(len(data[i])):
            if data_to_return[i][j] < 0:
                data_to_return[i][j] = data[i][j] + 360
    return data_to_return

Fig = plt.figure(figsize = (2,2), dpi = 300)
sample = np.loadtxt(sys.argv[1], usecols=range(2 * sys.argv[3], 2 * sys.argv[3] + 1), unpack=True, dtype=np.float32)
phi = sample[0]
psi = sample[1]
Bins = np.linspace(start=-180, stop=180, num=101)

hist2D, xedges, yedges = np.histogram2d(phi,psi,bins=Bins)
density2D = hist2D/np.sum(hist2D)

step = xedges[1] - xedges[0]
midps = xedges[1:] - 0.5*step

fig, ax = plt.subplots()
TickFP  = ftman.FontProperties(size=12)
MTickFP = ftman.FontProperties(size=0)
vfunc = np.vectorize(int)
XTicks = vfunc(np.linspace(-180, 180, 9))
YTicks = vfunc(np.linspace(-135, 180, 8))

levels = MaxNLocator(nbins=10).tick_values(hist2D.min(), density2D.max())
cf = ax.contourf(midps, midps, density2D.T, levels = levels, cmap = plt.get_cmap('Greys'))
fig.colorbar(cf, ax = ax)
ax.set_xlabel("$\phi$", fontsize=20)
ax.set_ylabel("$\psi$", fontsize=20)

ax.set_xticks(XTicks, minor=False)
ax.set_yticks(YTicks, minor=False)



a, range_Phi, range_Psi = reject_outliers(sample)

if range_Phi[0] < range_Phi[1]:
    hline_points = np.array([range_Phi[0], range_Phi[1]])
else:
    hline_points = np.array([range_Phi[0], 180, -180, range_Phi[1]])

if range_Psi[0] < range_Psi[1]:
    vline_points = np.array([range_Psi[0], range_Psi[1]])
else:
    vline_points = np.array([range_Psi[0], 180, -180, range_Psi[1]])

for index_h in range(0, len(hline_points)):
    for index_v in range(0, len(vline_points), 2):
        ax.vlines(hline_points[index_h], vline_points[index_v], vline_points[index_v + 1], colors = "r")

for index_v in range(0, len(vline_points)):
    for index_h in range(0, len(hline_points), 2):
        ax.hlines(vline_points[index_v], hline_points[index_h], hline_points[index_h + 1], colors = "r")

Fig.savefig(sys.argv[2])



