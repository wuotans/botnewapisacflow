import logging
from datetime import datetime
try:
    from src import flow
    flow.main()
except Exception as e:
    logging.exception(e)
    with open('logExceptions.txt', 'a') as f:
        f.write(f"\nError[{str(datetime.now())}]: " + str(e))
