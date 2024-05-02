import logbook
from logbook.queues import ZeroMQSubscriber
import zmq

def setup_log_server(log_filename):
    logbook.set_datetime_format("local")
    log_handler = logbook.FileHandler(log_filename)
    log_handler.push_application()

    # Setting up a ZeroMQ subscriber
    # subscriber = ZeroMQSubscriber('tcp://127.0.0.1:5555')  # Bind to port 5555
    # subscriber.socket.bind(subscriber.uri)  # Use bind, not connect
    # context = zmq.Context()
    print("before ZeroMQSubscriber")
    uri = 'tcp://127.0.0.1:5556'
    subscriber = ZeroMQSubscriber(uri)
    # subscriber.socket.bind(uri)
    print("after bind")
    
    while True:
        print("inside while loop, before recv")
        try:
            print("nibba rohit")
            record = subscriber.recv()
            print(record)
            log_handler.handle(record)
            print("handled record")
        except zmq.error.ZMQError as e:
            print("ZeroMQ error:", e)
        

if __name__ == "__main__":
    setup_log_server("central_log.log")
