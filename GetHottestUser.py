import sys
from github import Github
import networkx as nx
from operator import itemgetter

# Global Variables
ACCESS_TOKEN = '05bb4eb867b152be20dd11f4fa292107c839931c'
USER = 'minrk'  # Define the GitHub User Name
REPO = 'findspark'  # Define the Repo name
client = Github(ACCESS_TOKEN)
g = nx.DiGraph()


def getStargazers(REPO):
    user = client.get_user(USER)
    repo = user.get_repo(REPO)  # Get a specific repo
    REPOS = user.get_repos()
    stargazers = list(repo.get_stargazers())  # The list of users who starred this REPO
    g.add_node(repo.name + '(repo)', type='repo', lang=repo.language, owner=user.login)
    for sg in stargazers:
        g.add_node(sg.login + '(user)', type='user')
        g.add_edge(sg.login + '(user)', repo.name + '(repo)', type='gazes')
    #	print(len(stargazers))#See if it return a correct list
    return stargazers


def buildRelations(stargazers):
    for i, sg in enumerate(stargazers):
        try:
            for follower in sg.get_followers():
                if follower.login + '(user)' in g:
                    g.add_edge(follower.login + '(user)', sg.login + '(user)',
                               type='follows')
        except Exception:  # ssl.SSLError
            sys.stderr.write("Encountered an error fetching followers for", \
                             sg.login, "Skipping.")

        print("Processed", i + 1, " stargazers. Num nodes/edges in graph", \
              g.number_of_nodes(), "/", g.number_of_edges())
        print("Rate limit remaining", client.rate_limiting)

def getHottestRepo(stargazers):
    MAX_REPOS = 500
    for i, sg in enumerate(stargazers):
        print(sg.login)
        try:
            for starred in sg.get_starred()[:MAX_REPOS]:  # Slice to avoid supernodes
                g.add_node(starred.name + '(repo)', type='repo', lang=starred.language, \
                           owner=starred.owner.login)
                g.add_edge(sg.login + '(user)', starred.name + '(repo)', type='gazes')
        except Exception:  # ssl.SSLError:
            print("Encountered an error fetching starred repos for", sg.login, "Skipping.")

        print("Processed", i + 1, "stargazers' starred repos")
        print("Num nodes/edges in graph", g.number_of_nodes(), "/", g.number_of_edges())
        print("Rate limit", client.rate_limiting)
    print(nx.info(g), '\n')
    # repos = [n for n in g.nodes_iter() if g.node[n]['type'] == 'repo']
    print("Popular repositories")
    for (n,d) in g.in_degree_iter():
        node = g.node[n]
        if node['type'] == 'repo':
            print(1)
    print(sorted([(n, d)
                  for (n, d) in g.in_degree_iter()
                  if g.node[n]['type'] == 'repo'], key=itemgetter(1), reverse=True)[:10])

    print("Respositories that luzhijun has bookmarked")
    print([(n, g.node[n]['lang'])
           for n in g['luzhijun(user)']
           if g['luzhijun(user)'][n]['type'] == 'gazes'])


    print("Programming languages luzhijun is interested in")
    print(list(set([g.node[n]['lang']
                    for n in g['luzhijun(user)']
                    if g['luzhijun(user)'][n]['type'] == 'gazes'])))

    print("Supernode candidates")
    print(sorted([(n, len(g.out_edges(n)))
                  for n in g.nodes_iter()
                  if g.node[n]['type'] == 'user' and len(g.out_edges(n)) > MAX_REPOS], \
                 key=itemgetter(1), reverse=True))
if __name__ == '__main__':
    stargazers = getStargazers(REPO)
    buildRelations(stargazers)
    print(nx.info(g), '\n')
    print(len([e for e in g.edges_iter(data=True) if e[2]['type'] == 'follows']), '\n')
    getHottestRepo(stargazers)
