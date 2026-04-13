Multiphase Flow model
=====


Multiphase transport equations
------------

The multiphase flow model uses an Euler-Euler approach (already available in ``multiphaseEulerFoam``).
Gas and liquid volume fractions are transported as 

 .. math::

   \frac{\partial (\alpha_j \rho_j)}{\partial t} + \nabla \cdot (\alpha_j \rho_j u_j) = \sum_{k\neq j} \dot{m}_{kj},
  
where :math:`j` is the phase index (gas or liquid), :math:`\alpha_j` is the volume fraction of the phase :math:`j`, :math:`\rho_j` is the density of phase :math:`j`, :math:`u_j` is the velocity vector of phase :math:`j`. The right-hand side of this equation includes the sum of interphase mass transfer terms where :math:`\dot{m}_{kj}` is the mass transfer rate from phase :math:`k` to phase :math:`j`. To model the relative motion of each phase, a phase-momentum transport equation is solved, which takes the form

 .. math::

   \frac{\partial (\alpha_j \rho_j u_j)}{\partial t} + \nabla \cdot (\alpha_j \rho_j u_j u_j) = \nabla \cdot (\alpha_j \overline{\tau}) - \alpha_j \nabla p + \alpha_j \rho_j g +\sum_{k\neq j} D_{kj} + M^{m}_j + F_j,

where :math:`\overline{\tau}` is the stress tensor which includes Reynolds stress and viscous (molecular and turbulent) stress (including turbulent viscosity) for the phase :math:`j`; :math:`D_{kj}` is the drag force exerted by phase :math:`k` on phase :math:`j` that depends on the drag coefficient associated with the dispersed phase and associated volume fraction, and :math:`F_j` contains interfacial forces acting on phase :math:`j` which includes lift, wall-lubrication, virtual-mass and turbulent-dispersion forces. :math:`M^{m}_j` accounts for the added momentum and is defined as :math:`M^{m}_j = \dot{m}_{j,in} u_k - \dot{m}_{j,out} u_j` where :math:`\dot{m}` is the mass transfer rate from/to phase :math:`j`, :math:`u_j` is the velocity of phase :math:`j` and :math:`u_k` is the velocity of phase :math:`k`.

If needed, an energy equation is solved to account for differences in phase temperatures.
    
 .. math::
   \frac{\partial \rho_j \alpha_j E_j}{\partial t} + \nabla \cdot (\rho_j \alpha_j u_j E_j) = \nabla \cdot (\alpha_j \kappa_{j} \nabla T_j) + \dot{Q}

where :math:`E_j` is the sensible energy of the phase :math:`j`, :math:`T_j` is the temperature of the phase :math:`j`, :math:`\kappa_{j}` is the effective thermal diffusivity of the phase :math:`j` (including molecular and turbulent contributions) and :math:`\dot{Q}` is the heat exchange due to differences in temperature. Heat exchange through the interface is driven by temperature differences between phases. The last right-hand side term can be written as :math:`\dot{Q} = h_{jl}(T_f - T_j)`, where :math:`h_{jl}` is the heat transfer coefficient of species :math:`l` in phase :math:`j`, :math:`T_j` is the temperature of phase :math:`j` and :math:`T_f` is the temperature at the interface. The temperature at the interface is computed based on the assumption that the rate of heat transfer must be equal to the latent heat :math:`\lambda_j` at the interface between phases :math:`j` and :math:`k` where :math:`h_{jl}(T_j - T_f) + h_{kl}(T_k - T_f) = \dot{m}_{j,in} \lambda_j`

Using the momentum and phase fraction, species mass fractions are transported as

 .. math::
    \frac{\partial (\rho_j \alpha_j Y_{jl})}{\partial t} + \nabla \cdot (\rho_j \alpha_j Y_{jl} u_j) = \nabla \cdot (\rho_j \alpha_j D_{jl} \nabla Y_{jl}) + S_{jl},

where :math:`Y_{jl}` is the :math:`l^{th}` species mass fraction in phase :math:`j`, :math:`D_{jl}` is the diffusivity of the :math:`l^{th}` species in phase :math:`j` and :math:`S_{jl}` are source terms due to interphase mass transfer.

If desired, a population balance equation can be solved to model the distribution of bubble size. The fundamental governing equation of the NDF is

 .. math::
    \frac{\partial n_v}{\partial t} + \nabla \cdot (u n_v) = h_v,

where $:math:`u` is the phase velocity, :math:`t` is time, :math:`n_v` is the number density of bubbles of size :math:`v` and the source term is :math:`h_v =  B_{\rm b} - B_{\rm d} +  C_{\rm b} -  C_{\rm d} - D + \dot{N_v}`, where :math:`B_{\rm b}` (resp. :math:`C_{\rm b}`) is the bubble birth contribution from bubble breakup (resp. coalescence), :math:`B_{\rm d}` (resp. :math:`C_{\rm d}`) is the bubble death contribution from bubble breakup (resp. coalescence), :math:`D` is the drift term that is due to changes of bubble volume arising from pressure or mass transfer induced density changes, and :math:`\dot{N_v}` is the bubble nucleation source term. The full expression of :math:`h_v` is available in [Lehnigk2021]_ and the effect of coalescence and breakup rates on the prediction of BiRD has been studied in [Hassanaly2025]_.


.. _Henry:

Multiphase flow closure models
------------

Though all closure models can be swapped by any other one available in OpenFOAM, we often use the same set of closure models. Usually, and throughout the tutorial, the user will find that the interphase drag force is obtained by using the Grace model [Grace1976]_ and transverse lift from the model by using the Tomiyama model [Tomiyama2002]_. Wall lubrication forces are computed using the model by Antal et al. [Antal1991]_ and turbulent dispersion uses the model of Burns et al. [Burns2004]_. Interphase mass transfer of species is modeled by using the mass transfer coefficient obtained from Higbie correlation [Higbie1935]_. The interphase mass transfer of a species also depends on the local saturation concentration obtained from Henry's constant and the local gas phase concentration of the species. 

Henry's constant
------------
The Henry's constant is a critical parameter that controls the mass transfer rates. The Henry's constant is a temperature dependent variable that is usually expressed in :math:`mol/(kg.bar)`, see for example `the NIST database <https://webbook.nist.gov/cgi/cbook.cgi?ID=C7782447&Mask=10>`_.


References
==========

.. [Lehnigk2021] Lehnigk, R. et al. (2021). "An open-source population balance modeling framework for the simulation of polydisperse multiphase flows". AIChE Journal.
.. [Hassanaly2025] Hassanaly, M. et al. (2025). "Bayesian calibration of bubble size dynamics applied to CO2 gas fermenters". Chemical Engineering Research and Design.
.. [Grace1976] Grace, J. R. (1976). "Shapes and Velocities of Single Drops and Bubbles Moving Freely through Immisicible Liquids". Transactions of the American Institute of Chemical Engineers.
.. [Tomiyama2002] Tomiyama, A. et al. (2002). "Transverse migration of single bubbles in simple shear flows". Chemical Engineering Science.
.. [Antal1991] Antal, S. P. et al. (1991). "Analysis of phase distribution in fully developed laminar bubbly two-phase flow". International Journal of Multiphase Flow.
.. [Burns2004] Burns, A. D et al. (2004). "The Favre averaged drag model for turbulent dispersion in Eulerian multi-phase flows". 5th International Conference on Multiphase Flow, ICMF.
.. [Higbie1935] Higbie, R. (1935). "The rate of absorption of pure gas into a still liquid during short periods of exposure". Transactions of the American Institute of Chemical Engineers.






