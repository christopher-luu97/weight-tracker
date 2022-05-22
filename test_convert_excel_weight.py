import pytest
from convert_excel_weight import * 

# fixtures here

# Load in the test data
df = pd.read_excel('./input_data/Weight_tracker_2022.xlsx', sheet_name='All', engine='openpyxl')

excel_date = ExcelProcessing(df)
excel_step_1 = excel_date.drop_columns()
excel_step_2 = excel_date.rename_headers(excel_step_1)
weight_convert = WeightConverter(excel_step_2)
weight_convert_1 = weight_convert.weights_only()
weight_convert_2 = weight_convert.individual_df(weight_convert_1)
weight_convert_3 = weight_convert.long_list_of_values(weight_convert_2)
date_convert = weight_convert.dates_only(excel_step_2)
date_convert_2 = weight_convert.individual_df(date_convert)
date_convert_3 = weight_convert.long_list_of_values(date_convert_2)
export_df = weight_convert.export_file(weight_convert_3, date_convert_3)

def test_drop_columns():
    '''
    Assert column names are as expected
    '''
    # Hardcoded from ./input_data/Weight_tracker_2022.xlsx
    cols = ['Beginning Weight', 'Extra Info',
       datetime.datetime(2020, 11, 11, 0, 0),
       datetime.datetime(2020, 11, 12, 0, 0),
       datetime.datetime(2020, 11, 13, 0, 0),
       datetime.datetime(2020, 11, 14, 0, 0),
       datetime.datetime(2020, 11, 15, 0, 0), 'Average']

    np.testing.assert_array_equal(excel_step_1.columns, cols)

def test_rename_headers():
    '''
    Assert column names are as expected
    '''
    cols = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday','Average']
    np.testing.assert_array_equal(excel_step_2.columns, cols)

def test_weights_only():
    '''
    Check we have 7 rows
    Also check we have transposed correctly 
    '''
    cols = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    idx_name = weight_convert_1.index.values
    np.testing.assert_array_equal(idx_name, cols)
    assert len(weight_convert_1) == 7 

def test_individual_df():
    '''
    Check item in list is a pandas series
    '''
    assert isinstance(weight_convert_2[0], pd.core.series.Series)

def test_long_list_of_values():
    '''
    Should return a dataframe and have a single column
    '''
    assert weight_convert_3.shape[1] == 1
    assert isinstance(weight_convert_3, pd.core.frame.DataFrame)

def test_dates_only():
    '''
    Make sure all times are the right type
    '''
    assert isinstance(date_convert[0][0], pd._libs.tslibs.timestamps.Timestamp)

def test_export_file():
    '''
    Check types and columns
    '''
    cols = ['Date', 'Weight']
    np.testing.assert_array_equal(export_df.columns, cols)
    assert isinstance(export_df['Date'][0], pd._libs.tslibs.timestamps.Timestamp)
    assert export_df.shape[1] == 2