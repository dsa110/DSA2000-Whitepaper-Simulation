# DSA2000-Whitepaper-Simulation
The simulation consists of two steps, setting up the measurement set (basically computing the uvws), and then inverting a model. For the first step I used casa for that (see `simobs.py`). Also see http://library.nrao.edu/public/memos/ngvla/NGVLA_55.pdf

For the second step I used wsclean which handles wide-field effects and is numerically more stable (see `wsclean-predict.sh`). I did have to make sure that the model fits file have unit Jy/px (e.g. https://casaguides.nrao.edu/index.php/Simulation_Recipes#Flux_Density_Scaling), and then changed the fits header so that the sources are above horizon.

TODO: Running subbands in parallel would make things faster.
