from flask import Flask, render_template, request
from requests import get
from json import loads
from datetime import datetime as dt
import re

app = Flask(__name__)

def clean_html(html):
	cleaned = re.sub(r"(?is)<(script|style).*?>.*?(</\1>)", "", html.strip())
	cleaned = re.sub(r"(?s)<!--(.*?)-->[\n]?", "", cleaned)
	cleaned = re.sub(r"(?s)<.*?>", " ", cleaned)
	cleaned = re.sub(r"&nbsp;", " ", cleaned)
	cleaned = re.sub(r"  ", " ", cleaned)
	cleaned = re.sub(r"  ", " ", cleaned)
	cleaned = re.sub(r"[,.;:]", " ", cleaned)
	return cleaned.strip()

@app.route('/', methods=['POST', 'GET'])
def results():
    if request.method == "GET":
        return render_template('index.html')

    if request.method == "POST":
    	url = request.form["url"]
    	string = request.form["string"]
    	
    	if not url.startswith("http://"):
    		url = "http://%s" % (url)	
	try:    
	    t_total = None
	    t_start = dt.now()
	    try:
	    	r = get(url, timeout=5.0)
	    except Timeout:
	    	return render_template('timeout.html')
	    t_fin = dt.now()
	    t_total = t_fin - t_start 
	    t_total = t_total.total_seconds()*1000.0
	    
	    word_count = 0
	    query_string = string.lower()
	    wordlist = [word.lower() for word in clean_html(r.content).split(" ")]
	    for word in wordlist:
	    	if word == query_string:
	    		word_count += 1

	    return render_template('result.html', string=string, url=url, t_total=t_total ,word_count=word_count)
	
	except:
		return render_template('error.html', url=url)


#To lauch the test-server, use 'foreman start' instead.
#if __name__ == '__main__':
#	app.run(debug=True)