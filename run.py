# !/usr/bin/env python
# -------------------------------------------------------------------------------
# run.py
# -------------------------------------------------------------------------------

from studygroup import app
from sys import argv, stderr

if __name__ == '__main__':

    if len(argv) != 2:
        print('Usage: ' + argv[0] + ' port', file=stderr)
        exit(1)

    try:
        port = int(argv[1])
    except:
        print('Port must be an integer', file=stderr)
        exit(1)
    app.run(host='0.0.0.0', port=int(argv[1]), debug=True)

# -------------------------------------------------------------------------------
