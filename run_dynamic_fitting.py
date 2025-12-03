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


@cmdwrapper
def fmrs_stats(dirs, output, fl_contrasts, contrasts, ftests):
    dirs_as_list = [str(x) for x in dirs.data]
    cmd = [
        'fmrs_stats',
        '--data',]\
        + dirs_as_list\
        + ['--output', output,
        '--fl-contrasts', fl_contrasts,
        '--combine', 'NAA', 'NAAG',
        '--combine', 'Cr', 'PCr',
        '--combine', 'PCh', 'GPC',
        '--combine', 'Glu', 'Gln',
        '--hl-contrasts', contrasts,
        '--hl-ftests', ftests,
        '--overwrite']
    print(cmd)
    return cmd


def second_level(
    first_level_fit: In,
    hl_contrasts: In,
    hl_ftests: In,
    fl_contrasts: In,
    second_level: Out
):
    fmrs_stats(first_level_fit, second_level, fl_contrasts, hl_contrasts, hl_ftests)

pipe = Pipeline(default_submit=dict(logdir="processing_logs"))
pipe(first_level, submit=dict(jobtime=int(120)), as_path=True)
pipe(second_level, submit=dict(jobtime=int(20)), as_path=False, no_iter=['subject'])


if __name__ == "__main__":
    pipe.cli(tree)
