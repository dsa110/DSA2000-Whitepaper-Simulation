# DSA2000-Whitepaper-Simulation
The simulation consists of two steps, setting up the measurement set (basically computing the uvws), and then inverting a model.

## Requirements
* CASA6 Python libraries (https://casa.nrao.edu/casadocs/casa-5.6.0/introduction/casa6-installation-and-usage)
* Sky model as FITS image (https://astronomers.skatelescope.org/ska-science-data-challenge-1/)
* wsclean (for inversion; https://sourceforge.net/projects/wsclean/)

## Simulating visibilities
For the first step I used casa for that (see `simobs.py`) and download an image from the SKA data challenge (https://astronomers.skatelescope.org/ska-science-data-challenge-1/). Also see http://library.nrao.edu/public/memos/ngvla/NGVLA_55.pdf. The cfg file used is the uvw coordinates of the array on the tangent plane set in `simobs.py` (this turned out to be the easiest way for me to get things working without a deep understanding of how UTM works in CASA).

```
./simobs.py <image.fits>
```

## Inverting model
For the second step I used wsclean which handles wide-field effects and is numerically more stable. I did have to make sure that the model fits file have unit Jy/px (e.g. https://casaguides.nrao.edu/index.php/Simulation_Recipes#Flux_Density_Scaling), and then changed the fits header so that the sources are above horizon.

To predict I did something like
```
wsclean -predict -size 1001 1001 -weight natural -scale 0.604asec -name SKAMid_B1_100h_v3_scaled_cropped_fun DSA_2000_ant_60x15s_mma_SKAMid.ms
```
where the model image has to have the name SKAMid_B1_100h_v3_scaled_cropped_fun.fits. 

To image
```
wsclean -no-update-model-required -niter 0 -size 1200 1200 -scale 0.5asec -weight briggs 0 -datacolumn MODEL_DATA -make-psf -name SKAMid_60x15s_bright DSA_2000_ant_60x15s_mma_SKAMid.ms
```
One can skip the -make-psf option if they don't need the PSF.

TODO: Running subbands in parallel would make things faster.
