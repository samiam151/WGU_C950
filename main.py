"""
Sam, Nicolas
Student ID: 001249697
"""
from wgups.models.application import Application
from wgups.structures import Timer

app = Application()
app.initialize()


if __name__ == '__main__':
    print("Welcome to the WGUPS Daily Local Deliveries System!")
    print("--- some instructions ---")

    exit_commands = ['quit', 'exit', 'q', '']
    # while input('Please enter a command:') not in exit_commands:
    #     pass

    app.run_time_reports()

