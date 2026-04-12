from pathlib import Path
import shutil

class ModelStorageEngine:
    """
    This utility class is meant to be used by a celery bg task to handle the cleanup of model files
    """

    # ml app file path
    base_dir = str(Path(__file__).resolve().parent.parent)

    storage_dir = Path(f"{base_dir}/model_store")


    def does_user_model_exist(self, user_id:int) ->bool:
        """
        This method checks if a model instance has been saved for a specific user
        """
        user_model_file_path = Path(self.construct_user_model_file_path(user_id))
        if user_model_file_path.exists():
            return True
        return False
        

    def construct_user_model_file_path(self, user_id:int) ->str:
        """
        This method construct the file path for the user and return it(str)
        """
        
        file_path = f"{self.storage_dir}/user_{user_id}_model.joblib"

        return file_path


    def deconstruct_user_model_file_path(self, file_path:str) -> list[str]:
        """
        This method is responsible for deconstructing the file_path to get the user id.
        It returns a list with the second element[1] as the user id

        """
        result = str(file_path).split("_")
        return result


    def clean_up(self):
        """
        This method delete the storage_dir and recreate it.
        """

        # deleting the storage directory
        if self.storage_dir.exists():
            shutil.rmtree(self.storage_dir)

        # creating the storage directory
        self.storage_dir.mkdir()

    
    def get_storage_dir_files(self):
        """
        This method get the file path of all the files in the storage dir.
        """
        path = self.storage_dir

        joblib_files = [f.name for f in path.glob("*.joblib")]

        return joblib_files
    
    
    def get_all_user_id_from_path(self):
        """
        This method get all the user id from the files in the storage dir
        """

        file_paths = self.get_storage_dir_files()

        user_id_list = []

        for path in file_paths:
            # transforming the content of path to a list
            path_list = self.deconstruct_user_model_file_path(path)

            # appending the user id
            user_id_list.append(int(path_list[1]))

        return sorted(user_id_list)
    

    def create_dummy_files(self):
        """
        Just for testing purpose
        """
        for i in range(1, 5):
            path = Path(f"{self.storage_dir}/user_{i}_model.joblib")
            print(path)
            path.write_text("lollu")

# eng = ModelStorageEngine()

# eng.clean_up()