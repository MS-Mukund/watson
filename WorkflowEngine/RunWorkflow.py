# handles ML workflow execution
import os 
import sys

import tensorflow as tf
from WorkflowEngine import workflow

# Load the workflow configuration - read from .config file
read_config = open('path/to/workflow/config', 'r')
workflow_config = read_config.read()

# Load the workflow
wf = workflow()
wf.load_workflow(workflow_config)

# Execute the workflow
status = wf.execute_workflow()

# exit with the status
sys.exit(status)
