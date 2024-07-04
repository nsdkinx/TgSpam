# -*- coding: utf-8 -*-

def format_exception(e: BaseException):
    import traceback
    # Get the traceback information
    traceback_info = traceback.extract_tb(e.__traceback__)

    # Print the exception message
    print("Exception in:")

    # Iterate over each traceback item
    for item in traceback_info:
        filename = item.filename
        line_number = item.lineno
        print(f'File "{filename}", line {line_number}')

    # Print the original exception message
    print(type(e).__name__ + ":", e)
