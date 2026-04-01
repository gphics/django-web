import pandas as pd
import numpy as np
from scipy.stats import shapiro, ttest_ind, mannwhitneyu
import pingouin as pg
import seaborn as sns
import matplotlib.pyplot as plt
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
        This method takes a feature and return the value with the minimum and maximum occurence

        Params:

            feature(str)

        Returns:
            dict:
                max:[actual_value, freq]

                min:[actual_value, freq]

                max_only:bool

                relative_max: int |float
                relative_min: int |float
                total:int
        """
        feature_data = self.df[feature]
        freq = feature_data.value_counts()

        # getting data length
        total_feature_count = feature_data.shape[0]

        # if only one unique value exist for the feature, in which max is the same as min, then show only the max
        max_only = True if len(freq.index) < 2 else False

        # if the max and min value occurences are the same, then show only the max
        max_only = False if str(freq.idxmax()) != str(freq.idxmin()) else True

        # generating the result 
        result = {
            "max":[str(freq.idxmax()), int(freq.max())],
            "min":[str(freq.idxmin()), int(freq.min())],
            "max_only" : max_only  # for interpretation purpose only
        }
   
        # adding relative value for interpretation purpose
        result["relative_max"] = self.get_percentage_prop(total_feature_count, result["max"][1])
        result["relative_min"] = self.get_percentage_prop(total_feature_count, result["min"][1])
        result["total"] = total_feature_count
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

    def get_percentage_prop(self, total_freq:int, feature_freq:int) -> int | float:
        """
        This function returns a percentage proportion of a particular relative to another value
        """
        return np.round(feature_freq * 100/total_freq)

    

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

    def basic_transformation(self, feature:str):
        """
        This method get the min and max occurences of a feature param
        """
        return self.get_feature_min_max(feature)
    
    def get_raw_transaction_amount(self, n:int|None=None):
        """
        This method returns the self.df['amount']

        Param:
            n: The number of transaction amount to return
        """
        if not n:
            return self.df["amount"]
        
        # if n is provided
        return self.df["amount"].sample(n=n)
    
    def get_transaction_amount_mean(self):
        """
        This method returns the mean of self.df['amount']
        """
        return self.df["amount"].mean()
    
    def verify_normalcy(self, data = None) -> bool:
        """
        This method uses shapiro to check if a particular data is normally distributed.

        Params:
        
            data?:the transaction['amount'] to test the normalcy on.

        Returns:
            bool: True  if normally distributed else False

        """
        data = data if data is not None else self.df["amount"]
        _, p_value = shapiro(data)

        significance = 0.05
        if p_value < significance:
            return False
        return True
    
    def translate_significance(self, p_value: float | int) -> bool:
        """
        This method returns a boolean value if the provided p_value is significant or not
        """

        significance = 0.05
        if p_value < significance:
            return True
        return False
    

    def check_mean_significance_ind(self, second_data, first_data=None) -> bool:
        """
        This method is responsible for performing two tailed two sample ttest or mannwhiteneyu test depending on the normalcy state of the provided data on transaction['amount'].

        Params:
            first_data?: a list containing the transaction['amount]. if not provided, the amount on self.df is used
            second_data: required, a list containing the transaction['amount]. 

        """
        # filling the first data if necessary
        first_data = first_data if first_data is not None else self.df["amount"]

        # checking if first and second data are normal
        is_normal_1 = self.verify_normalcy(first_data)
        is_normal_2 = self.verify_normalcy(second_data)

        # main operation
        if is_normal_1 and is_normal_2:
            # perform a parametric test
            _, p_value = ttest_ind(first_data, second_data, equal_var=False)
            
        else:
            # perform a non-parametric test
            _, p_value = mannwhitneyu(first_data, second_data)
            
        return self.translate_significance(p_value)
       
    
        
