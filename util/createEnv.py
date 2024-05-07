import venv
import os

def create_env_and_install(requirements_path, app_name):
    """
    Creates a Python environment named app_name and installs requirements from the given file path.

    Args:
        requirements_path (str): Path to the requirements.txt file.
    """
    env_name = app_name
    env_dir = os.path.join(os.getcwd(), env_name)

    # Create virtual environment
    env = venv.create(env_dir)

    # Activate virtual environment (modify for your OS if needed)
    activate_this = os.path.join(env_dir, 'bin', 'activate')
    with open(activate_this) as file:
        exec(file.read(), {'__file__': activate_this})

    # Install requirements
    install_command = f"pip install -r {requirements_path}"
    os.system(install_command)

    print(f"Python environment '{env_name}' created and activated.")
    print(f"Requirements installed from '{requirements_path}'.")