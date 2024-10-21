#!/usr/bin/env python3
import argparse
import numpy as np

import openmc


def _parse_args():
    """Parse and return commandline arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--batches", type=int, default=100,
                        help='Number of batches to simulate (int)')
    parser.add_argument("-p", "--particles", type=int, default=int(1e7),
                        help='Number of particles per batch (int)')
    parser.add_argument("-s", "--threads", type=int,
                        help='Number of threads to use in the simulation (int)')

    args = parser.parse_args()

    return args

def main():
    """Analysis of Osaka Sphere Benchmark Experiment (OKTAVIAN) -Tungsten experiment"""
    
    # Parse commandline arguments
    args = _parse_args()

    # Instantiate Model object
    model = openmc.Model()

    ############################################################################
    # Define Materials

    # 
    mat_1 = openmc.Material(material_id=1)
    mat_1.set_density('g/cm3', 2.77813)
    mat_1.add_nuclide('Zr90', 0.5145, 'ao')
    mat_1.add_nuclide('Zr91', 0.1122, 'ao')
    mat_1.add_nuclide('Zr92', 0.1715, 'ao')
    mat_1.add_nuclide('Zr94', 0.1738, 'ao')
    mat_1.add_nuclide('Zr96', 0.028, 'ao')
    # 
    mat_2 = openmc.Material(material_id=2)
    mat_2.set_density('g/cm3', 7.824)
    mat_2.add_nuclide('Cr50', 0.00803825, 'wo')
    mat_2.add_nuclide('Cr52', 0.15501, 'wo')
    mat_2.add_nuclide('Cr53', 0.0175768, 'wo')
    mat_2.add_nuclide('Cr54', 0.00437525, 'wo')
    mat_2.add_nuclide('Fe54', 0.0411488, 'wo')
    mat_2.add_nuclide('Fe56', 0.645948, 'wo')
    mat_2.add_nuclide('Fe57', 0.0149178, 'wo')
    mat_2.add_nuclide('Fe58', 0.00198528, 'wo')
    mat_2.add_nuclide('Ni58', 0.0755655, 'wo')
    mat_2.add_nuclide('Ni60', 0.0291075, 'wo')
    mat_2.add_nuclide('Ni61', 0.0012654, 'wo')
    mat_2.add_nuclide('Ni62', 0.00403374, 'wo')
    mat_2.add_nuclide('Ni64', 0.00102786, 'wo')

    # create materials instance
    materials = openmc.Materials([mat_1, mat_2])

    # %%

    ############################################################################
    # Define Geometry

    # surfaces
    surf_8 = openmc.XPlane(surface_id=8, x0=-2.2)
    surf_1 = openmc.XCylinder(surface_id=1, y0=0.0, z0=0.0, r=2.55)
    surf_6 = openmc.Sphere(surface_id=6, x0=0.0, y0=0.0, z0=0.0, r=30.5)
    surf_9 = openmc.XPlane(surface_id=9, x0=-2.5)
    surf_2 = openmc.XCylinder(surface_id=2, y0=0.0, z0=0.0, r=2.85)
    surf_5 = openmc.Sphere(surface_id=5, x0=0.0, y0=0.0, z0=0.0, r=30.0)
    surf_7 = openmc.Sphere(surface_id=7, x0=0.0, y0=0.0, z0=0.0, r=100.0, boundary_type='vacuum')

    # regions
    region_1 = (+surf_8 & -surf_1 & -surf_6)
    region_2 = ((-surf_8 & +surf_9 & -surf_2) | (+surf_8 & +surf_1 & -surf_2 & -surf_5))
    region_3 = ((-surf_5 & -surf_9) | (+surf_9 & +surf_2 & -surf_5))
    region_4 = ((+surf_5 & -surf_6 & -surf_8) | (+surf_8 & +surf_1 & +surf_5 & -surf_6))
    region_5 = (+surf_6 & -surf_7)

    # cells
    cell_1 = openmc.Cell(cell_id=1, region=region_1, fill=None)
    cell_2 = openmc.Cell(cell_id=2, region=region_2, fill=mat_2)
    cell_3 = openmc.Cell(cell_id=3, region=region_3, fill=mat_1)
    cell_4 = openmc.Cell(cell_id=4, region=region_4, fill=mat_2)
    cell_5 = openmc.Cell(cell_id=5, region=region_5, fill=None)

    # create root universe
    universe = openmc.Universe(cells=[cell_1, cell_2, cell_3, cell_4, cell_5])

    # create geometry instance
    model.geometry = openmc.Geometry(universe)

    ############################################################################
    # Define Settings

    # source definition
    # oktavian source
    # Create a point source    
    energies = np.array([
        0.04000, 0.05547, 0.06131, 0.06776, 0.07488, 0.08276, 0.09146, 0.10108,
        0.11171, 0.12346, 0.13644, 0.15079, 0.16665, 0.18418, 0.20355, 0.22496,
        0.24862, 0.27476, 0.30366, 0.33560, 0.37089, 0.40990, 0.45301, 0.50065,
        0.55331, 0.61150, 0.67581, 0.74689, 0.82544, 0.91225, 1.00820, 1.11420,
        1.23140, 1.36090, 1.50400, 1.66220, 1.83700, 2.03020, 2.24380, 2.47970,
        2.74050, 3.02880, 3.34730, 3.69930, 4.08840, 4.51840, 4.99360, 5.51880,
        6.09920, 6.74060, 7.44960, 8.23300, 9.09890, 10.05600, 11.11300, 12.28200,
        13.57400, 15.00200, 16.57900, 18.32300, 20.25000
    ])

    weights= np.array([
        2.34698e-05, 0.000415683, 4.35812e-05, 0.000445402, 0.000228589,
        0.000168707, 8.63297e-06, 0.000278683, 0.000131914, 0.000328094, 
        4.01013e-05, 0.00039153, 3.01854e-05, 0.000299594, 0.00045695, 
        0.000365011, 0.000350803, 0.000574161, 0.000580666, 0.000589515, 
        0.000794161, 0.000784508, 0.000969033, 0.00101611, 0.00126596, 
        0.00144396, 0.0017001, 0.00180698, 0.00202595, 0.00214917, 
        0.00224533, 0.00255639, 0.00262286, 0.00252654, 0.00275538,
        0.00259479, 0.00266401, 0.00263196, 0.0026901, 0.0034111, 
        0.00486127, 0.0024327, 0.00255973, 0.00231423, 0.0022431, 
        0.00217998, 0.00198407, 0.00195394, 0.00184984, 0.00183921, 
        0.00195181, 0.00212306, 0.00271143, 0.00339517, 0.0057611, 
        0.0318268, 0.521042, 0.304658, 0.00073995, 0.000356743, 
        0.0
    ])

    source = openmc.IndependentSource()
    source.space = openmc.stats.Point((0, 0, 0))
    source.angle = openmc.stats.Isotropic()
    source.particle = 'neutron' 
    source.energy = openmc.stats.Tabular(energies, weights, interpolation='histogram')
    
    # Indicate how many particles to run
    settings = openmc.Settings(run_mode='fixed source')
    settings.photon_transport = True
    settings.source = source
    settings.batches = args.batches
    settings.particles = args.particles
    settings.output = {'tallies': False}

    model.settings = settings

    ############################################################################
    # Specify Tallies
    # setup the filters for the cell tally
    vessel_surface_filter = openmc.SurfaceFilter(surf_6) # outer radius of outer steel vessel
    neutron_particle_filter = openmc.ParticleFilter(['neutron'])
    
    neutron_energies = np.array([
        4.72740E-02, 4.92000E-02, 5.12100E-02, 5.33000E-02, 5.54800E-02, 5.77400E-02, 
        6.01000E-02, 6.25500E-02, 6.51000E-02, 6.77600E-02, 7.05300E-02, 7.34000E-02, 
        7.64000E-02, 7.95200E-02, 8.27600E-02, 8.61400E-02, 8.96500E-02, 9.33100E-02, 
        9.71200E-02, 1.01090E-01, 1.05210E-01, 1.09500E-01, 1.13970E-01, 1.18620E-01, 
        1.23470E-01, 1.28500E-01, 1.33750E-01, 1.39210E-01, 1.44890E-01, 1.50800E-01, 
        1.56960E-01, 1.63360E-01, 1.70030E-01, 1.76970E-01, 1.84190E-01, 1.91710E-01, 
        1.99530E-01, 2.07670E-01, 2.16150E-01, 2.24970E-01, 2.34150E-01, 2.43710E-01, 
        2.53650E-01, 2.64000E-01, 2.74780E-01, 2.85990E-01, 2.97660E-01, 3.09810E-01, 
        3.22450E-01, 3.35610E-01, 3.49310E-01, 3.63570E-01, 3.78400E-01, 3.93850E-01, 
        4.09920E-01, 4.26650E-01, 4.44060E-01, 4.62180E-01, 4.81050E-01, 5.00680E-01, 
        5.21110E-01, 5.42380E-01, 5.64510E-01, 5.87550E-01, 6.11530E-01, 6.36480E-01, 
        6.62460E-01, 6.89500E-01, 7.17630E-01, 7.46920E-01, 7.77400E-01, 8.09130E-01, 
        8.42150E-01, 8.76520E-01, 9.12290E-01, 9.49520E-01, 9.88270E-01, 1.02860E+00, 
        1.07060E+00, 1.11430E+00, 1.15980E+00, 1.20710E+00, 1.25630E+00, 1.30760E+00, 
        1.36100E+00, 1.41650E+00, 1.47430E+00, 1.53450E+00, 1.59710E+00, 1.66230E+00, 
        1.73010E+00, 1.80080E+00, 1.87420E+00, 1.95070E+00, 2.03030E+00, 2.11320E+00, 
        2.19940E+00, 2.28920E+00, 2.38260E+00, 2.47990E+00, 2.58110E+00, 2.68640E+00, 
        2.79600E+00, 2.91010E+00, 3.02890E+00, 3.15250E+00, 3.28120E+00, 3.41510E+00, 
        3.55450E+00, 3.69950E+00, 3.85050E+00, 4.00760E+00, 4.17120E+00, 4.34140E+00, 
        4.51860E+00, 4.70300E+00, 4.89490E+00, 5.09470E+00, 5.30260E+00, 5.51900E+00, 
        5.74430E+00, 5.97870E+00, 6.22270E+00, 6.47660E+00, 6.74100E+00, 7.01610E+00, 
        7.30240E+00, 7.60040E+00, 7.91060E+00, 8.23340E+00, 8.56940E+00, 8.91920E+00, 
        9.28320E+00, 9.66200E+00, 1.00560E+01, 1.04670E+01, 1.08940E+01, 1.13390E+01, 
        1.18010E+01, 1.22830E+01, 1.27840E+01, 1.33060E+01, 1.38490E+01, 1.44140E+01, 
        1.50020E+01, 1.56150E+01, 1.62520E+01, 1.69150E+01, 1.76050E+01, 1.83240E+01, 
        1.90720E+01, 1.98500E+01, 2.06600E+01
    ])*1e6

    energy_neutron_filter = openmc.EnergyFilter(neutron_energies)

    #creates an empty tally object
    model.tallies = openmc.Tallies()

    # create the tally
    neutron_surface_spectra_tally = openmc.Tally(name='nspectrum')
    neutron_surface_spectra_tally.scores = ['current']
    neutron_surface_spectra_tally.filters = [vessel_surface_filter, neutron_particle_filter, energy_neutron_filter]
    model.tallies.append(neutron_surface_spectra_tally)

    # define the folder names for storing the statepoints
    cwd = 'results'
    model.settings = settings
    
    return model.run(cwd=cwd, threads=args.threads)


if __name__ == "__main__":
    main()