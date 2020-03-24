import fire

from .run import FileRunner


def run(file):
    """
    Run a Scriic and print the generated instructions.

    Any parameters will be asked for on the command line.

    :param file: Path to the file to run
    """
    runner = FileRunner(file)

    # Ask for parameters
    params = dict()
    for param in runner.params:
        params[param] = input(f'Parameter {param}: ')

    # Run the scriic
    steps = runner.run(params)

    # Print steps
    for i, step in enumerate(steps):
        print(f'{i+1}. {step}')

# This is used as an entrypoint in setup.py
def main():
    fire.Fire(run)


if __name__ == '__main__':
    # Allow this file to be ran directly too
    main()