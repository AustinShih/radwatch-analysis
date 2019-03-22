import becquerel as bq
from becquerel import Spectrum
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
import math as m

class PF(object):
    def _

    def f_near(energy_array,energy): #finds index of closest energy in spectrum to
    #that of the characteristic energy
        idx = np.abs(energy_array - energy).argmin()
        return idx
    def calibration(integrals): #calculate efficiencies
        efficiencies = []
        for x in range(0,len(source_activities)):
            iso = bq.tools.Isotope(source_isotopes[x])
            efficiency = integrals[x]/(source_activities[x]*branching_ratio[x])
            efficiencies = np.append(efficiencies,efficiency)
        return efficiencies
    def Efficiency(source_isotopes,source_energies,source_activities,spectrum,background,branching_ratio):
    #input: array of isotopes, energies, and activities, spectrum file name, background
    #spectrum file name, branching ratio
        spec = Spectrum.from_file(spectrum) #import spectrum data
        spec_counts = spec.counts_vals #spectrum counts
        bg = Spectrum.from_file(background) #import spectrum data
        bg_counts = bg.counts_vals #background counts
        sub_spec = spec - bg #background subtraction
        spec_energies = sub_spec.energies_kev #all energues
        spec_counts = spec_counts-bg_counts #all counts
        #peak fitting and area under curve
        integrals = []
        for n in source_energies:
            fit = bq.core.fitting.FitterGaussErfLine(x=sub_spec.channels, y=sub_spec.cps_vals, y_unc=sub_spec.cps_uncs)
            idx = f_near(spec_energies,n)
            fit.set_roi(idx-100,idx+100)
            fit.fit()
            amp = fit.result.params['gauss_amp'].value
            mu = fit.result.params['gauss_mu'].value
            sigma =fit.result.params['gauss_sigma'].value
            def gaussian(x):
                return (spec.livetime * amp /(m.sqrt(2*m.pi)*sigma)) * m.exp(- ((x-mu)**2) / (2*sigma**2))
            integral = integrate.quad(gaussian, idx-100, idx+100)
            integrals = np.append(integrals,integral[0])
        #calculate efficiency
        efficiencies = calibration(integrals)
        return efficiencies
