#!/bin/bash
# Tetun Crawler Pipeline

echo "Initiating the crawling process ..."

# Generate seed words and seed URLS
# Loop to run the seeder.py script 10 times
for i in {1..10}; do
   echo "Generating seed words and seed URLS for the $i time ..."
   python3 ./pipeline/seeder.py
done

# # Crawling the World Wide Web with 15 rounds
echo "Crawling the World Wide Web ..."
cd nutch
./bin/crawl -i -s urls/ --hostdbupdate --hostdbgenerate crawl/ 15
cd ..
# # Crawling concluded
echo "The crawling have been successfully concluded."

# Construct text corpus
echo "Constructing text corpus ..."
python3 ./pipeline/construct_corpus.py
# Corpus concluded
echo "The corpus have been successfully generated."

# Generate collection statistic
echo "Generating statistic for the collection ..."
python3 ./pipeline/view_collection_stat.py
# Statistic generation concluded
echo "The statistics have been successfully generated."
