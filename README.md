# BudgetTrackerCAN

BudgetTrackerCAN is a comprehensive budget tracking tool designed **for my personal use** given Intuit is shutting down Mint. It helps me manage my finances by aggregating transaction data from all my accounts across major financial institutions in Canada. The tool automates the process of retrieving transactions, categorizing them, and tracking my budget.

> **Note: This project is intended for my personal use, and I may not maintain it for anyone else.**

For now, I have finished the backbone for Amex Canada, with the card selection hard-coded for myself.

## To-do
- [x] amex.py backbone
- [x] keyring
- [x] run.py
- [ ] tangerine.py
- [ ] amex.py card selection

## Instructions
1. Run `add_credentials.py` to store your credentials. They will be encrypted and stored locally by `keyring`.
2. Modify `config.yaml` to include your financial institutions, cards, and URLs.
3. Run `run.py`. All transactions will be stored locally in `transactions.db`.
