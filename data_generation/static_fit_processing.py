from pathlib import Path

base_path = Path('simulated_data')

from fsl_mrs.utils import mrs_io
from fsl_mrs.utils.preproc import nifti_mrs_proc as nproc
import fsl_mrs.core.nifti_mrs as ntools
import numpy as np

def average(img, indices, ndyn):
    imgs = []
    for idx in indices:
        _, tmp = ntools.split(
            img,
            'DIM_DYN',
            np.arange(idx, idx+ndyn).tolist())
        print(tmp.shape)
        tmp = nproc.average(
            tmp,
            'DIM_DYN'
        )
        imgs.append(tmp.remove_dim('DIM_COIL'))
    return imgs


for fp in base_path.rglob('*.nii.gz'):
    print(fp)
    data = mrs_io.read_FID(fp)
    if '3T' in str(fp):
        averaged = average(
            data,
            np.arange(0, 640, 128),
            128
        )
    
    elif '7T' in str(fp):
        averaged = average(
            data,
            np.arange(0, 320, 64),
            64
        )
    subject = fp.parent.parent.stem
    for idx, avg in enumerate(averaged):
        avg.save(fp.parent / f'{subject}_{idx:0.0f}_svs.nii.gz')