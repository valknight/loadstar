import os
import shutil
import click
import PyInstaller.__main__
import cv2
print(cv2.file)

files = []
directories = ['web', 'web_static']

if __name__ == '__main__':
    click.echo(click.style('Cleaning up existing builds...'))
    try:
        shutil.rmtree('dist')
    except FileNotFoundError:
        pass
    click.echo(click.style('Running pyinstaller...'))
    PyInstaller.__main__.run([
        'loadstar/__main__.py',
        'paths="..\\venv\Lib\site-packages\cv2"'
    ])
    click.echo(click.style('Removing build folder'))
    shutil.rmtree('build')
    click.echo(click.style('Copying requirements'))
    for folder in directories:
        shutil.copytree('loadstar/{}'.format(folder), 'dist/{}'.format(folder))
    for f in files:
        shutil.copyfile('loadstar/{}'.format(folder), 'dist/{}'.format(f))