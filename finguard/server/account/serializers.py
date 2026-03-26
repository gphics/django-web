from rest_framework import serializers
from django.contrib.auth import get_user_model
from . models import Profile
from rapidfuzz import process as text_processor, fuzz
from babel.numbers import get_currency_symbol

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """"
    This serializer is for the creation of the user only
    """
   
    class Meta:
        model = User
        fields = "__all__"
        # fields = ["password", "username"]
        extra_kwargs = {
            "password":{"write_only":True}
        }

    def validate_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError("Password length must be greater than 5")
        return value
        
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class ProfileSerializer(serializers.ModelSerializer):
    """
    This serializer is for the creation and listing of profiles
    """
    user = UserSerializer(read_only = True)
    class Meta:
        model = Profile
        fields =  "__all__"

    def validate_city(self, value):
        """
        The purpose of this validator is to ensure uniqueness of the city and prevent having the same city with different but similar spellings as it would be used for data explorations.
        """
        # transforming the value to  title case
        city = str(value).title()

        # getting all cities
        unique_city = Profile.objects.values_list("city", flat=True).distinct()

        # if no city have been saved to the db
        if len(unique_city) == 0:
            return city
        
        # looking for best match with a threshold score of 80
        result= text_processor.extractOne(query=city, choices=unique_city, scorer=fuzz.token_sort_ratio, score_cutoff=80)

        # if best match exist
        if result:
            city, *rest = result
            return city
        
        # since best match does not exist, the city is regarded as a new city, hence returned
        return city
    

    def validate_state(self, value):
        """
        The purpose of this validator is to ensure uniqueness of the state and prevent having the same state with different but similar spellings as it would be used for data explorations.
        """
        # transforming the value to title case
        state = str(value).title()

        # getting all states
        unique_states = Profile.objects.values_list("state", flat=True).distinct()

        # if no state have been saved to the db
        if len(unique_states) == 0:
            return state
        
        # looking for best match with a threshold score of 80
        result= text_processor.extractOne(query=state, choices=unique_states, scorer=fuzz.token_sort_ratio, score_cutoff=80)

        # if best match exist
        if result:
            state, *rest = result
            return state
        
        # since best match does not exist, the state is regarded as a new state, hence returned
        return state
    

    def validate_country(self, value):
        """
        The purpose of this validator is to ensure uniqueness of the country and prevent having the same country with different but similar spellings as it would be used for data explorations.
        """
        # transforming the value to title case
        country = str(value).title()

        # getting all countries
        unique_country = Profile.objects.values_list("country", flat=True).distinct()

        # if no state have been saved to the db
        if len(unique_country) == 0:
            return country
        
        # looking for best match with a threshold score of 80
        result= text_processor.extractOne(query=country, choices=unique_country, scorer=fuzz.token_sort_ratio, score_cutoff=80)

        # if best match exist
        if result:
            country, *rest = result
            return country
        
        # since best match does not exist, the country is regarded as a new country, hence returned
        return country

    def validate_currency(self, value):
        """
        This method is for validating the currency field. If the provided currency code exist, it's currency symbol is returned for saving into the db field.
        """

        currency_code = value

        # getting currency symbol
        currency_symbol = get_currency_symbol(currency_code)

        if currency_code == "XYZ":
            # raising error
            raise serializers.ValidationError(f"Currency code '{currency_code}' is invalid")
        else:

            # returning appropriate currency symbol
            return currency_symbol

     