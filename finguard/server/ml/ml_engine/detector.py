from pathlib import Path
import joblib
import pandas as pd
from sklearn.ensemble import IsolationForest
from feature_engine.encoding import CountFrequencyEncoder
from sklearn.preprocessing import OneHotEncoder, RobustScaler
from sklearn.compose import ColumnTransformer

class EngineUtils:
    """
    This class hadles all operations not directly related to the business logic
    """

    # default variables

    
    def __init__(self, data:list):
        """
        # Conditions for a retrain:
            - First model creation: the retrain serves as a guide so that the new model can be saved locally. Just for direction.

            - Actual retrain
        
        """
        self.raw_df = pd.DataFrame(data)

        # converting amount to int
        self.raw_df["amount"] = self.raw_df["amount"].astype(int)

    
        # creating the encoder
        self.generate_feature_transformer()
 
        # initializing the model
    
        self.model = IsolationForest(contamination=0.1, random_state=42, max_features=0.5, max_samples=self.raw_df.shape[0])
        
       
    def remove_df_id(self, data:pd.DataFrame |None =None):
        """
        This method removes the id col from the data, save it as self.target_id and return the df that remains.

        # Note: this operation should be done before encoding.
        """
        target_df = self.raw_df if not data else data

        # cloning ...
        target_df = target_df.copy()

        # subsetting id
        target_id = target_df.pop("id")

        # saving the target id that was removed
        self.target_id = target_id

        return target_df

    
    def generate_feature_transformer(self):
        """
        Generates the encoder.

        This method saves:
            ct: column transformer
            X: the encoded default raw data
        """

        transformers = [
            ("ohe", OneHotEncoder(sparse_output=False, drop="if_binary",categories=[["CREDIT", "DEBIT"]]), ["transaction_type"]),
            ("freq_enc", CountFrequencyEncoder(), ["category"]),
            ("scaling", RobustScaler(), ['amount', 'month', 'hour', 'month_day', 'weekday'])
            
        ]

        ct = ColumnTransformer(transformers, verbose_feature_names_out=False, remainder="passthrough")

        ct.set_output(transform="pandas")

        # data without id
        new_data = self.remove_df_id()
        
        # training the encoder with a data without the id column
        self.X = ct.fit_transform(new_data)
        
        # saving the encoder
        self.ct = ct




class AnomalyDetectionEngine(EngineUtils):
    """
    Main properties:
        - ct: column transformer for encoding
        - model
        - X: encoded raw data
    """

    def encode_data(self, data:dict|None=None):
        """
        This method transform the data and save it as X
        """

        df = pd.DataFrame(data)

        # transforming data
        X = self.ct.transform(self.remove_df_id(df))

       
        # saving X
        self.X = X

        return X


    def train_model(self):
        """
        training the model, if it's just newly created
        """
        

        # training ...
        self.model.fit(self.X)

        

    def predict(self, data=None):
        """
        This method helpe to make predictions
        """

        model = self.model

        if not data:
            X_test = self.X
        else:
            X_test = self.encode_data(data)
        
        # making predictions
        predictions = model.predict(X_test)
        result = pd.DataFrame()

        result["id"] = self.target_id
        result["flagged"] = (predictions == -1)
        
        # return result
        return result.to_dict(orient="records")


# script_dir = Path(__file__).resolve().parent
# df = pd.read_csv(script_dir/"guest.csv")
# df = df.drop(columns=["Unnamed: 0"])
# print(df)

# print(df[df["id"].isin([43,42,17,13,7]) ])
# print(df.nsmallest(2, columns=["amount"]))

# model = AnomalyDetectionEngine(df, 166)

# model.train_model()


# pred = model.predict()

# print(pred[pred["flagged"] == True ])

# print(df)

# print(model.X.head())
# print(model.X.columns.to_list())