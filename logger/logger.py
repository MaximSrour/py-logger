"""
A logger
"""

import sys
import os
import datetime
import re
import inspect
from colors import color

class Logger:
    """
    A logger
    """

    LOG_FILE_NAME = None

    WHITE = 15
    PURPLE = 93
    ORANGE = 166
    LIGHT_RED = 160
    BLUE = 21
    GREEN = 28
    LIGHT_BLUE = 26
    LIGHT_CYAN = 39

    END_CHAR = "\033[0m"

    ANSI_ESCAPE = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

    DEPTH = 2

    def init() -> str:
        """
        Create a new log file

        @returns {str} - The name of the log file
        """

        if not os.path.exists("./.logs"):
            os.makedirs("./.logs")

        now = datetime.datetime.now()

        Logger.LOG_FILE_NAME = f"./.logs/LOG_{now.date().strftime('%Y%m%d')}-{now.time().strftime('%H%M%S')}.log"
        return Logger.LOG_FILE_NAME

    def use_last_log_file() -> str:
        """
        Find the last log file in the .log directory

        @returns {str} - The name of the last log file
        """

        if not os.path.exists("./.logs"):
            return None

        files = os.listdir("./.logs")

        log_files = [file for file in files if file.startswith("LOG_")]

        if len(log_files) == 0:
            return None

        log_files.sort()

        Logger.LOG_FILE_NAME = "./.logs/" + log_files[-1]
        return Logger.LOG_FILE_NAME
    
    def get_scope() -> str:
        """
        Get the name of the function that called this function

        @returns {str} - The name of the function that called this function
        """

        caller = inspect.stack()[Logger.DEPTH][3] + "()"
        try:
            scope = inspect.stack()[Logger.DEPTH][0].f_locals["self"].__class__.__name__

        except Exception as e:
            scope = inspect.stack()[Logger.DEPTH][1].split("/")[-1].split(".")[0]

        return Logger.color_text(scope + "." + caller, Logger.GREEN) + ": "

    def color_text(message: str, fg_color_option: int = None, bg_color_option: int = None) -> str:
        """
        Color a string

        @param {str} message - The message to color
        @param {str} color - The color to color the message in
        @returns {str} - The colored message
        """

        assert type(fg_color_option) == int or fg_color_option == None, "fg_color_option must be an int or None"
        assert type(fg_color_option) == int or fg_color_option == None, "bg_color_option must be an int or None"

        if fg_color_option == None:
            return message
        else:
            if bg_color_option == None:
                return color(message, fg=fg_color_option)
            else:
                return color(message, fg=fg_color_option, bg=bg_color_option)

    def log(message: str, target_output = sys.stdout, suppress_log = False) -> None:
        """
        Log a message

        @param {str} message - The message to log
        """

        if target_output != None:
            try:
                print(message, file=target_output)
            except Exception as e:
                Logger.log_error(f"Unable to print to {target_output} - {e}")

        if not suppress_log:
            if Logger.LOG_FILE_NAME == None:
                Logger.use_last_log_file()

            now = datetime.datetime.now()
            message = f"[{now.date().strftime('%Y/%m/%d')}-{now.time().strftime('%H:%M:%S.%f')}] {message}"

            with open(Logger.LOG_FILE_NAME, "a") as log_file:
                print(Logger.ANSI_ESCAPE.sub('', message), file=log_file)
    
    def log_header(message: str, suppress_log = False) -> None:
        """
        Log a header

        @param {str} header - The header to log
        """

        Logger.log(Logger.color_text(message, Logger.PURPLE), sys.stdout, suppress_log)

    def log_info(message: str, suppress_log = False) -> None:
        """
        Log an info message

        @param {str} info - The info message to log
        """

        Logger.log(Logger.color_text("INFO", Logger.LIGHT_BLUE) + ": " + Logger.get_scope() + message, sys.stdout, suppress_log)
    
    def log_warning(message: str, suppress_log = False) -> None:
        """
        Log a warning

        @param {str} warning - The warning to log
        """

        Logger.log(Logger.color_text("WARNING", Logger.ORANGE) + ": " + Logger.get_scope() + message, sys.stderr, suppress_log)
    
    def log_error(message: str, suppress_log = False) -> None:
        """
        Log an error

        @param {str} error - The error to log
        """

        Logger.log(Logger.color_text("ERROR", Logger.LIGHT_RED) + ": " + Logger.get_scope() + message, sys.stderr, suppress_log)

    def log_critical(message: str, suppress_log = False) -> None:
        """
        Log a critical error

        @param {str} error - The error to log
        """

        Logger.log(Logger.color_text("CRITICAL", Logger.WHITE, Logger.LIGHT_RED) + ": " + Logger.get_scope() + message, sys.stderr, suppress_log)

    def log_debug(message: str, suppress_stdout = True, suppress_log = False) -> None:
        """
        Log a debug message

        @param {str} debug - The debug message to log
        """

        file = None
        if not suppress_stdout:
            file = sys.stdout

        Logger.log(Logger.color_text("DEBUG", Logger.WHITE, Logger.LIGHT_BLUE) + ": " + Logger.get_scope() + message, file, suppress_log)
    
    def log_test(test_name: str, suppress_log = False) -> None:
        """
        Log a test being run

        @param {str} test_name - The name of the test
        """

        Logger.log("Running test: " + Logger.color_text(test_name, Logger.LIGHT_BLUE), sys.stdout, suppress_log)
    
    def log_subtest(subtest_name: str, suppress_log = False) -> None:
        """
        Log a test being run

        @param {str} test_name - The name of the test
        """

        Logger.log("Testing: " + Logger.color_text(subtest_name, Logger.LIGHT_CYAN), sys.stdout, suppress_log)

def main():
    Logger.init()
    Logger.log_header("Running Logger program")

    Logger.log_info("This is an info message")
    Logger.log_warning("This is a warning message")
    Logger.log_error("This is an error message")
    Logger.log_critical("This is a critical message")

    Logger.log_debug("This is a suppressed debug message")
    Logger.log_debug("This is a non-suppressed debug message", suppress_stdout=False)

    Logger.log_test("This is a test")
    Logger.log_subtest("This is a subtest")

    Logger.log("This is a normal message")

if __name__ == "__main__":
    main()