import requests
from operator import itemgetter
from plotly.graph_objs import Bar
from plotly import offline

# Make an API call to store response
url = 'https://hacker-news.firebaseio.com/v0/topstories.json'
r = requests.get(url)
print(f'Status Code {r.status_code}')

# Process Data
submission_ids = r.json()
submission_dicts = []
for index, submission_id in enumerate(submission_ids[:31]):
    # Separate API calls for each submission
    url = f'https://hacker-news.firebaseio.com/v0/item/{submission_id}.json'
    r = requests.get(url)
    print(f'{index} id: {submission_id} status: {r.status_code}')
    response_dict = r.json()

    # Build a dictionary for each article
    try:
        submission_dict = {
            'title': response_dict['title'],
            'link': response_dict['url'],
            'comments': response_dict['descendants']
        }
    except KeyError:
        continue
    else:
        submission_dicts.append(submission_dict)

submission_dicts = sorted(submission_dicts, key=itemgetter('comments'), reverse=True)

titles, links, comments = [], [], []
for position, submission_dict in enumerate(submission_dicts):
    print(f'\n{position + 1}\tTitle: {submission_dict["title"]}')
    print(f'\tDiscussion Link: {submission_dict["link"]}')
    print(f'\tComments: {submission_dict["comments"]}')

    titles.append(submission_dict["title"])

    repo_url = submission_dict["link"]
    title = submission_dict["title"]
    repo_link = f"<a href='{repo_url}'>{title}</a>"
    links.append(repo_link)

    comments.append(submission_dict["comments"])

data = {
    'type': 'bar',
    'x': links,
    'y': comments,
    'hovertext': titles,
    'marker': {
        'color': 'rgb(60, 100, 150)',
        'line': {'width': 1.5, 'color': 'rgb(25, 25, 25)'}
    },
    'opacity': 0.6,
}

my_layout = {
    'title': 'Top 30 Most Recent Interacted Articles on HackerNews',
    'xaxis': {'title': 'Articles',
              'titlefont': {'size': 24},
              'tickfont': {'size': 14},
              },
    'yaxis': {'title': 'Comments',
              'titlefont': {'size': 24},
              'tickfont': {'size': 14},
              }
}
fig = {'data': data,'layout': my_layout}
offline.plot(fig, filename='hackernews_top30.html')
