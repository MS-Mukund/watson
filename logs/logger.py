import logbook
from logbook.queues import ZeroMQHandler
import zmq

def setup_logger(log_filename):
    logbook.set_datetime_format("local")
    
    # Create a FileHandler to write log messages to a file
    file_handler = logbook.FileHandler(log_filename)
    file_handler.push_application()
    
    # Create a ZeroMQHandler to send log messages to a ZeroMQ socket
    zero_mq_handler = ZeroMQHandler('tcp://127.0.0.1:5555', multi=True)
    zero_mq_handler.push_application()

    # Create a Logger object
    logger = logbook.Logger('AppLogger')
    print("Logger created")
    
    return logger

