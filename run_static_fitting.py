from pathlib import Path
from fsl_pipe import Pipeline, In, Out, Ref
from fsl.wrappers.fsl_mrs import fsl_mrs
from file_tree import FileTree

base_dir = Path(__file__).parent
tree = FileTree.read(base_dir / 'dynamic_fitting.tree')
tree.update_glob('avg_data', inplace=True)


def name(x: Path) -> str:
    return x.with_suffix('').with_suffix('').name


def fit_default(
    avg_data: In,
    static_fit_default: Out,
    basis: Ref
):
    "Average data, normal basis = default"
    fsl_mrs(
        avg_data,
        basis,
        static_fit_default,
        baseline='poly,1',
        no_rescale=True)
    
def fit_preproc_lw(
    avg_data_broadened: In,
    static_fit_preproc_lw: Out,
    basis: Ref
):
    "Broadened data, normal basis = preproc_lw"
    fsl_mrs(
        avg_data_broadened,
        basis,
        static_fit_preproc_lw,
        baseline='poly,1',
        no_rescale=True)

def fit_basis_lw(
    avg_data: In,
    static_fit_basis_lw: Out,
    basis_broadened: Ref
):
    "Normal data, broadened basis = basis_lw"
    fsl_mrs(
        avg_data,
        basis_broadened,
        static_fit_basis_lw,
        baseline='poly,1',
        no_rescale=True)


pipe = Pipeline(default_submit=dict(logdir="processing_logs_static"))
pipe(fit_default, submit=dict(jobtime=int(5)), as_path=False)
pipe(fit_preproc_lw, submit=dict(jobtime=int(5)), as_path=False)
pipe(fit_basis_lw, submit=dict(jobtime=int(5)), as_path=False)


if __name__ == "__main__":
    pipe.cli(tree)
