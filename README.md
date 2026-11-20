# Expense Tracker
Expense tracker is a super simple CLI tool that tracks all your recurring expenses. You might use this to track active susbcriptions, recurring daily expenses etc (although they're generically called subscriptions in the tool)

![Demonstration of the program running](assets/markdown/demonstration.gif)

## Features
- Can add subscriptions
- Can remove subscriptions
- Can edit subscriptions
- Information board tells you the "relative cost" of the expense, which is a simple CDF (Cumulative Distribution Function) of that expense, giving you a small insight on how much more, or less expense it is from the rest of your other expenses
- Information board tells you general statistics such as total expense, minimum and maximum, mean, and standard deviation.
- Navigable command interface using `W` and `A` and `Enter`.

## Installation
1. Download the `.whl` file in the releases section.
2. Ensure you have `pipx` installed (globally) and that you have ran `pipx ensurepath` at least once. You can use `python -m pip install pipx` in a non-venv activated terminal to install it.
3. Run `pipx install <path to your wheel file>`
4. `expense` should now be available as a global command on your system.

## Usage
Running `expense` will bring up an interactive screen, navigable via `W` and `A` and `Enter`. There is a minimum size that your command prompt has to be for the interface to work properly, but you can refresh by clicking any key after resizing. `CTRL + C` during any of the screens where you input information (not the main menu) will abort the program. Your keyboard is also completely locked into the terminal (known limitation), so be sure to exit it when you are no longer using it.
