# FALL 2021
# SI 206
# Name: Daijour Williams
# Who did you work with:

from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import unittest


def get_titles_from_search_results():
    """
    Write a function that creates a BeautifulSoup object on "search_results.html". Parse
    through the object and return a list of tuples containing book titles, authors, and rating
    (as printed on the Goodreads website) in the format given below. Make sure to strip()
    any newlines from the book titles and author names.

    url = search_results.hmtl
    resp = requests.get(url)
    if resp.ok:
    soup = BeautifulSoup(resp.content, 'html.parser')
    tags = find_all(div class_=u-anchorTarget)
    <span itemprop="name" role="heading" aria-level="4">Harry Potter and the Deathly Hallows (Harry Potter, #7)</span>

    <span itemprop="name">J.K. Rowling</span>

    <span class="minirating"><span class="stars staticStars notranslate"><span size="12x12" class="staticStar p10"></span><span size="12x12" class="staticStar p10"></span><span size="12x12" class="staticStar p10"></span><span size="12x12" class="staticStar p10"></span><span size="12x12" class="staticStar p6"></span></span> 4.62 avg rating — 2,795,923 ratings</span>

    put the list into their own objetcts then iterate through the index to create and place each tuple into the list.
    [('Book title 1', 'Author 1','Rating 1'), ('Book title 2', 'Author 2', 'Rating 2')...]
    """
    with open('search_results.html', 'r') as f:
        contents = f.read()
        soup = BeautifulSoup(contents, 'html.parser')
    nametaglst = soup.find_all('span', itemprop='name', role='heading')
    ratingtaglst = soup.find_all('span',class_='minirating')
    authortaglst = soup.find_all('span', itemprop='name')
    # authortaglst = soup.findChildren('span', itemprop='name')
    lst = []
    authorlst = []
    for tag in authortaglst:
       if len(tag.attrs) == 1:
           authorlst.append(tag.text)

    for indx in range(len(nametaglst)):
        name = nametaglst[indx]
        author = authorlst[indx] 
        rating = ratingtaglst[indx]
        tupl = (name.text,str(author),float(rating.text[1:5]))
        lst.append(tupl)
    # for tag in ratingtaglst:
    #     print(tag.text)
    return lst

def get_search_links():
    """
    Write a function that creates a BeautifulSoup object after retrieving content from
    "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc". Parse through the object and return a list of
    URLs for each of the first ten books in the search using the following format:

    ['https://www.goodreads.com/book/show/84136.Fantasy_Lover?from_search=true&from_srp=true&qid=NwUsLiA2Nc&rank=1', ...]

    Notice that you should ONLY add URLs that start with "/book/show/" to 
    your list, and be sure to append the full path (https://www.goodreads.com) to the URL so that the url is in the format 
    “https://www.goodreads.com/book/show/kdkd".

    <a class="bookTitle" itemprop="url" href="/book/show/84136.Fantasy_Lover?from_search=true&amp;from_srp=true&amp;qid=NwUsLiA2Nc&amp;rank=1">
        <span itemprop="name" role="heading" aria-level="4">Fantasy Lover (Hunter Legends, #1)</span>
</a>
    use soupe to return list, then maybe iterate through soup list with counter to put first ten into a list
    """
    lst = []
    url = "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content,'html.parser')
    tags = soup.find_all('a', class_='bookTitle')
    counter = 0
    for tag in tags:
        resp = tag.get('href',None)
        if resp == None:
            continue
        elif counter == 10:
            #print(lst)
            return lst
        elif '/book/show/' in resp:
            lst.append("https://www.goodreads.com"+resp)
            counter += 1



def get_book_summary(book_html):
    """
    Write a function that creates a BeautifulSoup object that extracts book
    information from a book's webpage, given the HTML file of the book. Parse through
    the BeautifulSoup object, and capture the book title, book author, number of pages, 
    and book rating. This function should return a tuple in the following format:
    
    ('Some book title', 'the book's author', number of pages, book rating)
    
    HINT: Using BeautifulSoup's find() method may help you here.
    You can easily capture CSS selectors with your browser's inspector window.
    Make sure to strip() any newlines from the book title, number of pages, and rating.


    """
    #ask about file direcrtory
    #Ask about author tags, how to get it with just the specified attritbute, not any more, and how to use rgeex
    #with open(book_html, 'r', encoding='utf8') as f:
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), book_html),encoding='utf-8') as f:
        contents = f.read()
        soup = BeautifulSoup(contents, 'html.parser')
    # url = book_html
    # resp = requests.get(url)
    # soup = BeautifulSoup(resp, 'html.parser')
    title = soup.find('h1', id='bookTitle')
    author = soup.find('span', itemprop='name')
    # for tag in authortags:
    #     if len(tag.attrs) == 1:
    #         authors.append(tag.text)
    numpage = soup.find('span', itemprop='numberOfPages')
    rating = soup.find('span', itemprop='ratingValue')
    finltupl = (title.text.strip(), author.text.strip(),int(numpage.text[0:3].strip()),float(rating.text.strip()))
    #print(finltupl)
    return finltupl

def summarize_best_books(filepath):
    """
    Write a function to get a list of categories, book title and URLs from the "BEST 
    BOOKS OF 2021" page in "best_books_2021.html". This function should create a 
    BeautifulSoup object from a filepath and return a list of (category, book title, 
    URL) tuples.
    
    For example, if the best book in category "Fiction" is "The Testaments (The 
    Handmaid's Tale, #2)", with URL
    https://www.goodreads.com/choiceawards/best-fiction-books-2020, then you should 
    append("Fiction", "The Testaments (The Handmaid's Tale, #2)", 
    "https://www.goodreads.com/choiceawards/best-fiction-books-2020")
    to your list of tuples.

    """
    #filepath? so use os?? open the file, open the link, then go to the page
    #with open(os.path.join(os.path.abspath(os.path.dirname(__file__)),'r')) as f:
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), filepath),encoding='utf-8') as f:
        contents = f.read()
        soup = BeautifulSoup(contents, 'html.parser')
    categorylst = soup.find_all('h4', class_='category__copy')
    booktitle =soup.find_all('img', class_='category__winnerImage')
    #urlst = soup.find_all('a', href = "^https")
    urlst = soup.find_all('div',class_='category clearFix')
    newlst = []
    for item in urlst:
        newlst.append(item.find('a'))
    #.get alt for title and .get src for url
    #iterate through index and use .text to put into tuple, 
    returnlst = []
    for indx in range(len(booktitle)):
        title = booktitle[indx].get('alt',None)
        url = newlst[indx].get('href',None)
        category = categorylst[indx].text
        tupl = (category.strip(), title.strip(), url.strip())
        returnlst.append(tupl)
    # print(returnlst)
    return returnlst
        

    


def write_csv(data, filename):
    """
    Write a function that takes in a list of tuples (called data, i.e. the
   one that is returned by get_titles_from_search_results()), sorts the tuples in 
   descending order by largest rating, writes the data to a csv file, and saves it to 
   the passed filename.
   The first row of the csv should contain "Book title", "Author Name", “Rating”, 
   respectively as column headers. For each tuple in data, write a new
   row to the csv, placing each element of the tuple in the correct column.
 
   When you are done your CSV file should look like this:
 
   Book title,Author Name,Rating
   Book1,Author1,Rating1
   Book2,Author2,Rating2
   Book3,Author3,Rating3
   
   In order of highest rating to lowest rating.
 
   This function should not return anything.

    """ #index 2 change rating to index
    header = ('Book title', 'Author Name', 'Rating')
    sortlst = sorted(data, key = lambda x: x[2], reverse = True)

    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for item in sortlst:
            writer.writerow(item)



def extra_credit(filepath):
    """
    EXTRA CREDIT

    Please see the instructions document for more information on how to complete this function.
    You do not have to write test cases for this function.
    """
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), filepath),encoding='utf-8') as f:
        contents = f.read()
        soup = BeautifulSoup(contents, 'html.parser')
    description = soup.find_all('span', id='freeText4791443123668479528')
    reg = "[A-Z][a-z]{2,}\s[A-Z]\w+\s*(?:[A-Z][a-z]+\s)*"
    nmlst = []
    for item in description:
        matchlst = re.findall(reg,item.text)
        if len(matchlst) != 0:
            nmlst += matchlst
    return nmlst
    # return matchlst Exclusion Zone, Soviet Union, United States', Cold War, Reactor No.4, V.I. Lenin Nuclear Power Plant, Adam Higginbotham, Alexander Akimov, Anatoli Dyatlov


class TestCases(unittest.TestCase):

    # call get_search_links() and save it to a static variable: search_urls
    search_urls = get_search_links()


    def test_get_titles_from_search_results(self):
        # call get_titles_from_search_results() and save to a local variable
        titles = get_titles_from_search_results()
        # check that the number of titles extracted is correct (20 titles)
        self.assertEqual(len(titles),20)
        
        # check that the variable you saved after calling the function is a list
        self.assertEqual(isinstance(titles,list),True)
        # check that each item in the list is a tuple

        # check that the first book and author tuple is correct (open search_results.html and find it)
        checkfirst = ('Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling', 4.62)
        self.assertEqual(checkfirst,titles[0])
        # check that the last title is correct (open search_results.html and find it)
        checklast = ('Harry Potter: The Prequel (Harry Potter,#0.5)', 'J.K. Rowling', 4.18)

    def test_get_search_links(self):
        # check that TestCases.search_urls is a list
        self.assertEqual(isinstance(TestCases.search_urls,list),True)
        # check that the length of TestCases.search_urls is correct (10 URLs)
        self.assertEqual(len(TestCases.search_urls),10)

        # check that each URL in the TestCases.search_urls is a string
        for item in TestCases.search_urls:
            self.assertEqual(isinstance(item,str),True)
        # check that each URL contains the correct url for Goodreads.com followed by /book/show/'
        reg = "^https://www.goodreads.com/book/show/\w+"
        pass

    def test_get_book_summary(self):
        # the list of webpages you want to pass in one by one into get_book_summary 
        html_list = ['book_summary_html_files/Fantasy Lover (Hunter Legends, #1) by Sherrilyn Kenyon.html',
                        'book_summary_html_files/Fantasy in Death (In Death, #30) by J.D. Robb.html',
                        'book_summary_html_files/Fantasy of Frost (The Tainted Accords, #1) by Kelly St. Clare.html',
                        'book_summary_html_files/The Mind’s I_ Fantasies and Reflections on Self and Soul by Douglas R. Hofstadter.html',
                        'book_summary_html_files/Gods and Mortals_ Fourteen Free Urban Fantasy & Paranormal Novels Featuring Thor, Loki, Greek Gods, Native American Spirits, Vampires, Werewolves, & More by C. Gockel.html',
                        'book_summary_html_files/Epic_ Legends of Fantasy by John Joseph Adams.html',
                        'book_summary_html_files/The Kingdom of Fantasy by Geronimo Stilton.html',
                        'book_summary_html_files/Kurintor Nyusi_ Diverse Epic Fantasy by Aaron-Michael Hall.html',
                        'book_summary_html_files/Kurintor Nyusi_ Diverse Epic Fantasy by Aaron-Michael Hall.html',
                        'book_summary_html_files/Die, Vol. 1_ Fantasy Heartbreaker by Kieron Gillen.html']
        # check that the number of book summaries is correct (10)
        result = []
        for item in html_list:
            result.append(get_book_summary(item))
        self.assertEqual(len(result),10)
            # check that each item in the list is a tuple
        for item in result:
            self.assertEqual(isinstance(item,tuple),True)
            # check that each tuple has 4 elements
            self.assertEqual(len(item),4)
            # check that the first two elements in the tuple are string
            self.assertEqual(isinstance(item[0],str),True)
            self.assertEqual(isinstance(item[1],str),True)
            # check that the third element in the tuple, i.e. pages is an int
            self.assertEqual(isinstance(item[2],int),True)
            # check that the fourth element in the tuple, i.e. rating is a float
            self.assertEqual(isinstance(item[3],float),True)
        # check that the first book in the search has 337 pages
        self.assertEqual(result[0][2],337)
        # check the last book has 4.02 rating
        self.assertEqual(result[-1][3],4.02)

    def test_summarize_best_books(self):
        # call summarize_best_books and save it to a variable
        summbooks = summarize_best_books("best_books_2020.html")
        # check that we have the right number of best books (20)
        self.assertEqual(len(summbooks),20)
            # assert each item in the list of best books is a tuple
        for item in summbooks:
            self.assertEqual(isinstance(item,tuple),True)
            # check that each tuple has a length of 3
            self.assertEqual(len(item),3)

        # check that the first tuple is made up of the following 3 strings:'Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'
        check = ('Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020')
        self.assertEqual(summbooks[0],check)
        # check that the last tuple is made up of the following 3 strings: 'Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'
        check2 = ('Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020')
        self.assertEqual(summbooks[-1],check2)

    def test_write_csv(self):
        # call get_titles_from_search_results on search_results.html and save the result to a variable
        titles = get_titles_from_search_results()

        # call write csv on the variable you saved and 'test.csv'
        write_csv(titles,'test.csv')
        # read in the csv that you wrote (create a variable csv_lines - a list containing all the lines in the csv you just wrote to above)
        file = open('test.csv','r')
        csv_lines = file.readlines()
        file.close()


        # check that there are 21 lines in the csv
        self.assertEqual(len(csv_lines),21)
        # check that the header row is correct
        header = 'Book title,Author Name,Rating'
        self.assertEqual(csv_lines[0].strip(),header)
        # check that the next row is 'Harry Potter Boxed Set, Books 1-5 (Harry Potter, #1-5)', 'J.K. Rowling,', '4.78'
        # ^^this version has a comma after J.K Rowling, however other versions of the answer might not have a comma. We accept both
        row2 = '"Harry Potter Boxed Set, Books 1-5 (Harry Potter, #1-5)",J.K. Rowling,4.78'
        self.assertEqual(csv_lines[1].strip(),row2)
        # check that the last row is 'Harry Potter and the Cursed Child: Parts One and Two (Harry Potter, #8)', 'John Tiffany (Adaptation),', '3.62'
        # ^^^again in a different answer the result for authoer is J.K Rowling. We should accept both
        rowlast = '"Harry Potter and the Cursed Child: Parts One and Two (Harry Potter, #8)", John Tiffany (Adaptation),3.62'
        self.assertEqual(csv_lines[-1].strip(),rowlast)


if __name__ == '__main__':
    print(extra_credit("extra_credit.html"))
    unittest.main(verbosity=2)