# sats_manager
This program helps you generate a list of all transactions on all of your addresses. Takes x/y/zpub as input, derives addresses, check for transaction history on each of them and stores the TX data (if any). Allows you to export the final TXs as a csv for your bookkeeping purposes.

# IMPORTANT SECURITY NOTICE
As of the current version, all the blockchain interactions take place via public APIs. <u>You are risking exposing your extended public key and derevation paths using this program in it's current state!</u>

- I am currently working on adding connectivity to personal nodes, as well as standalone .exe/.dmg installers.
