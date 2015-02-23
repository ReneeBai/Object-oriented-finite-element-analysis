import subprocess, os.path
import numpy as np

quakes = ['quake1', 'quake2']

# Run the analyses, in parallel
procs = []
for q in quakes:
    datafile = q+'.dat'
    infilename = q+'_input.txt'
    infile = open(infilename, 'w')
    infile.write('[Beam]\n')
    infile.write('length=10.0\n')
    infile.write('E=210e9\n')
    infile.write('I=2.7009842839238267e-05\n')
    infile.write('rho=7800.\n')
    infile.write('A=0.005969026041820614\n')
    infile.write('dampingRatio=0.04\n')
    infile.write('\n[Analysis]\n')
    infile.write('numModes=5\n')    # Determined manually
    infile.write('numStations=51\n')
    infile.write('\n[GroundMotion]\n')
    infile.write('groundMotionFile='+q+'.dat\n')
    infile.write('\n[Output]\n')
    infile.write('outputDir='+q+'\n')
    infile.close()

    procs.append(subprocess.Popen(['python', 'beam505.py', infilename]))

for p in procs:
    p.wait()

loadnames = [('accel', 'ACCELERATION'),
             ('moment', 'MOMENT'),
             ('shear', 'SHEAR')]
for loadtype, loadfullname in loadnames:
    loadmax = []
    loadmin = []
    for q in quakes:
        loaddata = np.loadtxt(os.path.join(q, loadtype+'.txt'), skiprows=4)
        loadstation = loaddata[:,0]
        loadmax.append(loaddata[:,1])
        loadmin.append(loaddata[:,2])
    loadmax = np.array(loadmax).T
    loadmin = np.array(loadmin).T
    maxid = np.argmax(loadmax, axis=1)
    minid = np.argmin(loadmin, axis=1)
    env_filename = loadtype+'_envelope.txt'
    env_file = open(env_filename, 'w')
    env_file.write(loadfullname+' COMPOSITE ENVELOPE\n')
    env_file.write('\n')
    env_file.write('POSITION    MAXIMUM    CASE     MINIMUM    CASE\n')
    env_file.write('--------  ----------  ------  ----------  ------\n')
    for i, pos in enumerate(loadstation):
        env_file.write('%8.2f  %10.3e  %6s  %10.3e  %6s\n'
                       %(pos, loadmax[i,maxid[i]], quakes[maxid[i]],
                              loadmin[i,minid[i]], quakes[minid[i]]))
    env_file.close()
