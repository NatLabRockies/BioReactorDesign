Tutorial for unstructured grids of tetrahedrons with MRF
--------------------------------------------------------
Features demonstrated:
* Sparging oxygen in water at 1VVM
* Mass transfer
* MRF region rotating at 100 RPM
* High Courant number schemes
* Pupulation balance model

Used for:
* Steady state calculation in complex geometries

The base case should run with $\Delta t \approx 1e^{-3}$ s.
__Uses OpenFOAM-13. Coarse mesh.__

__Example results__
Volume colors are gas volume fraction and surface color are gas velocity.

![Gas volume fraction](/tutorials_13/STR_tetra/alphag.png)
  
