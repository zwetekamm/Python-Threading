import http.client, urllib.request, urllib.parse, urllib.error, base64
import threading
import json
import os
import time
import timeit

api_key = input('Enter Bing Image Search API key: ')
query = input('Enter a search term: ')
count = input('Enter number of results to download: ')
path = input('Choose a folder path (append with "/"): ')
path_threading = path + '/threading/'
path_not_threading = path + '/not-threading/'

headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': api_key,
}

params = urllib.parse.urlencode({
    # Request parameters
    'q': query,
    'count': count,
    'offset': 0,
    'mkt': 'en-us',
    'safeSearch': 'Moderate',
})

def verify_path(path):
	if not os.path.exists(path):
		os.makedirs(path)

verify_path(path)
verify_path(path_threading)
verify_path(path_not_threading)

def download(url, path, file_name):
	full_path = path + str(file_name) + '.jpg'
	urllib.request.urlretrieve(url, full_path)

def process(path):
	try:
		conn = http.client.HTTPSConnection('api.cognitive.microsoft.com')
		conn.request("GET", "/bing/v7.0/images/search?%s" % params, "{body}", headers)
		response = conn.getresponse()
		data = response.read()
		parsed = json.loads(data)

		file_name = 1
		
		# Use the image url for each search value and download. Filename is incremented integer.
		for item in parsed['value']:
			download(item['contentUrl'], path, file_name)
			file_name += 1
			
		conn.close()
	except Exception as e:
		print("[Errno {0}] {1}".format(e.errno, e.strerror))

def test_not_threading():
	process(path_not_threading)
	process(path_not_threading)
	process(path_not_threading)

def test_threading():
	t1 = threading.Thread(target=process, args=(path_threading,))
	t2 = threading.Thread(target=process, args=(path_threading,))
	t3 = threading.Thread(target=process, args=(path_threading,))

	t1.start()
	t2.start()
	t3.start()

	t1.join()
	t2.join()
	t3.join()

if __name__ == '__main__':
	print("--Run Time--")
	print("Not Threaded: %0.2fs"%(timeit.timeit(test_not_threading,number=1),))
	print("Threaded: %0.2fs"%(timeit.timeit(test_threading,number=1),))