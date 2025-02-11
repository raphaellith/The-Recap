import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

def get_titles_from_the_guardian(get_link=False):
    url = "https://www.theguardian.com/technology/all"

    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    result = []

    for a_tag in soup.find_all("a"):
        data_link_name = a_tag.get('data-link-name')
        if data_link_name is not None:
            if data_link_name.startswith("news") or data_link_name.startswith("feature"):
                title = a_tag.get('aria-label')
                if get_link:
                    link = "https://www.theguardian.com" + a_tag.get('href')
                    result.append((title, link))
                else:
                    result.append(title)
    return result

def get_titles_from_bbc(get_link=False):
    url = "https://www.bbc.co.uk/news/technology"

    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    result = []

    for a_tag in soup.find_all("a"):
        if a_tag.get('href') is not None:
            link = a_tag.get('href')
            if link.startswith('/news'):
                children = a_tag.find_all("span")
                for child in children:
                    if child.get('aria-hidden') == 'false':
                        title = child.text
                        if get_link:
                            link = 'https://www.bbc.co.uk' + link
                            result.append((title, link))
                        else:
                            result.append(title)
    return result

def clean_and_tokenize(headlines):
    common_words = {'a', 'an', 'the', 'and', 'or', 'but', 'if', 'then', 'else', 'on', 'in', 'at', 'of', 'for', 'to', 'with'}
    cleaned_headlines = []
    for headline in headlines:
        words = re.findall(r'\b\w+\b', headline.lower())
        cleaned_words = [word for word in words if word not in common_words]
        if cleaned_words:  # ensure headline is not empty after cleaning
            cleaned_headlines.append(' '.join(cleaned_words))
    return cleaned_headlines

# compare headlines using cosine similarity
def compare_headlines(headlines1, headlines2, threshold=0.2):
    all_headlines = headlines1 + headlines2
    if not all_headlines: 
        return []
    
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(all_headlines)
    
    cosine_matrix = cosine_similarity(tfidf_matrix)
    n1 = len(headlines1)
    n2 = len(headlines2)
    
    matches = []
    for i in range(n1):
        for j in range(n1, n1 + n2):
            score = cosine_matrix[i][j]
            if score > threshold:
                matches.append((headlines1[i], headlines2[j - n1], score))
    
    return matches

def main():
    guardian_headlines = get_titles_from_the_guardian()
    bbc_headlines = get_titles_from_bbc()

    print("Guardian Headlines:", guardian_headlines)
    print("BBC Headlines:", bbc_headlines)

    cleaned_guardian = clean_and_tokenize(guardian_headlines)
    cleaned_bbc = clean_and_tokenize(bbc_headlines)

    print("Cleaned Guardian Headlines:", cleaned_guardian)
    print("Cleaned BBC Headlines:", cleaned_bbc)

    matches = compare_headlines(cleaned_guardian, cleaned_bbc)

    if not matches:
        print("No matches found.")

    for match in matches:
        print(f"Guardian: {match[0]}")
        print(f"BBC: {match[1]}")
        print(f"Similarity Score: {match[2]:.2f}\n")

if __name__ == "__main__":
    main()
