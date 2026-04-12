from pathlib import Path
import joblib
import pandas as pd
from sklearn.ensemble import IsolationForest
from feature_engine.encoding import CountFrequencyEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer

class EngineUtils:
    """
    This class hadles all operations not directly related to the business logic
    """

    # default variables
    model_store_dir_name = "model_store"
    base_dir = Path(__file__).resolve().parent.parent
    
    def __init__(self, data:list, user_id:int, retrain:bool=False):
        """
        # Conditions for a retrain:
            - First model creation: the retrain serves as a guide so that the new model can be saved locally. Just for direction.

            - Actual retrain
        
        """
        self.raw_df = pd.DataFrame(data)
       
        self.user_model_file_name = f"user_{user_id}_model.joblib"
        self.user_model_file_path  = f"{self.base_dir}/{self.model_store_dir_name}/{self.user_model_file_name}"

        # deleting the model if retrain is necessary
        if retrain:
            self.delete_model()

        # creating the encoder
        self.generate_feature_transformer()
 
        # retrieving / initializing the model
    
        if self.verify_user_model():
            self.model = self.retrieve_model()
          
        else:
            self.model = IsolationForest()
       


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


    def verify_user_model(self) -> bool:
        """
        This method checks if the user already have his model saved before
        """
        file_path = Path(self.user_model_file_path)

        if file_path.exists():
            return True
        return False


    def save_model(self):
        """
        Savig the model
        """
        try:
            joblib.dump(self.model, self.user_model_file_path)
        except Exception as e:
            print(str(e))
        
    def retrieve_model(self) -> IsolationForest:
        """
        Retrieving saved model
        """
        try:
            # getting the saved model
            user_model = joblib.load(self.user_model_file_path)

            # saving the loaded data
            self.model = user_model

            return user_model
        except Exception as e:

            return None
        
    def delete_model(self):
        file = Path(self.user_model_file_path)

        # deleting the model file
        file.unlink(missing_ok=True)
    

    def generate_feature_transformer(self):
        """
        Generates the encoder.

        This method saves:
            ct: column transformer
            X: the encoded default raw data
        """

        transformers = [
            ("ohe", OneHotEncoder(sparse_output=False, drop="if_binary",categories=[["CREDIT", "DEBIT"]]), ["transaction_type"]),
            ("freq_enc", CountFrequencyEncoder(), ["category"])
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
        if not self.verify_user_model():

            # training ...
            self.model.fit(self.X)

            # saving the model locally
            self.save_model()

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
        
        return result.to_dict(orient="records")
