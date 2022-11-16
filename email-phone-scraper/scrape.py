import requests
import bs4
import re
import validators
from urllib.parse import urlparse


def trim_html(html):
	soup = bs4.BeautifulSoup(html, 'html.parser')
	for s in soup(['script', 'style']):
		s.decompose()
	return ' '.join(soup.stripped_strings)

def remove_ws(string):
    return "".join(string.split())

def getEmailAndPhone(urlList):

	phoneList = []
	emailList = []
	
	maxDepth = len(urlList)

	for url in urlList:
		rawHTML = requests.get(url).text
		# print(url)

		soup = bs4.BeautifulSoup(rawHTML, 'html.parser')

		if maxDepth:
			aSoup = soup.find_all('a', attrs={'href': re.compile(r"^/[^.]*$")})
			
			for i in range(len(aSoup)):
				aSoup[i] = aSoup[i].get('href')

				if aSoup[i][0] == '/':
					# print(aSoup[i])
					tempURL = url + aSoup[i][1:]
					if tempURL not in urlList:
						urlList.append(tempURL)

			maxDepth -= 1

		cleanHTML = trim_html(rawHTML)

		emailRegex = r"[\w\+\-][\w\+\-.]{0,62}[\w\+\-]@([A-z0-9]*\.)*[A-z0-9]*"
		# phoneRegex = r"((\+*)((0[ -]*)*|((91 )*))((\d{12})+|(\d{10})+))|\d{5}([- ]*)\d{6}"
		phoneRegex = r"\+?[\s]*([0-9]{2})?[\s-]([0-9]{3}[\s-]*){3}[0-9]"

		matchedStrings = re.findall(f"({phoneRegex})|({emailRegex})", cleanHTML)
	
		for i in matchedStrings:
			if i[0]:
				phoneList.append(i[0])
			if i[3]:
				emailList.append(i[3])

	# remove white spaces
	phoneList = map(remove_ws, phoneList)
	emailList = map(remove_ws, emailList)
		
	# remove duplicate
	phoneList = list(dict.fromkeys(phoneList))
	emailList = list(dict.fromkeys(emailList))

	res = {
		'phoneList': phoneList,
		'emailList': emailList
	}

	return res

if __name__ == "__main__":
	# urlList = ['https://www.staloysiuspuc.in/', 'https://sahyadri.edu.in/']
	urlList = ['https://sahyadri.edu.in/']
	print(getEmailAndPhone(urlList))

# :)