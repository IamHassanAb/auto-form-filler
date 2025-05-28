from pds.QuestionDS import QuestionDS
from pds.RequestDS import RequestDS
from pds.ResponseDS import ResponseDS


class Context:
    """
    Context object to store and manage the state of the form filling session.
    """

    def __init__(self):
        self.fields = None
        self.QuestionDS = QuestionDS
        self.RequestDS = RequestDS
        self.ResponseDS = ResponseDS
    
    def set_field(self, field: list):
        """
        Set the fields for the context.
        
        :param field: List of RequestDS objects representing the form fields.
        """
        if isinstance(field, list) and all(isinstance(f, RequestDS) for f in field):
            self.fields = field
        else:
            raise ValueError("Fields must be a list of RequestDS objects.")
        
    def get_fields(self):
        """
        Get the fields from the context.
        
        :return: List of RequestDS objects representing the form fields.
        """
        if self.fields is None:
            raise ValueError("Fields have not been set in the context.")
        return self.fields
    
    def get_question_ds(self):
        """
        Get the QuestionDS class from the context.
        
        :return: QuestionDS class.
        """
        return self.QuestionDS
    
    def get_request_ds(self):
        """
        Get the RequestDS class from the context.
        
        :return: RequestDS class.
        """
        return self.RequestDS
    
    def get_response_ds(self):
        """
        Get the ResponseDS class from the context.
        
        :return: ResponseDS class.
        """
        return self.ResponseDS
    
    def __repr__(self):
        return f"Context(fields={self.fields})"
    

