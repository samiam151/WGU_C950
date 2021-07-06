"""
Sam, Nicolas
Student ID: 001249697
"""
from wgups.models.application import Application

app = Application()
app.initialize()

if __name__ == '__main__':
    print("=====================================================")
    print("Welcome to the WGUPS Daily Local Deliveries System!")
    print("=====================================================")
    app.display_options()

    command = input(app.input_prompts.get("enter_command"))
    while command.lower() not in app.exit_commands:
        try:
            c = app.commands.get(command.lower())
            c.get("method")()
            print(f"========= END =========")
            command = input(app.input_prompts.get("enter_command")).lower()
        except AttributeError:
            print(f"========= ERROR =========")
            print(app.input_prompts.get("incorrect_command"))
            app.display_options()
            command = input(app.input_prompts.get("enter_command")).lower()

    print("=====================================================")
    print("Thanks for using our system. See you next time!")
    print("====================== END ==========================")
