LINK TO PROJECT: https://github.com/hjeronen/project_1

The project has a simple messaging application (called 'Poster') where users can send messages to each other. The application code is largely based on the exercise template of the exercise 'Cookie heist' from part III of the course 'Securing Software' [1], with own modifications and additions.

Running the application requires having the same libraries installed as the programming exercises on the course 'Securing Software' (namely Python 3). Fix for flaw 3 requires installing an additional package, but instructions for installation and deployment are given with the fix.

After cloning the repository, go to the 'project_1' folder ('project_1' root, not repository root) where you should see the file 'manage.py'. You can start the application server by running the 'manage.py' file with python (command 'python manage.py runserver' or 'python3 manage.py runserver' depending on your OS). Once the server is started go to http://127.0.0.1:8000/ in browser.

The application has preregistered users 'alice' (password 'redqueen'), 'bob' ('squarepants') and 'admin' ('admin') for testing the application, but new users can also be created.

The flaw categories were picked from OWASP Top 10 list 2021. [2]

---------

FLAW 1: A01:2021 – Broken Access Control
LINK: https://github.com/hjeronen/project_1/blob/150226d33492cb8b78e81461f1638a7da0995b85/project_1/poster/views.py#L53

The application uses Django's authentication system (with login_required() decorator) to allow sending, viewing or deleting messages, but it does not specify who must be logged in. This leads to users having access to other user's messages, which they should not have.

For example, the application allows users to delete their messages, and requires that the user is logged in to do so – however, it does not check that the logged in user is the owner of the message (either sender or receiver). Users should be able to delete only their own messages, but now anyone who is logged in can delete anyone else's messages by modifying the URL.

HOW TO FIX:

LINK TO FIX: https://github.com/hjeronen/project_1/blob/150226d33492cb8b78e81461f1638a7da0995b85/project_1/poster/views.py#L57

The backend should check that the currently logged in user is the owner of the message before deleting it (here, either sender or receiver is the message's owner).

---------

FLAW 2: A03:2021 – Injection
LINK: https://github.com/hjeronen/project_1/blob/150226d33492cb8b78e81461f1638a7da0995b85/project_1/poster/views.py#L25

When saving the user's message to the database, the message content is directly attached to the SQL-statement. This enables SQL injection attacks: it is possible to escape the current statement and write a new one that also gets executed. For example, by sending the message (without opening and closing quotes) "hacking your fancy app', '2022-08-17 13:13:27.106930', 2, 1); UPDATE auth_user SET is_superuser=1, is_staff=1 WHERE username='alice'; INSERT INTO poster_message VALUES (NULL, 'alice is the queen now!" alice can change her user role to admin (and flood admin's page with unnecessary messages). This way the attacker could also send messages using someone else's id number, delete the whole database, or wreak all kinds of havoc.

HOW TO FIX:

LINK TO FIX option 1: https://github.com/hjeronen/project_1/blob/150226d33492cb8b78e81461f1638a7da0995b85/project_1/poster/views.py#L35
LINK TO FIX option 2: https://github.com/hjeronen/project_1/blob/150226d33492cb8b78e81461f1638a7da0995b85/project_1/poster/views.py#L45

There are several ways to fix this issue. For starters, you should use 'execute()' command instead of 'executescript()', since the former allows the execution of only one SQL statement at a time, and therefore you cannot escape the current INSERT statement. SQL injection is still possible, but would only lead to an error (with INSERT statements). To actually prevent injection, you should also use parameterized SQL statements where user input is properly separated from the query. The best practice would be to use Django's Models that have built in protection against SQL-injection. The Message-model is defined in the file 'project_1/poster/models.py'.

---------

FLAW 3: A02:2021 – Cryptographic Failures
LINK: https://github.com/hjeronen/project_1/blob/150226d33492cb8b78e81461f1638a7da0995b85/project_1/project_1/settings.py#L31

Django uses the variable SECRET_KEY for all cryptographic signing. It is defined in the project file 'settings.py', and currently publicly available in the project's GitHub repository. This should never happen with a real project, as attackers could use the SECRET_KEY for producing their own signed values.

HOW TO FIX:

LINK TO FIX part 1: https://github.com/hjeronen/project_1/blob/150226d33492cb8b78e81461f1638a7da0995b85/project_1/project_1/settings.py#L15
LINK TO FIX part 2: https://github.com/hjeronen/project_1/blob/150226d33492cb8b78e81461f1638a7da0995b85/project_1/project_1/settings.py#L25
LINK TO FIX part 3: https://github.com/hjeronen/project_1/blob/150226d33492cb8b78e81461f1638a7da0995b85/project_1/project_1/settings.py#L35

The old SECRET_KEY should be removed from the public repository and changed into a new key. The new key and all other sensitive information in 'settings.py' should be defined in a separate configuration file, from where it is imported to the 'settings.py' where it is needed. This separate configuration file should then be kept private (not uploaded in GitHub).

For example, with Django you can install Django Environ package (if you are using pip, run command 'pip install django-environ' in project_1 root), import it to 'settings.py' (see links to fix part 1 and part 2), create '.env' file in the same directory where the file 'settings.py' is and declare all environment variables there (write 'SECRET_KEY=your-secret-key' without spaces or quotes into the '.env' file and save), and add '.env' to '.gitignore'. Use the environment variables defined in '.env' in the 'settings.py' instead of the actual values (see link to fix part 3). For original and more detailed instructions see link at footnote [3]. In addition to SECRET_KEY, other sensitive information such as the database address and the default setting for DEGUB should be defined in the '.env'  file as well, and be kept secret.

It should be noted that even if the SECRET_KEY was removed from the 'settings.py' file and from the public repository, it would still be in the commit history on GitHub and freely available to anyone, which is why a new key should be generated (you can generate a new key for example with the command: ‘python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'’ (instructions from [4])). Erasing GitHub's commit history is a bit trickier, though GitHub docs [5] have some instructions for this, too.

As a side note, the database file containing sensitive user information such as passwords should not be in the public repository either.

---------

FLAW 4: A07:2021 – Identification and Authentication Failures
LINK: https://github.com/hjeronen/project_1/blob/150226d33492cb8b78e81461f1638a7da0995b85/project_1/project_1/settings.py#L116

There is a function for registering new users for the messaging application that uses Django's own user registration form, which has some built in safety features against for example injection attacks. However, there are not enough requirements for safe passwords, thus allowing registration with relatively weak passwords and making the application vulnerable for credential stuffing attacks. Also, the pre-existing credentials, for example 'admin:admin', are clearly not up to standard, and are causing a major risk for the application.

HOW TO FIX:

LINK TO FIX: https://github.com/hjeronen/project_1/blob/150226d33492cb8b78e81461f1638a7da0995b85/project_1/project_1/settings.py#L123

The first step in defending against credential stuffing attacks is enforcing good password policy (also, admin should change their password immediately). Django's authentication system can handle validating passwords, preventing users from choosing weak credentials. Password validation is configured in the AUTH_PASSWORD_VALIDATORS setting in the 'settings.py' file. You can add more validators depending on what criteria for password creation you would like to enforce. For example, CommonPasswordValidator compares the given password to 20000 most common passwords, and prevents the use of at least the most obvious or popular passwords. For more on validators see Django docs [6].

Of course, a password that passes all the validators might still not be a good or strong password. The attackers might also be using known credential lists obtained through data breaches to other systems. People tend to use the same username and password for different services, in which case it does not matter how strong your users’ passwords are if they have been exposed elsewhere. To further mitigate the risk of credential stuffing attacks, more robust actions such as account lockout or multi factor authentication should be used [7]. You could also use django-ratelimit-backend to prevent multiple login attempts from the same IP [8]. These are not implemented here, though.

---------

FLAW 5: A05:2021 – Security Misconfiguration
LINK: https://github.com/hjeronen/project_1/blob/150226d33492cb8b78e81461f1638a7da0995b85/project_1/project_1/settings.py#L40

The application code in the GitHub is currently in development mode, but if the application was run with current settings in production, there would be some serious security concerns. When attempting something that raises an error, such as a badly formatted SQL injection, the application will show very detailed error pages to the user. This should definitely not happen since this traceback gives the attacker valuable information about the structure of the application and its database, enabling them to improve their attacks.

HOW TO FIX:

LINK TO FIX: https://github.com/hjeronen/project_1/blob/150226d33492cb8b78e81461f1638a7da0995b85/project_1/project_1/settings.py#L48

Django shows the error page because the application is run with the setting DEBUG = True. This should of course never happen in production environment, but instead the DEBUG should be set to 'False' (this setting should be defined in the '.env' file). When not running the application in debug mode, the list ALLOWED_HOSTS will need to be defined – here it can be set to '['127.0.0.1', 'localhost']' (or in production environment whatever the host name is). For more on DEBUG see Django docs [9].

---------

Sources:

[1] https://cybersecuritybase.mooc.fi/module-2.3/1-security#programming-exercise-cookie-heist

[2] https://owasp.org/www-project-top-ten/

[3] https://alicecampkin.medium.com/how-to-set-up-environment-variables-in-django-f3c4db78c55f

[4] https://www.educative.io/answers/how-to-generate-a-django-secretkey

[5] https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository

[6] https://docs.djangoproject.com/en/4.1/topics/auth/passwords/#module-django.contrib.auth.password_validation

[7] https://www.linkedin.com/pulse/protecting-django-app-from-password-guessing-attacks-jerin-jose

[8] https://django-ratelimit-backend.readthedocs.io/en/latest/

[9] https://docs.djangoproject.com/en/4.1/ref/settings/#debug
