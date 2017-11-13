import praw
import prawcore
import re

r = praw.Reddit(client_id = 'YOUR_CLIENT_ID_HERE', client_secret = 'YOUR_CLIENT_SECRET_HERE', user_agent = 'YOUR_USER_AGENT_HERE')
print("Logging on...")

file = open('countryname.txt','r')
alias_dict = {}
count_dict = {}
country_list = []

id_file = open('id.txt','r')

for line in file:
	pair = line.rstrip().split('=',1)
	if len(pair) == 1:
		pair.insert(0,pair[-1].split('/')[0])
	for i in pair[-1].split('/'):
		alias_dict[i] = pair[0]
	country_list.append(pair[0])

#for line in id_file:
for post in r.subreddit('polandball').new(limit=None):
	print ("###########################################################")
	output = []
	count_dict = dict.fromkeys(country_list,0) #reset count
	
	#post = r.submission(id=line.rstrip())
	post.comments.replace_more(limit=None)

	for comment in post.comments.list():
		parsed = ' ' + re.sub('[^a-zA-Z ]', ' ', comment.body) + ' ' #padding
		print (parsed)
		
		#OP bonus
		if post.author == comment.author:
			multiplier = 10
			logtext = "     [OP]"
		else:
			multiplier = 1
			logtext = "     [User]"
		
		#first pass for special '' alias
		for alias in alias_dict:
			if alias[0] == "'" and alias[-1] == "'":
				match = ' ' + alias[1:-1] + ' '
				if match in parsed:
					if parsed.count(match) > 1:
						print (logtext + match + ' x' + str(parsed.count(match)))
					else:
						print (logtext + match)
					count_dict[alias_dict[alias]] += parsed.count(match) * multiplier
					parsed = parsed.replace(match,'')
					
		#lowercase for rest
		parsed = parsed.lower()
		for alias in alias_dict:
			if alias[0] != "'" or alias[-1] != "'":
				match = ' ' + alias.lower().decode('utf-8') #left padding - word can extend right but not left
				if match in parsed:
					if parsed.count(match) > 1:
						print (logtext + match + ' x' + str(parsed.count(match)))
					else:
						print (logtext + match)
					count_dict[alias_dict[alias]] += parsed.count(match) * multiplier
					parsed = parsed.replace(match,'')
	
	#title
	parsed = ' ' + re.sub('[^a-zA-Z ]', ' ', post.title) + ' '
	multiplier = 20
	logtext = "     [TITLE]"
	
	for alias in alias_dict:
		if alias[0] == "'" and alias[-1] == "'":
			match = ' ' + alias[1:-1] + ' '
			if match in parsed:
				if parsed.count(match) > 1:
					print (logtext + match + ' x' + str(parsed.count(match)))
				else:
					print (logtext + match)
				count_dict[alias_dict[alias]] += parsed.count(match) * multiplier
				parsed = parsed.replace(match,'')
				
	parsed = parsed.lower()
	for alias in alias_dict:
		if alias[0] != "'" or alias[-1] != "'":
			match = ' ' + alias.lower().decode('utf-8')
			if match in parsed:
				if parsed.count(match) > 1:
					print (logtext + match + ' x' + str(parsed.count(match)))
				else:
					print (logtext + match)
				count_dict[alias_dict[alias]] += parsed.count(match) * multiplier
				parsed = parsed.replace(match,'')
				
	#count stats
	total = 0.0
	for country in count_dict:
		if count_dict[country] != 0:
			total += count_dict[country]
			
	for country in count_dict:
		if count_dict[country] != 0:
			output.append([count_dict[country]/total,country])
	output.sort(reverse=True)
	for i in output:
		print (i[1] + ": " + str(i[0]))
	print(post.title.encode('utf-8'))
	print(post.url.encode('utf-8'))