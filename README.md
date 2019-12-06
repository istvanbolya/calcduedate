# Calculate Due date
A module to calculate issue resolve date.

* [Installation](#installation)
* [Usage](#usage)
* [Unittests](#unittests)

## Installation
The module uses base Python3.x libraries only.

I suggest to use [virtualenv](https://www.pythonforbeginners.com/basics/how-to-use-python-virtualenv) with Python 3.x.
After installing virtualenv, create a new one for the module:

```
mkdir ~/calcduedate
virtualenv ~/calcduedate/venv
```

Activate the env.:

```
cd ~/calcduedate
source venv/bin/activate
```

Checkout the source:

`git clone https://github.com/istvanbolya/calcduedate.git`


## Usage
The module contains a `run_calcduedate.py` script, which shows the basic usage:
- Create a `CalcDueDate()` instance
- call the `.calculate()` method with params: `submit_datetime, turnaround_time`

If there is a validation/calculation issue, the module will raise a `CalcDueDateException`.

## Unittests
You can run the unittests by executing unittest under the module directory in virtualenv:
 
 `python -m unittest`
