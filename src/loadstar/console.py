
import click


class ConsoleUI():
    """Provides loop for console UI to prevent rapid flashing of screen when using clears
    """

    def __init__(self, showInputs: bool = True) -> None:
        self.displayFrame = 0
        self.display_interval = 5
        self.showInputs = showInputs

    def loop(self, loading: bool, fps: int, loadingColour: int, frameInterval: int):
        self.displayFrame += 1
        if self.displayFrame >= self.display_interval:
            self.displayFrame = 0
            self.output(loading, fps, loadingColour, frameInterval)

    def forceToRender(self):
        """Used when something has happened and we need the UI to immediately show that."""
        self.displayFrame = self.display_interval

    def output(self, loading: bool, fps: int, loadingColour: int, frameInterval: int):
        click.clear()
        if loading:
            click.echo(click.style('loading!!', fg='red', bold=True))
        else:
            click.echo(click.style("Not loading!", fg='green'))
        click.echo(
            'frame interval (o to reduce, p to increase): {}'.format(frameInterval))
        click.echo(
            'loading shade (b to calibrate): {}'.format(loadingColour))
        click.echo(click.style("Open configuration panel: http://127.0.0.1:10000/", bold=True))
        click.echo('fps: {}'.format(fps))
