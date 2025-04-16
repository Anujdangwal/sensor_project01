import sys


def error_message_detail(error,error_detail: sys):
    _,_,exc_tb=error_detail.exc_info()

    file_name = exc_tb.tb_frame.f_code.cp_filename

    error_message = "Error occured python script name {0} line number [{1}] error message [{2}]".format(
        file_name,exc_tb.tb_lineno,str(error)
    )

    return error_message








class Custom_exception(Exception):
    def __init__(self,error_message, error_details: sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(
            error_message,error_detail = error_message_detail
        )

    
    def __str__(self):
        self.error_message