# DebtPortal Vulnerable App
I built Debt Portal as part of a capstone CTF challenge for my Ethical Hacking (CIS 4093 / 4560) students at Baruch. The entire CTF consisted of a penetration test against a fictious student loan company called Debt Direct, and involved attacking services with known vulnerable configurations (e.g. FTP with anonymous access) along with a vulnerable web portal that I quickly put together in Python. 

The goal was to attack the web portal, gain access to the backend database, and find a way to erase student loan debt from a fictious user's account -- and of course document everything, since was part of an ethical penetration testing assignment.

![image](https://user-images.githubusercontent.com/46505379/153771489-9e46f146-67d5-4f6d-9906-7166c07c8f8e.png)

## Overview
* Website is written in Python (Flask)
* User data is stored in a local SQLite database. This made it very easy to deploy the app using one-click deployemnts like AWS Beanstalk
* User registration is disabled in the current version - students had to find and crack hashes leaked on a different system.
* Login requires 2FA provided by Twilio - you'll need to supply your own API keys in order to operate the 2FA validation module (which includes an intended bypass vulnerability)
* Once logged in, users have the ability to update profile information, view current balance, export recent transactions, and initiate a live support session


## Vulnerabilities
I used a few different variations of the site over multiple semesters, but key vulnerabilities included:
1. SQL Injection
2. Insecure hashing of passwords (MD5)
3. 2FA Bypass vulnerability
4. XSS in chat functionality 
5. Multiple business logic vulnerabilities 

![image](https://user-images.githubusercontent.com/46505379/153771638-0eb646e1-ad68-4205-8d12-6f2d06f24cd4.png)
