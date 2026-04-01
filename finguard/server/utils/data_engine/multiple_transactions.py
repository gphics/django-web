import pandas as pd
from pandas.api.types import is_numeric_dtype
import numpy as np


class Helper:
    """
    This is the utils class for the main class performing this file processing operations
    """

    acceptable_content_type = "text/csv"
    # compulsorily present cols
    required_cols = ["amount", "category", "transaction_date"]

    # optionally present cols
    optional_cols = ["transaction_type", "description"]

    def __init__(self, file):
        self.file_name:str = file.name
        self.content_type:str = file.content_type

        # validating content type as only csv file is required
        self.validate_content_type()
        
        # initializing dataframe
        self.df = pd.read_csv(file)
        
        # validating the df
        # ...

        # column validation
        self.validate_df_cols()

        # transaction_date col validation
        self.validate_col_transaction_date()

        # validating the number dtype status of the amount col
        self.validate_col_amount()

        # checking and raising error if empty value is present
        self.validate_is_null()


    def validate_content_type(self):
        """
        This method validate the file content type
        """

        if self.acceptable_content_type != self.content_type.lower():
            raise Exception(f"Only csv file is accepted")
        
    
    def validate_df_cols(self):
        """
        This method validate the created dataframe columns availability.

        Required cols:
            amount: int
            category: int|str
            transaction_date: str (later to datetime)

        Optional cols:
            transaction_type:str
            description:str
        """
        # getting the df
        df = self.df

        # getting the df cols
        df_cols = df.columns.to_list()
        # checks ...
        required_column_checks = {}

        # looping through the required columns
        for req_col in self.required_cols:

            # if the req_col is present in the df
            if req_col in df_cols:
                required_column_checks[req_col] = True

            # else
            else:
                required_column_checks[req_col] = False

        # raising errors if the required col is absent
        for key, value in required_column_checks.items():

            if value == False:
                raise Exception(f"{key} column does not exist")
        
        # for the optional columns
        for opt_col in self.optional_cols:

            # if the opt_col is present, append it to the required cols
            if opt_col in df_cols:
                self.required_cols.append(opt_col)
           
        # updating the df
        self.df = df[self.required_cols].copy()
        
    def validate_col_transaction_date(self):
        """
        This method transform the data type of transaction date col to datetime and raise error if not possible.
        """
        try:
            self.df["transaction_date"] = pd.to_datetime(self.df["transaction_date"])
        except Exception as e:
            raise e

    def validate_col_amount(self):
        """
        This method validate if the amount col is of number dtype
        """

        is_num = is_numeric_dtype(self.df["amount"])

        if not is_num:
            raise Exception("The amount column can only contain number")

    def validate_is_null(self):
        """
        This method checks for nullish values
        """
        null_list = self.df.isnull().mean()*100
        
        null_cols = null_list[null_list > 0].index.to_list()

        if len(null_cols):
            cols_str = ", ".join(null_cols)
            raise Exception(f"{cols_str} contains empty values. ")
        
    
class TransactionFileProcesor(Helper):
    """
    This is the file processing class. It's main output is the json (list of dict) for all rows in the csv file uploaded by the user.
    """
    
    def transform_to_json(self) -> list:
        """
        This method transform the df json(list of dicts) to be used for creating the transaction
        """

        return self.df.to_dict(orient="records")