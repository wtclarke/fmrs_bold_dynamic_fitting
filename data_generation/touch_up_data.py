from fsl.data.image import Image
from pathlib import Path

base_path = Path('simulated_data')

import json
import nibabel as nib

def cleanhdr(img):
    hdr_ext = img.header.extensions[0].json()
    for key in ['SpectralWidth', 'NumberOfTransients', 'AcquisitionVoxelSize', 'NumberOfSpectralPoints']:
        hdr_ext.pop(key, None)

    for key in hdr_ext:
        if key in ('SpectrometerFrequency', 'ResonantNucleus'):
            continue
        hdr_ext[key] = hdr_ext[key][0]

    img.header.extensions[0] = json.dumps(hdr_ext)
    extension = nib.nifti1.Nifti1Extension(
                44,
                json.dumps(hdr_ext).encode('UTF-8'))
    img.header.extensions.clear()
    img.header.extensions.append(extension)
    return img


for fp in base_path.rglob('*.nii.gz'):
    print(fp)
    cleanhdr(Image(fp)).save()
