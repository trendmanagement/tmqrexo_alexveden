from scipy.io import loadmat  # this is the SciPy module that loads mat-files
import pandas as pd
from datetime import datetime, timedelta


def loaddata(path):
    """
    Load EXO data from .mat file and return Pandas.Dataframe
    :param path: path to .mat file
    :return: Pandas.Dataframe, info dict (tuple)
    """

    def convert_mat_date(matlab_datenum):
        """
        Matlab to Python date convert helper function
        """
        return datetime.fromordinal(int(matlab_datenum)) + timedelta(days=int(matlab_datenum%1)) - timedelta(days=366)

    # Loading .mat file
    mat = loadmat(path)

    # Getting date and exo series from .mat container
    mat_date = mat['optStr']['seriesDates'][0][0][0]
    exo = mat['optStr']['entrySignalingSeries'][0][0][3]
    dates = list(map(convert_mat_date, mat_date))

    info = {
        'name': mat['optStr']['cfgName'][0][0][0],
        'underlying': mat['optStr']['instrumentSymbol'][0][0][0],
        'tickincrement': mat['optStr']['tickIncrement'][0][0][0][0],
        'tickvalue': mat['optStr']['tickValue'][0][0][0][0],
        'pcf': mat['optStr']['pcf'][0][0][0],
        'pcfqty': mat['optStr']['cfgContracts'][0][0][0],
        'legs': mat['optStr']['legs'][0][0][0][0],
    }

    # Return Pandas DataFrame object and information about spread
    return pd.DataFrame({'exo': exo}, index=dates), info

