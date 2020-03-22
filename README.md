# COVID-19 quick analysis

This is a package to analyse data provided by the WHO concerning the COVID-19 pandemic. Data is prepared by John Hopkins Whiting School of Engineering and can be found [here](https://github.com/CSSEGISandData). There is no guarantee whatsoever that the numbers used and plots created reflect reality. It is everyones own responsibility to ensure that.

## Installation

Prerequesites are

* [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
* [Python, Python Pip, version >= 3](https://www.python.org)

It is recommended to install everything in a Python virtual environment ([setup instructions](https://packaging.python.org/tutorials/installing-packages/#creating-virtual-environments) for versions >= 3.6)

Creating the environment has to be done only once.
```bash
python3 -m venv /path/to/new/venv
```

and it is then activated/deactivatde via

```bash
source /path/to/new/venv/bin/activate   # activate

deactivate                              # deactivate
```

The advantage of a dedicatde virtual environment is that you can, for instance, install any packages with `pip` without interfering with your central Python installation. Removing the directory of your virtual environment is enough to clean everything you did there.

To really install the package, do the following

```bash
cd /path/to/where/the/package/should/live

# Get the package
git clone https://github.com/benedikt-voelkel/COVID19-Analysis

# (Create and) Load the virtual Python environment
# ...

cd COVID19-Analysis
pip install -e .

# That's it
```

Now get the data everything is based on at the moment

```bash
cd /path/to/where/the/data/should/live

git clone https://github.com/CSSEGISandData/COVID-19
```

Now, you are all set.

Make sure, you are in the virtual environment now. Then, you can basically run the analysis from anywhere. Just type
`covid19-analysis` and hit **Enter**. It tells you that the path to the data is required as an argument. So let's do that

```bash
covid19-analysis /path/to/where/data/should/live/COVID-19
```

It should create a file `plot.png` in the directory the script was run from. 


