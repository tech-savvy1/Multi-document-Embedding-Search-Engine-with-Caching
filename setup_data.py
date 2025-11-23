import os
from sklearn.datasets import fetch_20newsgroups

def setup_data():
    # Create the directories to store the documents
    os.makedirs("data/docs", exist_ok=True)
    print("Downloading 20 Newsgroups dataset...")
    
    # Fetch a small subset to keep it lightweight (100-200 docs)
    newsgroups = fetch_20newsgroups(subset='train', categories=['sci.space', 'comp.graphics'], remove=('headers', 'footers', 'quotes'))
    
    limit = 150 # Limit to 150 docs
    
    for i, text in enumerate(newsgroups.data[:limit]):
        if len(text) > 100: # Skip very short/ empty files
            filename = f"data/docs/doc_{i:03d}.txt"
            with open(filename, "w", encoding="utf-8") as f: # Save each document as a text file
                f.write(text) # Write the document content to the file
    
    print(f"Saved {limit} documents to data/docs/")

if __name__ == "__main__": # Run the setup function when executed directly
    setup_data()