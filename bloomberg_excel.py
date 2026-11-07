import pandas as pd

def get_data(isin):
    """
    Return ticker, timeseries dataframe, and metadata dataframe for a given ISIN 

    Example call:
    df_timeseries, df_metadata, name = get_data("US21873SAL25")
    
    """
    file = pd.read_excel(
        "data/converts_backup_v2.xlsx",
        sheet_name=isin,
    )
    name = str(file.iloc[0,0]) # corp equity ticker location in excel
    df_timeseries, df_metadata = clean_data(file)

    return df_timeseries, df_metadata, name

def clean_data(file):
    """
    Helper function to clean the dataframes from the excel file.
    Return two clean dataframes: point in time timeseries and static metadata 
    """
    col_timeseries =['Date',
            'Bond price', 'Bid price', 'Ask price', 'Yield to maturity',
            'Z-spread','Stock price', '30-day volatility', '90-day volatility',
            'Dividend yield', 'Beta']
    
    col_metadata =['Parity', 'Conversion premium', 'Bond floor', 'Delta', 'Gamma','Implied volatility', 'Face value','Conversion ratio',
                'Conversion price','Effective duration', 'Yield to worst',
                'Outstanding', 'Seniority', 'Coupon rate',
                'Maturity date', 'Coupon frequency', 'Dividend yield.1',
                'Settlement date', 'Issuer', 'Currency',
                'Callable?', 'Puttable?']

    file.rename(columns={file.columns[0]: "Date"}, inplace=True) # Name column 0 as date
    # Remove metadata rows and before parsing dates
    df_timeseries = file[col_timeseries].copy()    
    df_timeseries = df_timeseries.iloc[2:].reset_index(drop=True)
    df_timeseries["Date"] = pd.to_datetime(df_timeseries['Date'])
    df_timeseries = df_timeseries.set_index("Date")    

    # Remove timeseries rows and before parsing dates
    df_metadata = file[col_metadata].copy()
    df_metadata = df_metadata.iloc[1:3].reset_index(drop=True) # keep only first two rows of metadata

    return df_timeseries, df_metadata
