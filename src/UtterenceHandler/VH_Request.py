import VH_Enums
from typing import Any, Dict, Optional

class VH_request:
    def __init__(self, text: str, NER_Dict: Dict[str, Any], values_dict: Dict[str, Any]) -> None:
        """
        Initialize a VH_request instance with attributes based on the NER_Dict.

        Args:
            text (str): The text input (not used in the current implementation).
            NER_Dict (Dict[str, Any]): A dictionary containing keys and values for various NER categories.
            values_dict (Dict[str, Any]): A dictionary containing values.
        """
        ner_keys = ['thing', 'attribute', 'location', 'state', 'action']
        for key in ner_keys:
            setattr(self, key, NER_Dict.get(key, [None])[0])

        self.input = text
        self.value = NER_Dict.get(0,None) #TODO
        self.value_type  = NER_Dict.get(1,None)
        
        # Initialize an empty description
        self.description : str = ""

        # Tokenize the input text using split
        tokens = text.split(' ')

        # Check if each token is not in the NER entities, value, or value type
        for token in tokens:
            if (token not in NER_Dict.values() and
                    token not in values_dict.values() and
                    token != self.value and
                    token != self.value_type):
                self.description += token + " "

        # Remove the trailing whitespace
        self.description = self.description.strip()

    def __str__(self) -> str:
        """
        Provide a string representation of the VH_request instance.

        Returns:
            str: A string representation of the instance.
        """
        return f"Thing: {self.thing}, Attribute: {self.attribute}, Location: {self.location}, Value: {self.value}, Action: {self.action}"
