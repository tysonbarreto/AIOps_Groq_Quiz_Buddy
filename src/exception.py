import sys

class AIException(Exception):
    def __init__(self, message:str, error_detail:sys):
        self.error_message = self.get_error_message(message, error_detail)
        super().__init__(self.error_message)
    
    def __str__(self):
        return self.error_message
    
    @staticmethod
    def get_error_message(message:str, error_detail:sys):
        _, _, exec_tb = sys.exc_info()
        file_name = exec_tb.tb_frame.f_code.co_filename if exec_tb else "Unknown File"
        line_number = exec_tb.tb_lineno if exec_tb else "Unknown File"
        return f"{message} | Error: {error_detail} | File: {file_name} | Line: {line_number}"
    
if __name__=="__main__":
    __all__=["AIException"]