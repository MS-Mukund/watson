# handles ML workflow execution
import os 
import sys

import tensorflow as tf
from WorkflowEngine import workflow


# Load the workflow configuration
workflow_config = workflow.load_workflow_config()

# Load the workflow
workflow = workflow.load_workflow(workflow_config)


# Execute the workflow
status = workflow.execute_workflow()

# exit with the status
sys.exit(status)


