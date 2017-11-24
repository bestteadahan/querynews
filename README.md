# querynews

<h3>01. ETL: Crawler News Article from New York Times</h3>
<li>crawler.py: Excute to start. could add additional module in the future.</li>
<li>getNTY.py: Crawler article url/content and insert to mongodb.</li>

<h3>02. DataProcessing: Calculating TF-IDF and find top 10 keywords each article</h3>
<li>stop-word-list.txt: English stop-word list from nltk.</li>
<li>modify_quotation.py: Remove punctuation and article with empty content.</li>
<li>calculateTFnWC.py: Word count and TF per article.</li>
<li>calculateTFIDFnKW.py: Calculate TF-IDF within whole database articles.</li>

<h3>03. Analyze: Decide Article Level</h3>
<li>vocabulary_list_new.csv: 6 levels of English vocabulary which are defined by Taiwan Education Institude.</li>
<li>add_leveltag.py: Decide article level by mapping top 10 keywords with vocabulary_list_new.csv.</li>

<h3>04. Web: Try it!</h3>
> npm install
> npm start
(listen on localhost:8000/query)
