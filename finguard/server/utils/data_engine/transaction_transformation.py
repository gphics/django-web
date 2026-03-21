import pandas as pd
import numpy as np

class TransformationUtils:
    """
    This class handle non-business related operations or those considered not main ops.
    """

    agg_params = ["mean", "min", "max", "count"]

    def __init__(self, all_trans):
        self.raw_data = [*all_trans]
        self.df = pd.DataFrame(self.raw_data)

        # transforming date
        self.df["transaction_date"] = pd.to_datetime(self.df["transaction_date"])

        self.extract_date_info()


    def extract_date_info(self):
        """
        This function extract necessary and needed date time informations
        """
        self.df["month"] = self.df["transaction_date"].dt.month
        self.df["hour"] = self.df["transaction_date"].dt.hour

        # day of the month (1-31)
        self.df["month_day"] = self.df["transaction_date"].dt.day
        self.df["weekday"] = self.df["transaction_date"].dt.weekday
        # e.g friday ...
        self.df["day_name"] = self.df["transaction_date"].dt.day_name()

    def get_feature_min_max(self, feature:str):
        """
        This method takes a feature and return the value with minimum and maximum occurence

        Params:

            feature(str)

        Returns:
            dict:
                max:[actual_value, freq]

                min:[actual_value, freq]
        """
        freq = self.df[feature].value_counts()
        result = {
            "max":[str(freq.idxmax()), int(freq.max())],
            "min":[str(freq.idxmin()), int(freq.min())],
        }
        return result

    def amount_deep_dive(self, feature:str):
        """
        This method group amount base on date time feature
        """
        grouped_df = self.df.groupby(feature)["amount"]
        grouped_df = grouped_df.describe().round(2)

        # print(grouped_df)

        result = {}
        for param in self.agg_params:
            first = self.get_large_small_agg_params(grouped_df, param)
            result[param] = first
        return result
    
    def get_large_small_agg_params(self, grouped_df, param:str):
        """
        This method is meant to work synergistically with self.amount_deep_dive. 

        Params:
            grouped_df: the result of describe() on a df grouped base on a certain date time feature
            param: the specific agg param to get

        Returns:
            dict:
                max:[index(feature), value(param)]
                min:[index(feature), value(param)]
        """


        target = grouped_df[param]
        smallest = target.nsmallest(1)
        largest = target.nlargest(1)

        result = {
            "min":[smallest.index[0], smallest.values[0]],
            "max":[largest.index[0], largest.values[0]],
        }
        return result

class MainEngine(TransformationUtils):
    """
    This class is responsible for transforming the transaction data into a usable form and also get the summary statistics of features.
    """
        
    def transform_amount(self, deep=False):
        """
        This method returns the summary statistics for the amount feature
        
        Param:
            deep(bool)

        Returns:
            if deep, an in-depth investigation into the amount feature using date time features is returned. and vice versa
        """
        if not deep:
            return self.df["amount"].describe().round(2).to_dict()
        
        deep_features = ["month", "hour", "month_day", "weekday", "day_name"]
        result = {}
        for feature in deep_features:
            result[feature] = self.amount_deep_dive(feature)
        return result
        
    

    def transform_transaction_date(self):
        """
        This method returns the summary statistics for the extracted date time features
        """

        try:
            # working on month
            month = self.get_feature_min_max("month")
            hour = self.get_feature_min_max("hour")
            month_day = self.get_feature_min_max("month_day")
            weekday = self.get_feature_min_max("weekday")
            day_name = self.get_feature_min_max("day_name")

            result = {
                "month": month,
                "hour": hour,
                "month_day": month_day,
                "weekday":weekday,
                "day_name":day_name
            }

            return result
        except Exception as e:
            print(e)

    
        
