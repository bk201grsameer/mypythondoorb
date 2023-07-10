import sys
import os

# Get the absolute path of the project's root directory
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

print(project_root)
# Add the project root to the Python module search path
