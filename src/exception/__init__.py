import sys 
import logging


def error_message_detail(error: Exception, error_detail:sys) -> str:

    """
    Extracts detailed error information including file name, line number, and the error message,

    :param error: the exception that occured.
    :param error_detail: The sys module to access traceback details.
    :return: A formatted error message string.
    """

    # Extract traceback details (exception information)
    _, _, exc_tb = error_detail.exc_info()

    # Get the file name where the exception occured
    file_name = exc_tb.tb_frame.f_code.co_filename


    # create a formatted error message string with file name, line number, and actual error
    line_number = exc_tb.tb_lineno

    error_message = f"Error occured in python script: [{file_name}] at line number [{line_number}]: {str(error)}"

    logging.error(error_message)

    return error_message


class MyException(Exception):

    """
    Custom exception calss for handling errror in the us visa application.

    """

    def __init__(self, error_message:str, error_detail:sys):
        """
        Initializes the USvisaException with a detialed error message.

        :param error_message: A string describing the error.
        :param error_detail: The sys module to access trackback details.
        """

        # Call the class constructor with the error message 
        super().__init__(error_message)

        self.error_message = error_message_detail(error_message, error_detail)

    def __str__(self) -> str:
        """
        Return the string representation of the error message.
        """

        return self.error_message