import os
script = """
from priority_classes.ssw.ssw import SswRequest


class #1(SswRequest):
    def __init__(self):
        super().__init__()


if __name__ == '__main__':
    with #1() as ssw:
        ssw.init_browser()
        ssw.login()
        ssw.#2()
"""
# with open('ssw.py','r') as f:
#     for row in f.readlines():
#         if 'def op' in row and not '_' in row:
#             op = row.split()[1].split('(')[0]
#             filename = op.replace('op', 'ssw')
#             file_ = filename + '.py'
#             with open(file_,'w') as n:
#                 n_script = script.replace('#1',filename.capitalize()).replace('#2',op)
#                 n.write(n_script)
with open('ssw_model.py', 'w') as n:
    n_script = script.replace('#1', 'Ssw_').replace('#2', 'op_')
    n.write(n_script)