# Symmetric Cryptography

## Overview
The Substitution Cipher Solver program attempts to decode a Patristocrat cipher(A substitution cipher where spaces in the encrypted text are non-existent or irrelevant).

## Algorithm

The program first generates a random decryption key and attempts to decode it using that key. Then it uses that text and gives a score based on which quadgrams(groups of four letters) appear, with high frequency quadrams getting higher scores and low occurring quadgrams getting lower scores. Then we modify that key by swapping two letters in the key and attempt to decode it using the new key. If the newer key has a better score than it is saved, else discarded(Hill Climbing Algorithm). This is done a set number of times, and then returns the final decoded text. To check if the returned text is made up of real words, we do a dictionary lookup to ensure its accuracy.
