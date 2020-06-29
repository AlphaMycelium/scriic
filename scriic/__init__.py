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
    for param in runner.required_parameters:
        params[param] = input(f"Parameter {param}: ")

    # Run the scriic
    instruction = runner.run(params)

    # Print instructions
    for i, instruction in enumerate(instruction.leaf_nodes()):
        instruction.display_index = i + 1
        print(f"{instruction.display_index}. {instruction.text()}")


# This is used as an entrypoint in setup.py
def main():
    fire.Fire(run)


if __name__ == "__main__":
    # Allow this file to be ran directly too
    main()
