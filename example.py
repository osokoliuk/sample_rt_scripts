import Snapshot.snapshot as snapshot

# Choose a redshift and snapshot number from the following lists
# zs = np.array([7.0, 6.9, 6.6, 6.3, 6.0, 5.75595334609, 5.7, 5.57876558674, 5.3, 5.1, 4.8, 4.48623755365,
#                 4.2, 4.0, 3.7, 3.6, 3.4, 3.2, 3.1, 2.8, 2.6, 2.4, 2.2, 2.0])
# nrs = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,
#                 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24])
z = 2.4
nr = 22

# Settings for the self-shielding; ssS is the custom Sherwood simulation with an on-the-fly self-shielding prescription
Sherwood = "ssS"
self_shield = False
units = "SB"

# Narrowband width in m
# dlambda = 8.75e-10 # m, mean MUSE (pseudo-)narrowband in Wisotzki et al. (2016)
dlambda = 3.75e-10

num_threads = 512

print('\n')

# Simulation parameters
size = "40"
res = "1024"
phys = ""

# Include mirror limit for recombination emission? (See Witstok et al. 2021 for details)
# rec_mirror = ''
rec_mirror = "HM12"
# rec_mirror = "P19"

# dens_cut = None
# dens_cut = -100
# dens_cut = -200
dens_cut = "-0.5_" + rec_mirror

# Set narrowband centre and zoom position
nb0 = 21.0
dzoom = 4 # half of the size of the zoom
zoomcx = 11 # centre x coord. of the zoom
zoomcy = 13 # centre y coord. of the zoom
zoom = [zoomcx-dzoom, zoomcx+dzoom, zoomcy-dzoom, zoomcy+dzoom]

# Image and colormap settings
grid_size = 300 # number of pixels
vmin, vmax = -24, -18 # SB limits
cmap = "inferno" # colormap

# Begin loading
check_ifcalc = True
force_calc = False

snap = snapshot.intmap(size, res, phys, nr, Sherwood=Sherwood, self_shield=self_shield, units=units)
boxsize = snap.boxsize
key = snap.key

z_nr = snap.z

snap.set_zoom(zoom)
nb = snap.set_nb(dlambda, nb0=nb0)

if check_ifcalc:
    calc = not snap.check_if_exists_int(pic_name="your_saved_intmap_name")
    if calc:
        print("File your_saved_intmap_name.npz not found - loading...")
else:
    calc = False

if force_calc or calc:
    # Calculate column density and intensity maps with specified number of cores, density cut and mirror limit prescription
    col, pic = snap.calc_int(grid_size=grid_size, num_threads=num_threads, dens_cut=dens_cut, rec_mirror=rec_mirror, col_dens=True)
    snap.save_int(pic_name="your_saved_intmap_name", col_name="your_saved_colmap_name")
else:
    col, pic = snap.load_int(pic_name="your_saved_intmap_name", col_name="your_saved_colmap_name")
