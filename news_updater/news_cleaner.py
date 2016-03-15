# Name: News Trimmer
# Author: Dax Gerts
# Date: 14 March 2016
# Script to parse master csv file and trim redundant and bad rows, based on jamylak's solution on stackoverflow
#	http://stackoverflow.com/questions/15741564/removing-duplicate-rows-from-a-csv-file-using-a-python-script

def main():
	with open('papers.csv','r') as incsv, open('papers_clean.csv','w') as outcsv:
		seen = set()
		for line in incsv:
			if line in seen: continue # skips duplicates

			seen.add(line)
			outcsv.write(line)


if __name__ == "__main__":
	# Suppress "no handlers could be found" message for tldextract
	# NOTE: requires admin access to access "logging.basicConfig()"
	main()