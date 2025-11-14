from pathlib import Path
from fsl_pipe import Pipeline, In, Out
from fsl.wrappers import cmdwrapper
from file_tree import FileTree

base_dir = Path(__file__).parent
tree = FileTree.read(base_dir / 'dynamic_fitting.tree')
tree.update_glob('raw_data', inplace=True)
tree.update_glob('first_level_design_mat', inplace=True)


def name(x: Path) -> str:
    return x.with_suffix('').with_suffix('').name


@cmdwrapper
def fsl_dynmrs(path, basis, config, des_mat, output):
    return ['fsl_dynmrs',
            '--data', str(path),
            '--basis', str(basis),
            '--dyn_config', str(config),
            '--time_variables', str(des_mat),
            '--baseline', 'off',
            '--output', str(output),
            '--report',
            '--overwrite']


def first_level(
        raw_data: In,
        basis: In,
        first_level_config: In,
        first_level_design_mat: In,
        first_level_fit: Out):
    fsl_dynmrs(
        raw_data,
        basis,
        first_level_config,
        first_level_design_mat,
        first_level_fit)


pipe = Pipeline(default_submit=dict(logdir="processing_logs"))
pipe(first_level, submit=dict(jobtime=int(120)), as_path=True)


if __name__ == "__main__":
    pipe.cli(tree)
