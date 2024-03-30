import tensorflow as tf
from webnode.ui import display_output

class DisplayManager:
    @staticmethod
    def send_output(output):
        display_output(output)