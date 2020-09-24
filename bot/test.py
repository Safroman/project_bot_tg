import re

var = 'notify_all ,kf,kf ,kf,dfnvs'
req = re.split(r' ', var, maxsplit=1)
print(req)