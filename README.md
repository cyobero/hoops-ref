# hoops-ref
A Python client for retrieving statistics from basketball-reference.com

## Motivation
As an NBA analytics enthusiast and Python data analyst, I wanted a library that would allow me to easily retrieve NBA statistics while working in ipython or Jupyter notebook.

## Quick Usage
First, clone this repo and change into directory.
```
git clone https://github.com/cyobero/hoops-ref && cd hoops-ref
```
Then, once you're in python you can create a new client instance 
```python
In [13]: from hoops_ref import HoopsRefClient

In [14]: cli = HoopsRefClient()

In [15]: df = cli.games("CHI", 2022)

In [16]: df.head()
Out[16]:
                               Opponent   Tm  Opp Venue
Date
Wed, Oct 20, 2021       Detroit Pistons   94   88     A
Fri, Oct 22, 2021  New Orleans Pelicans  128  112     H
Sat, Oct 23, 2021       Detroit Pistons   97   82     H
Mon, Oct 25, 2021       Toronto Raptors  111  108     A
Thu, Oct 28, 2021       New York Knicks  103  104     H
```
