from scipy.io import loadmat, savemat  # this is the SciPy module that loads and saves mat-files
import pandas as pd
from datetime import datetime, timedelta
import numpy as np


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
    exo = mat['optStr']['entrySignalingSeries'][0][0][3] / mat['optStr']['tickIncrement'][0][0][0][0] * mat['optStr']['tickValue'][0][0][0][0]
    dates = list(map(convert_mat_date, mat_date))

    #print(mat['optStr'].dtype.names)

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


def exportdata(path, date, data_dict):
    """
    Exports Pandas.Series to .mat file
    :param path: path to file
    :param date: python datetime array
    :param data_dict: dictionary of pandas.Series to export
    :return: Empty
    """
    mdict = {}

    def convert_date_to_mat(dt):
        """
        Python to Matlab date convert helper function
        """
        mdn = dt + timedelta(days=366)
        frac = (dt-datetime(dt.year, dt.month, dt.day, 0, 0, 0)).seconds / (24.0 * 60.0 * 60.0)
        return mdn.toordinal() + frac

    mdict['date'] = np.array(list(map(convert_date_to_mat, date)))
    # Converting Pandas.Series to NumPy array
    for key, value in data_dict.items():
        # Check length equality
        if len(date) != len(value):
            raise ValueError('Length of all arrays must be equal')
        mdict[key] = value.values

    # Saving data to .mat file
    savemat(path, mdict=mdict)

