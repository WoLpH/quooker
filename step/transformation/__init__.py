import os
import sys

'Generate the proper prefix to import the transformations'
prefix = [__name__, None]

'import all .py files'
for file in os.listdir(os.path.dirname(__file__)):
    if file and file[0] not in ('.', '_'):
        if file.endswith('.py'):
            prefix[-1] = file[:-3]
            __import__('.'.join(prefix))
        elif (os.path.isdir(file) and
                os.path.isfile(os.path.join(file, '__init__.py'))):
            prefix[-1] = file
            __import__('.'.join(prefix))
