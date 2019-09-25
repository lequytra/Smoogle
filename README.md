

![Smoogle logo](https://github.com/lequytra/Search-Engine/blob/master/Smoogle%20logo.png](https://github.com/lequytra/Search-Engine/blob/master/Smoogle.png)

### Set Up Environment:
To create an environment with the environment.yml file, navigate to the folder containing the environment file and type ```conda env create -f environment.yml``` into your terminal. To activate your environment, do ```conda activate env-name```. The environment in the yml file is named ```IR```. 

> **Dependency**
>
> ```sys```  ```os```  ```pickle```   ```csv```
>
> ```random```  ```re```
>
> ```urllib```   ```validators```  ```requests```  ```http.client```  ```BeautifulSoup```  

### Supporting Classes:

1. ##### Graph.py

   ```class Graph``` is used for constructing web graph object that is used for calculating PageRank

2. ##### BIR.py

   ```class Doc``` stores information about the document after tf-idf  (term frequency-inverse document frequency)

   - ```doc_id```: id of document
   - ```term_freq```: frequency of term in the document
   - ```most_common```:maximum frequency in the document

   ```class BIR``` creates 2D ```numpy``` array with (term, ```Doc```) pair for every terms in the document lists

3. ##### Conversion.py

   ```class Conversion``` builds expression Tree to process query

4. ##### PageRank.py

   ```class PageRank``` updates the weight of given ```Graph``` based on the PageRank algorithm

5. ##### text_processing_utils.py

   ```extract_keywords(query, stem=True, return_score=False)``` is used for extracting keywords from given query

### Scraping Web:

1. ##### WebCrawler.py

   This program scrapes web pages starting from given seed url and its hyperlinks in the content and builds web graph while scraping 

   Output: 

   /Contents		

   - Contents of each crawled web pages in ```.txt``` format

   /Data

   - ```need_to_crawl.csv```: web pages added to graph but not crawled yet
   - ```id_url.csv``` and ```url_id.csv```: dictionary of web pages that is in the graph
   - ```c_id_url.csv``` and ```c_url_id.csv```: dictionary of web pages that is crawled
   - ```graph.p```: web graph storing ```Graph``` object

2. ##### setup.py

   This program updates ```graph.p``` by calculating the PageRank and save tf-idf table from contents of crawled web pages

### Search Engine Execution:

##### Session.py

This program searches list of relevant web pages to the user query based on tf-idf inverted index and web graph.

##### main.py

Type ```python main.py``` into the terminal to run the search machine

The program allows the user to choose from 3 options (**s**, **a**, **q**)

- **s**: search
- **a**: advance search
  - ```AND``` ```NOT``` ``OR`` keywords to search more accurately
- **q**: quit the search machine

If the user selects search or advanced search, the program asks you to type query.



