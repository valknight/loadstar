import os
import shutil
import click
import PyInstaller.__main__
import cv2

files = []
directories = ['web_static', 'web']

if __name__ == '__main__':
    click.echo(click.style('Cleaning up existing builds...', bold=True))
    try:
        shutil.rmtree('dist')
    except FileNotFoundError:
        pass
    click.echo(click.style('Running pyinstaller...', bold=True))
    PyInstaller.__main__.run([
        'loadstar/__main__.py',
        '--add-data=loadstar/web/*;web/',
        '--add-data=loadstar/web_static/*;web_static/',
        '--onefile'
    ])
    click.echo(click.style('Removing build folder', bold=True))
    #shutil.rmtree('build')
    click.echo(click.style('Copying requirements', bold=True))
    for folder in directories:
        shutil.copytree('loadstar/{}'.format(folder), 'dist/{}'.format(folder))
    for f in files:
        shutil.copyfile('loadstar/{}'.format(folder), 'dist/{}'.format(f))
    click.echo(click.style('Done! Check the dist/ folder :)', bold=True, fg='green'))