import click
import requests
import subprocess
import json
import os
from markdown_reader import extract_dict

def user_exists(username, reloadfile, verbose):
    os_status = os.system('cut -d: -f1 /etc/passwd | grep "' + username + '"')
    if(os_status == 0):
        return True
    else:
        return False

def command_call(command, verbose):
    os_status = os.system(command)
    if verbose:
        click.echo(message='The command "' + command + ' exited with status ' + str(os_status))

@click.command()
@click.option('--reloadfile', is_flag=True, help='Reloads the ssh keys from git')
@click.option('--verbose', is_flag=True, help='Enables verbose mode')

def get_keys(reloadfile, verbose):

    GITLAB_TOKEN = ""
    GITLAB_PROJECT_ID = ""
    GITLAB_SLUG = ""
    GITLAB_URL = "https://gitlab.com/api/v4/projects/" + GITLAB_PROJECT_ID + "/wikis/" + GITLAB_SLUG
    GITLAB_HEADER = {
    "PRIVATE-TOKEN": GITLAB_TOKEN
    }

    if reloadfile:
        filelink = GITLAB_URL

        if verbose:
            click.echo(message='Fetching from ' + filelink)

        result = requests.get(url=filelink, headers=GITLAB_HEADER)

        if verbose:
            click.echo(message='Request done with status ' + str(result.status_code))

        json_dict = json.loads(result.text)

        if verbose:
            click.echo(message='Request content: ' + json_dict['content'])

        users_dict = extract_dict(json_dict['content'])

        if verbose:
            click.echo(message='Content parsed: \n\n' + str(users_dict))

        for each in users_dict:
            if(user_exists(each, reloadfile, verbose)):
                click.echo(message="There exists the user " + each)
            else:
                if each != '':
                    CREATE_USER_COMMAND = 'sudo useradd -m ' + each
                    command_call(CREATE_USER_COMMAND, verbose)

            MKDIR = 'mkdir /home/' + each + '/.ssh/'

            command_call(MKDIR, verbose)

            TOUCH = 'touch /home/' + each + '/.ssh/authorized_keys'

            command_call(TOUCH, verbose)

            ECHO_COMMAND = 'echo "'
            ECHO_FILE = '" > /home/' + each + '/.ssh/authorized_keys'
            ECHO_CONTENT = ECHO_COMMAND + users_dict[each] + ECHO_FILE

            command_call(ECHO_CONTENT, verbose)

        click.echo(message='Keys reloaded successfully!')

    else:
        click.echo(message='Please give me a flag =(')
if __name__ == '__main__':
    get_keys()
