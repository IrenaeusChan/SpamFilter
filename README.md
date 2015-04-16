# SpamFilter
Bayesian Spam Filter to organize Spam and Ham

#spam.py
This script will create 2 dictionaries utilizing the two provided test cases “learning_ham” and “learning_spam”. After creating the two dictionaries, the script will then create two files titled “outputHam.txt” and “outputSpam.txt” which contains the total number of words matched for all data sets, a list of all the words, their frequencies, P(word|spam or ham), and P(spam or ham|word). 

To use this script, ensure that learning datasets are in the current directory, then on the command line type: 
  python spam.py 

This will produce the two files stated above.

In addition to learning the two dataset provided, the spam.py program also comes with the function to determine whether or not a folder containing email messages is considered spam or not. Simply going into the program and choosing the correct path for the variable fileTest will allow users to receive a list of files within the test folder that are either SPAM or HAM depending on the set confidence level. 

