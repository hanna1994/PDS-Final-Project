from github import Github
ACCESS_TOKEN = '05bb4eb867b152be20dd11f4fa292107c839931c'

#Example 1
USER = 'StevenQu'
client = Github(ACCESS_TOKEN)
user = client.get_user(USER)
REPOS=user.get_repos() #Get all the repos
print(list(REPOS))


#Example 2
USER='minrk'#Define the GitHub User Name 
REPO='findspark'#Define the Repo name
client = Github(ACCESS_TOKEN)
user = client.get_user(USER)
repo=user.get_repo(REPO) #Get a specific repo
REPOS=user.get_repos()
stargazers=list(repo.get_stargazers())#The list of users who starred this REPO
print(len(stargazers))#See if it return a correct list

