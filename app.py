from __future__ import unicode_literals
from flask import Flask,render_template,url_for,request

from spacy_summarization import text_summarizer
from gensim.summarization import summarize
from nltk_summarization import nltk_summarizer
import time
import re
import spacy
nlp = spacy.load('en_core_web_sm')
app = Flask(__name__)

# Web Scraping Pkg
from bs4 import BeautifulSoup
# from urllib.request import urlopen
from urllib.request import urlopen,Request

# Sumy Pkg
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

# Sumy 
def sumy_summary(docx):
	parser = PlaintextParser.from_string(docx,Tokenizer("english"))
	lex_summarizer = LexRankSummarizer()
	summary = lex_summarizer(parser.document,3)
	summary_list = [str(sentence) for sentence in summary]
	result = ' '.join(summary_list)
	return result


# Reading Time
def readingTime(mytext):
	total_words = len([ token.text for token in nlp(mytext)])
	estimatedTime = total_words/200.0
	return estimatedTime

# Fetch Text From Url
def get_text(url):
	page = urlopen(url)
	soup = BeautifulSoup(page)
	fetched_text = ' '.join(map(lambda p:p.text,soup.find_all('p')))
	return fetched_text

@app.route('/')
def about():
	return render_template('about.html')


@app.route('/analyze',methods=['GET','POST'])
def analyze():
	start = time.time()
	if request.method == 'POST':
		rawtext = request.form['rawtext']
		final_reading_time = readingTime(rawtext)
		final_summary = text_summarizer(rawtext)
		summary_reading_time = readingTime(final_summary)
		end = time.time()
		final_time = end-start
	return render_template('index.html',ctext=rawtext,final_summary=final_summary,final_time=final_time,final_reading_time=final_reading_time,summary_reading_time=summary_reading_time)

@app.route('/analyze_url',methods=['GET','POST'])
def analyze_url():
	start = time.time()
	if request.method == 'POST':
		raw_url = request.form['raw_url']
		rawtext = get_text(raw_url)
		final_reading_time = readingTime(rawtext)
		final_summary = text_summarizer(rawtext)
		summary_reading_time = readingTime(final_summary)
		end = time.time()
		final_time = end-start
	return render_template('index.html',ctext=rawtext,final_summary=final_summary,final_time=final_time,final_reading_time=final_reading_time,summary_reading_time=summary_reading_time)



@app.route('/compare_summary')
def compare_summary():
	return render_template('compare_summary.html')

@app.route('/comparer',methods=['GET','POST'])
def comparer():
	start = time.time()
	if request.method == 'POST':
		rawtext = request.form['rawtext']
		final_reading_time = readingTime(rawtext)
		final_summary_spacy = text_summarizer(rawtext)
		summary_reading_time = readingTime(final_summary_spacy)
		# Gensim Summarizer
		final_summary_gensim = summarize(rawtext)
		summary_reading_time_gensim = readingTime(final_summary_gensim)
		# NLTK
		final_summary_nltk = nltk_summarizer(rawtext)
		summary_reading_time_nltk = readingTime(final_summary_nltk)
		# Sumy
		final_summary_sumy = sumy_summary(rawtext)
		summary_reading_time_sumy = readingTime(final_summary_sumy) 

		end = time.time()
		final_time = end-start
	return render_template('compare_summary.html',ctext=rawtext,final_summary_spacy=final_summary_spacy,final_summary_gensim=final_summary_gensim,final_summary_nltk=final_summary_nltk,final_time=final_time,final_reading_time=final_reading_time,summary_reading_time=summary_reading_time,summary_reading_time_gensim=summary_reading_time_gensim,final_summary_sumy=final_summary_sumy,summary_reading_time_sumy=summary_reading_time_sumy,summary_reading_time_nltk=summary_reading_time_nltk)



@app.route('/index')
def index():
	return render_template('index.html')


# web scraping part

def get_h1(url):
	req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	source = urlopen(req).read()
	soup = BeautifulSoup(source,'lxml')
	
	fetch_h1 = ' '.join(map(lambda h1:h1.text,soup.find_all('h1')))
	
	return fetch_h1

def get_h2(url):
	req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	source = urlopen(req).read()
	soup = BeautifulSoup(source,'lxml')
	
	
	fetch_h2 = ' '.join(map(lambda h2:h2.text,soup.find_all('h2')))

	return fetch_h2
def get_links(url):
	req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	source = urlopen(req).read()
	soup = BeautifulSoup(source,'lxml')
	
	
	fetch_links = ' '.join(map(lambda links:links.text,soup.find_all('a', attrs={'href': re.compile("^http://")})))
	
	return fetch_links

def get_meta(url):
	req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	source = urlopen(req).read()
	soup = BeautifulSoup(source,'lxml')
	content = []

	for tags in soup.find_all('meta'):
		content = tags.get('content')
	
	return content

def get_meta1(url):
	req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	source = urlopen(req).read()
	soup = BeautifulSoup(source,'lxml')
	content1 = []
	
	for tags in soup.find_all('meta'):
		content1 = tags.get('name')
					
	return content1

def get_p(url):
	req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	source = urlopen(req).read()
	soup = BeautifulSoup(source,'lxml')
	
	
	fetch_p = ' '.join(map(lambda p:p.text,soup.find_all('p')))
	
	return fetch_p

def get_title(url):
	req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	source = urlopen(req).read()
	soup = BeautifulSoup(source,'lxml')
	
	
	fetch_title = ' '.join(map(lambda p:p.text,soup.find_all('title')))
	return fetch_title

def get_tables(url):
	req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	source = urlopen(req).read()
	soup = BeautifulSoup(source,'lxml')
	fetch_tables = ' '.join(map(lambda p:p.text,soup.find_all('table')))
	return fetch_tables

def get_bold(url):
	req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	source = urlopen(req).read()
	soup = BeautifulSoup(source,'lxml')
	fetch_bold = ' '.join(map(lambda p:p.text,soup.find_all('b')))

	return fetch_bold


def get_italics(url):
	req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	source = urlopen(req).read()
	soup = BeautifulSoup(source,'lxml')
	fetch_italics = ' '.join(map(lambda p:p.text,soup.find_all('i')))

	return fetch_italics

def get_underline(url):
	req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	source = urlopen(req).read()
	soup = BeautifulSoup(source,'lxml')
	fetch_underline = ' '.join(map(lambda p:p.text,soup.find_all('u')))

	return fetch_underline

@app.route('/test')
def test():
	return render_template('test.html')

@app.route('/web_scrap',methods=['GET','POST'])
def web_scrap():
	if request.method == 'POST':
		raw_url = request.form['raw_url']
		rawh1 = get_h1(raw_url)
		rawh2 = get_h2(raw_url)
		rawlinks = get_links(raw_url)
		rawmeta = get_meta(raw_url)
		rawmeta1 = get_meta1(raw_url)
		rawp = get_p(raw_url)
		rawtitle = get_title(raw_url)
		rawtables = get_tables(raw_url)
		rawbold = get_bold(raw_url)
		rawitalics = get_italics(raw_url)
		rawunderline = get_underline(raw_url)

	return render_template('result.html',len = len(rawmeta),rawbold=rawbold,rawitalics=rawitalics,rawunderline=rawunderline,rawmeta1=rawmeta1,rawtables = rawtables,rawtitle=rawtitle,raw_url=raw_url,rawh1=rawh1,rawh2=rawh2,rawlinks=rawlinks,rawmeta=rawmeta,rawp=rawp)





if __name__ == '__main__':
	app.run(use_reloader = True,debug=True)