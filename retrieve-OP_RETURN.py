# retrieve-OP_RETURN.py
# 
# CLI wrapper for OP_RETURN.py to retrieve data from OP_RETURNs
#
# Copyright (c) Coin Sciences Ltd
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


import sys, string
from OP_RETURN import *


if len(sys.argv)<2:
	sys.exit(
'''Usage:
python retrieve-OP_RETURN.py <txid> <testnet (optional)>'''
	)

txid=sys.argv[1]

if len(sys.argv)>2:
	testnet=bool(sys.argv[2])
else:
	testnet=False

datas = OP_RETURN_get_asms(txid, testnet)
for data in datas:
	print(data)
