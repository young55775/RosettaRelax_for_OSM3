# import py3Dmol
from pyrosetta import *
init()
from pyrosetta.toolbox import mutate_residue
from pyrosetta.teaching import *
from pyrosetta.rosetta.protocols.relax import ClassicRelax
from pyrosetta.rosetta.protocols.relax import FastRelax
import pyrosetta.distributed
import pyrosetta.distributed.io as io
import argparse
# import pyrosetta.distributed.viewer as viewer

def main(mode,file,position,residue,out):
    # pmm = PyMOLMover()
    if mode == 'Classic':
        relax = ClassicRelax()
    else:
        relax = FastRelax()
    model = pose_from_pdb(file)
    test = Pose()
    test.assign(model)
    position = position.split('m')
    residue = residue.split('m')
    for i in range(len(position)):
      mutate_residue(test,int(position[i]),residue[i])
    model.pdb_info().name('start')
    test.pdb_info().name('test')
    sfxn = get_fa_scorefxn()
    relax.set_scorefxn(sfxn)
    print('relaxing.........')
    relax.apply(test)
    test.dump_pdb(out)
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode',help='"Classic" or "Fast", DEFAULT = Fast',default='Fast')
    parser.add_argument('--file')
    parser.add_argument('--pos')
    parser.add_argument('--res')
    parser.add_argument('--out')
    arg = parser.parse_args()
    main(arg.mode,arg.file,arg.pos,arg.res,arg.out)