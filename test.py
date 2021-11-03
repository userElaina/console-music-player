import os
import sys

import muz

pth='./'
if len(sys.argv)>1:
	pth=sys.argv[1]
	if not os.path.isdir(pth):
		print('The system cannot find the path specified.')
		sys.exit(0)

muz.Muz(pth,'cycle',log=os.path.join(os.path.dirname(__file__),'muz.log')).join()

# python test.py /all/sakura/music/
