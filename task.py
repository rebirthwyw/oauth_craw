from craw.Crystal import Crystal
from model import OauthCraw
import traceback


oc = OauthCraw()
task = Crystal("oauthCraw", 1)
# task.start_single(["https://linux.cn"])
while True:
	url = oc.selectUrl()
	if url == False:
		break
	try:
		task.start_single(["https://" + url])
	except Exception,e:
		print traceback.format_exc()
	oc.deleteUrl()
