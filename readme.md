# The Impact of BOLD Induced Linewidth Modulation on Functional 1H MRS Analysis - Dynamic Fitting

This repository accompanies the work `The Impact of BOLD Induced Linewidth Modulation on Functional 1H MRS Analysis` by Martin Wilson, Simon Finney and William Clarke.

## Installation
This repository uses the [Pixi](https://pixi.prefix.dev/latest/) package manager. Install `pixi` by following the [online documentation](https://pixi.prefix.dev/latest/installation/).

On linux or mac run:
```
curl -fsSL https://pixi.sh/install.sh | sh
```
and restart your terminal or shell to make the installation take effect.


## Running the analysis

To generate the data run:
```
pixi run generate_data
```

Then to run the dynamic fitting (all three models) run:
```
pixi run dynamic-fit
```

To load, explore the data and generate the plots present in the `figures` directory run the
`results_analysis.ipynb` notebook, setting the environment to the `pixi` `default` environment.

## Licensing
This repository is released under the MIT License.
