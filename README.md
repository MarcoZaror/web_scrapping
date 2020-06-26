## README file

This piece of software was developed to access every news from the BBC and Daily Mail websites. In addition, it stores the link, title, summary and corpus.

### Files
Data.py
  - Class to store the content of the news, process it and write it
  - Methods
    - update_content: Update the previously loaded content with the new information
    - load_content: Load the stored content
    - write_content: Write the updated content in a file
    - remove_dup: Remove duplicate news
  
Scrapping.py
  - Class to perform the scraping process
  - Methods
    - look_for_links: Obtain all the links given an url
    - grab_summary: Self-explanatory
    - grab_title: Self-explanatory
    - grab_article: Self-explanatory
    
main.py
  - Run the software
  - Steps:
    - Starts from a list of seeds (web urls)
    - From each seed, extracts all the potential news links
    - For each link, check that it is news and grab the title, article and summary
