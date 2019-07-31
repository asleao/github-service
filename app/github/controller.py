from github import Github


def repository(repository_data: RepositoryData):
    """
    Funcion responsable for getting the credentials and create a repository.
    """
    github_object = authenticate(data=data)
    language = data['language']
    repository_name = data['name']
    if data['action'] == 'add':
        add_repository(github_object, language, repository_name)
    elif data['action'] == 'remove':
        username = github_object.get_user().login
        repository_slug = '{}/{}'.format(username, repository_name)
        repo = github_object.get_repo(repository_slug)
        if repo is not None:
            repo.delete()
            print('{} removed succesfully!'.format(repository_name))

    # TODO Enviar callback?


def add_repository(github_object, language, repository_name):
    github_object.get_user().create_repo(
        repository_name, gitignore_template=language, auto_init=True)
    print('{} created succesfully!'.format(repository_name))


def manage_collaborators(data):
    """
        Funcion responsable for manage collaborators of the repository.
    """
    github_object = Github(repository_data.token)
    repository = github_object.get_user().get_repo(repository_data.repository_name)

    for collaborator in repository_data.collaborators:
        if repository_data.action == 'add':
            add_collaborator(repository, collaborator, repository_data.repository_name)
        elif repository_data.action == 'remove':
            remove_collaborator(repository, collaborator, repository_data.repository_name)


def add_collaborator(repository, collaborator, repository_name):
    """
        Funcion responsable for adding collaborators to the repository.
    """
    repository.add_to_collaborators(collaborator, repository_name)
    print('{} added succesfully on {}!'.format(
        collaborator, repository_name))


def remove_collaborator(repository, collaborator, repository_name):
    """
        Funcion responsable to remove collaborators from the repository.
    """
    if not repository.has_in_collaborators(collaborator):
        return print('{} doesn\'t exist in {}!'.format(collaborator, repository_name))
    else:
        repository.remove_from_collaborators(collaborator)
        return print('{} removed succesfully from {}!'.format(collaborator, repository_name))
