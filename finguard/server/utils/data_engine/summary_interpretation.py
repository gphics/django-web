from .financial_activity_using_std import get_financial_activity


class Helper:
    """
    This class holds method which are not part of the business logic
    """
    month_str = [
        "_", #because month range in python is 1-12
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December"
    ]
    def format_hour(self, value:int) -> str:
        """
        This method convert 24hrs format to 12hrs format
        """
        value = int(value)
        period = "AM" if value < 12 else "PM"

        hour_12 = value % 12

        return f"{hour_12} {period}"
    
    def format_month(self, value:int) -> str:
        """
        This method convert month(int) to it's string version
        """
        value = int(value)
        month = self.month_str[abs(value)]

        return month
        

deep_template = """

Based on your transaction history, February saw your highest average spending at ₦6,022.38, while March remained the lowest at ₦4,925.67. Your single largest purchase reached ₦8,856.00 in March, even though that same month also recorded your smallest transaction of just ₦203.00. In terms of activity, March was your busiest period with 24 total entries, compared to a quieter 16 entries in February.

"""
transaction_date = """
"Your monthly transaction count ranged from a low of 16 in February to a high of 24 in March. This shows an uptick in activity as you moved into the later part of the quarter."
"""


summ = """

You have completed a total of 40 transactions, with an overall average value of ₦5,364.35. Most of your spending falls within a broad range, starting from a small purchase of ₦203.00 up to a maximum of ₦8,856.00. When looking at the middle of your spending habits, your typical transaction value is ₦5,985.00, with half of all your purchases falling between ₦3,290.75 and ₦7,283.25.

"You completed 40 transactions this month with an average value of ₦5,364.35. However, your habits were quite varied, with a typical swing of ₦2,527.05 between different purchases. While half of your activity stayed above ₦5,985.00, the total range was wide, spanning from a low of ₦203.00 to a peak of ₦8,856.00

"""

class InterpretationEngine(Helper):
    
    def __init__(self, data, currency:str, financial_activity:str):

        # destructuring the data parameter
        self.amount = data.get("amount", None)
        self.category = data.get("category", None)
        self.flagged = data.get("flagged", None)
        self.transaction_dates = data.get("transaction_dates", None)
        self.transaction_type = data.get("transaction_type", None)
        self.amount_by_date = data.get("amount_by_date", None)

        # others
        self.currency = currency
        self.financial_activity = str(financial_activity).lower()
        self.date_time_features = ["hour", "month",  "day_name", "month_day"]
        self.agg_params = ["mean", "min", "max", "count"]

     
    def interpret_amount(self) -> str:
        """
        This method interpret the amount feature.
        """
        amount = self.amount
        currency = self.currency

        # destructuring amount metrics
        count = int(amount["count"])
        mean = amount["mean"]
        std = amount["std"]
        min_ = amount["min"]
        max_ = amount["max"]
        percentile_25 = amount["25%"]
        percentile_50 = amount["50%"]
        percentile_75 = amount["75%"]
        
        paragraph = f""" You have a total of {count} transactions with an average transaction amount of {currency} {mean}. However, your financial activity were {self.financial_activity},  with a typical swing of {currency} {std} between transactions. When looking at the middle of your financial activity, your typical transaction value is {currency} {percentile_50}, 25% of your transactions are for {currency} {percentile_25} or less while 75% of your transactions are for {currency} {percentile_75} or less. Lastly, your lowest and highest transaction amounts are {currency} {min_} and {currency} {max_} respectively. """

        return paragraph

    def interpret_location_amount(self, location, location_type="city") ->str :
        """
        This method interpret the transaction summary statistics for a particular location
        """
        amount = self.amount
        currency = self.currency

        # destructuring amount metrics
        count = int(amount["count"])
        mean = amount["mean"]
        std = amount["std"]
        min_ = amount["min"]
        max_ = amount["max"]
        percentile_25 = amount["25%"]
        percentile_50 = amount["50%"]
        percentile_75 = amount["75%"]
        location_financial_activity = get_financial_activity(std, mean)

        paragraph = f""" Based on the latest transaction data for {location} {location_type}, there have been {count} transactions recorded. The average transaction amount is {currency} {mean} with a typical swing of {currency} {std} between transactions which is {str(location_financial_activity).lower()}. Transaction amounts range from a minimum of {currency} {min_} to a maximum of {currency} {max_}. 25% of total transactions in {location} have a transaction amount of  {currency} {percentile_25} or less, 50% of total transactions in {location}  have a transaction amount of  {currency} {percentile_50} or less, and 75% of total transactions in {location}  have a transaction amount of  {currency} {percentile_75} or less. """

        return paragraph
    
    def interpret_transaction_dates(self) -> list:
        """
        This method interpret transaction dates
        """
        result = []

        for date_feature in self.date_time_features:
            feature_data = self.transaction_dates[date_feature]
            max_ = feature_data["max"]
            min_ = feature_data["min"]

            # if the feature is either hour or month
            if date_feature in ["hour", "month"]:

                # creating the title
                title = date_feature+"ly"

                # creating default values
                min_period = ""
                max_period = ""
                pointer_adj = "in"

                # if feature is month
                if date_feature == "month":

                    # formating month(int) to month(str)
                    min_period = self.format_month(min_[0])
                    max_period = self.format_month(max_[0])

                # if feature is hour
                else:

                    # updating the adj
                    pointer_adj = "at"

                    # formating hour from 24hrs to 12hrs
                    min_period = self.format_hour(min_[0])
                    max_period = self.format_hour(max_[0])

                # creating the interpretation
                paragraph = f"""Your {title} transaction count ranged from a low frequency of {min_[1]} {pointer_adj} {min_period} to a high of {max_[1]} {pointer_adj} {max_period}. """

                # appending the interpretation to the result list
                result.append(paragraph)
            else:
                title =  "day of the week" if date_feature == "day_name" else "day of the month"
                paragraph = f""" The {title} with the highest volume of transaction is {max_[0]} with a frequency of {max_[1]} and the lowest is {min_[0]} with a frequency of {min_[1]}.  """
                result.append(paragraph)
        
        return result


    def interpret_amount_by_date(self) -> list:
        """
        This method interpret the amount by date
        """    

        result = []

        # looping through all date time features
        for date_feature in self.date_time_features:

            # getting specific date time feature data
            feature_data = self.amount_by_date[date_feature]

            # final process
            result.append(self.handle_feature_data(feature_data, date_feature))

        return result

    def handle_feature_data(self, data, date_feature):
        """

        This process handle the actual data interpretation for the amount by date.

        """
        result = []
        for param in self.agg_params:
            param_data = data[param]
            
            # getting the min and max for each of the param
            max_ = param_data["max"]
            min_ = param_data["min"]

            # if the feature is either hour or month
            if date_feature in ["hour", "month"]:

                # creating the title
                title = date_feature+"ly"

                # creating default values
                min_period = ""
                max_period = ""
                pointer_adj = "in"

                # if feature is month
                if date_feature == "month":

                    # formating month(int) to month(str)
                    min_period = self.format_month(min_[0])
                    max_period = self.format_month(max_[0])

                # if feature is hour
                else:

                    # updating the adj
                    pointer_adj = "at"

                    # formating hour from 24hrs to 12hrs
                    min_period = self.format_hour(min_[0])
                    max_period = self.format_hour(max_[0])

                # creating the interpretation
                if param == "mean":
                    paragraph = f""" {max_period} saw your highest average spending at {self.currency} {max_[1]} while {min_period} is the lowest at {self.currency} {min_[1]}. """
                elif param == "max":
                    paragraph = f""" Your single largest transaction of {self.currency} {max_[1]} occurs {pointer_adj} {max_period}. """
          
                elif param == "min":
                    paragraph = f""" while your single smallest transaction of {self.currency} {min_[1]} occurs {pointer_adj} {min_period}. """
                else:
                    paragraph = f""" In terms of activity, {max_period} was your busiest period with {max_[1]} total transactions, compared to a quieter {min_[1]} total transactions {pointer_adj} {min_period}. """

                # appending the interpretation to the result list
                result.append(paragraph)

            else:
                title =  "day of the week" if date_feature == "day_name" else "day of the month"
                paragraph = f""" The {title} with the highest volume of transaction is {max_[0]} with a frequency of {max_[1]} and the lowest is {min_[0]} with a frequency of {min_[1]}.                """
                # creating the interpretation
                if param == "mean":
                    paragraph = f""" The {title} with the highest average spending of {self.currency} {max_[1]} is {max_[0]} while the {title} with the lowest average spending of {self.currency} {min_[1]} is {min_[0]}. """
                elif param == "max":
                    paragraph = f""" Your single largest transaction of {self.currency} {max_[1]} occurs on the {title} {max_[0]}. """
          
                elif param == "min":
                    paragraph = f""" Your single smallest transaction of {self.currency} {min_[1]} occurs on the {title} {min_[0]}. """
                else:
                    paragraph = f""" In terms of activity, the {title} {max_[0]} was your busiest period with {max_[1]} total transactions, compared to a quieter {title} {min_[0]} with a total transactions of {min_[1]}. """
                result.append(paragraph)
        
        return result
       

    def interpret_category(self):
        """
        This method interpret the category summary stat
        """
        data = self.category
        min_ = data["min"]
        max_ = data["max"]

        total = data["total"]
        max_only = data["max_only"]
        relative_min = data["relative_min"]
        relative_max = data["relative_max"]

        max_section = f"Your most active transaction category is {max_[0]}, appearing {max_[1]} times ({relative_max} % of your total transactions)."
        min_section = f"In contrast, {min_[0]} saw the least activity with only {min_[1]} recorded transaction ({relative_min} % of your total transactions)."

        paragraph = max_section if max_only else max_section+" " + min_section
        
        return paragraph
    
    def interpret_flagged(self):
        """
        This method interpret the flagged summary stat
        """
        data = self.flagged
        min_ = data["min"]
        max_ = data["max"]

        total = data["total"]
        max_only = data["max_only"]
        relative_min = data["relative_min"]
        relative_max = data["relative_max"]
        print(data)
        action_word = "anomalous" if max_[0] == True else "normal"

        max_section = f"From the review of your transaction activities. Out of {total} transactions, {max_[1]} transactions ({relative_max}%) have been flagged as {action_word} transactions "

        min_section = f"while {min_[1]} transactions ({relative_min}%)  were processed normally."

        paragraph = max_section+"." if max_only else max_section+" " + min_section
        
        return paragraph
    

    def interpret_transaction_type(self):
        """
        This method interpret the transaction_type summary stat
        """
        data = self.transaction_type
        min_ = data["min"]
        max_ = data["max"]

        total = data["total"]
        max_only = data["max_only"]
        relative_min = data["relative_min"]
        relative_max = data["relative_max"]


        max_section = f"From the review of your transaction activities. Out of {total} transactions, {max_[1]} transactions ({relative_max}%) are {str(max_[0]).lower()} transactions "

        min_section = f"while {min_[1]} transactions ({relative_min}%) are {str(min_[0]).lower()} transaction."

        paragraph = max_section+"." if max_only else max_section+" " + min_section
        
        return paragraph


 
    
    def interpret_all(self):
        """
        
        """
        result = {}

        result["amount"] = self.interpret_amount()
        result["transaction_dates"] = self.interpret_transaction_dates()
        result["amount_by_date"] = self.interpret_amount_by_date()
        result["category"]=self.interpret_category()
        result["flagged"]=self.interpret_flagged()
        result["transaction_type"]=self.interpret_transaction_type()


        return result

    