from collections import OrderedDict

import requests

max_total_repos = 15

grouped = True

authors = {
    "CSML-IIT-UCL":dict(name="CSML",max_repos=None, excluded_repos=[".github"], selected_repos=None),

    # users to fetch
    "prolearner":dict(name="Riccardo Grazzi", max_repos=5, excluded_repos=["procedural-planet"], selected_repos=None),
    "Pietronvll":dict(name="Pietro Novelli", max_repos=5, excluded_repos=[], selected_repos=None),
    "IsakFalk":dict(name="Isak Falk", max_repos=5, excluded_repos=[], selected_repos=["learn2learn"]),
    "vladi-iit":dict(name="Vladimir Kostic", max_repos=5, excluded_repos=[], selected_repos=None),
    "RuohanW":dict(name="Ruohan Wang", max_repos=5, excluded_repos=[], selected_repos=None),
    "LeonardoCella":dict(name="Leonardo Cella", max_repos=5, excluded_repos=[], selected_repos=None),
}

def generate_readme_grouped(authors):
    readme_content = "# Popular Repos\n\n"

    repositories = []
    for username, author in authors.items():
        author_url = get_author_profile_url(username)
        max_repos = author['max_repos'] if author['max_repos'] is not None else 10000
        repos = sort_repositories_by_stars(get_repositories(username))
        for i, r in enumerate(repos):
            r['displayed_owner'] = author['name']
            r['owner_url'] = author_url
            if i < max_repos and r["name"] not in author['excluded_repos']:
                if author['selected_repos'] is None:
                    repositories.append(r)
                elif r["name"] in author['selected_repos']:
                    repositories.append(r)

    repositories_to_show = sort_repositories_by_stars(repositories)[:max_total_repos]

    for repo in repositories_to_show:
        username = repo['owner']['login']
        repo_name = repo["name"]
        stars = repo["stargazers_count"]
        forks = repo["forks_count"]
        readme_content += "- [{}]({})".format(repo_name, get_repo_url(username, repo_name))
        if stars > 0:
            readme_content += " - ⭐ {}".format(stars)
            if forks > 0:
                readme_content += " 🍴 {}".format(forks)
        readme_content += " - [{}]({})".format(repo['displayed_owner'], repo['owner_url'])

        readme_content += "\n"

    readme_content += "\n"

    with open("profile/README.md", "w") as readme_file:
        readme_file.write(readme_content)

def generate_readme(authors):
    readme_content = "# CSML Repositories\n\n"

    for i, (username, author) in enumerate(authors.items()):
        if i == 1:
            readme_content += "## Members\n\n"
        if i > 0:
            readme_content += "### [{}]({})\n".format(author['name'], get_author_profile_url(username))

        repositories = get_repositories(username)
        sorted_repositories = sort_repositories_by_stars(repositories)
        repositories_to_show = sorted_repositories[:author['max_repos']] if author['max_repos'] is not None else sorted_repositories

        for repo in repositories_to_show:
            repo_name = repo["name"]
            if repo_name not in author['excluded_repos']:
                stars = repo["stargazers_count"]
                forks = repo["forks_count"]
                readme_content += "- [{}]({})".format(repo_name, get_repo_url(username, repo_name))
                if stars > 0:
                    readme_content += " - ⭐ {}".format(stars)
                    if forks > 0:
                        readme_content += " 🍴 {}".format(forks)

                readme_content += "\n"

        readme_content += "\n"

    with open("profile/README.md", "w") as readme_file:
        readme_file.write(readme_content)


def get_repositories(author):
    url = f"https://api.github.com/users/{author}/repos"
    headers = {
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        repositories = response.json()
        return repositories
    else:
        print(f"Failed to retrieve repositories for {author}. Error: {response.text}")
        return []

def sort_repositories_by_stars(repositories):
    sorted_repositories = sorted(repositories, key=lambda x: x["stargazers_count"], reverse=True)
    return sorted_repositories

def get_author_profile_url(author):
    return "https://github.com/{}".format(author)

def get_repo_url(author, repo_name):
    return "https://github.com/{}/{}".format(author, repo_name)


if __name__ == '__main__':
    if grouped:
        generate_readme_grouped(authors)
    else:
        generate_readme(authors)