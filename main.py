"""
Sam, Nicolas
Student ID: 001249697
"""
from wgups.models.application import Application
from wgups.structures import Timer

app = Application()
app.initialize()

if __name__ == '__main__':
    print("=====================================================")
    print("Welcome to the WGUPS Daily Local Deliveries System!")
    print("=====================================================")
    app.display_options()

    command = input('Please enter a command: ')
    while command not in app.exit_commands:
        try:
            c = app.commands.get(command)
            c.get("method")()
            print(f"========= END =========")
            command = input('Please enter a command:')
        except AttributeError:
            print(f"========= ERROR =========")
            print("Please enter a valid command from the options below")
            app.display_options()
            command = input('Please enter a command: ')

    print("See you next time!")
