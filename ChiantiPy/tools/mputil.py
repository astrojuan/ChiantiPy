'''
Functions needed for standard Python multiprocessing module mspectrum
'''

import ChiantiPy.core as ch

def doFfQ(inQ, outQ):
    '''
    Multiprocessing helper for `ChiantiPy.core.continuum.freeFree`

    Parameters
    -----------
    inQ : `~multiprocessing.Queue`
        Ion free-free emission jobs queued up by multiprocessing module
    outQ : `~multiprocessing.Queue`
        Finished free-free emission jobs
    '''
    for inputs in iter(inQ.get, 'STOP'):
        ionS = inputs[0]
        temperature = inputs[1]
        wavelength = inputs[2]
        abund = inputs[3]
        em = inputs[4]
        ff = ch.continuum(ionS, temperature, abundance=abund, em=em)
        ff.freeFree(wavelength)
        outQ.put(ff.FreeFree)
    return
    #
    # ----------------------------------------------
    #
def doFbQ(inQ, outQ):
    '''
    Multiprocessing helper for `ChiantiPy.core.continuum.freeBound`

    Parameters
    -----------
    inQ : `~multiprocessing.Queue`
        Ion free-bound emission jobs queued up by multiprocessing module
    outQ : `~multiprocessing.Queue`
        Finished free-bound emission jobs
    '''
    for inputs in iter(inQ.get, 'STOP'):
        ionS = inputs[0]
        temperature = inputs[1]
        wavelength = inputs[2]
        abund = inputs[3]
        em = inputs[4]
        fb = ch.continuum(ionS, temperature, abundance=abund, em=em)
        fb.freeBound(wavelength)
        outQ.put(fb.FreeBound)
    return
    #
    # ----------------------------------------------
    #
def doIonQ(inQueue, outQueue):
    '''
    Multiprocessing helper for `ChiantiPy.core.ion` and `ChiantiPy.core.ion.twoPhoton`

    Parameters
    -----------
    inQueue : `~multiprocessing.Queue`
        Jobs queued up by multiprocessing module
    outQueue : `~multiprocessing.Queue`
        Finished jobs
    '''
    for inpts in iter(inQueue.get, 'STOP'):
        ionS = inpts[0]
        temperature = inpts[1]
        density = inpts[2]
        wavelength = inpts[3]
        wvlRange = [wavelength.min(), wavelength.max()]
        filter = inpts[4]
        allLines = inpts[5]
        abund = inpts[6]
        em = inpts[7]
        doContinuum = inpts[8]
        thisIon = ch.ion(ionS, temperature, density, abundance=abund)
        thisIon.intensity(wvlRange = wvlRange, allLines = allLines, em=em)
        if 'errorMessage' not in sorted(thisIon.Intensity.keys()):
            thisIon.spectrum(wavelength,  filter=filter)
        outList = [ionS, thisIon]
        if not thisIon.Dielectronic and doContinuum:
            if (thisIon.Z - thisIon.Ion) in [0, 1]:
                thisIon.twoPhoton(wavelength)
                outList.append(thisIon.TwoPhoton)
        outQueue.put(outList)
    return
