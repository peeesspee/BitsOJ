def create_file(code, language):

# if code is in C++
    if language == 'C++':
        with open("test.cpp", "w") as file:
            file.write(code)
            return "test.cpp"

# if code is in C
    if language == 'C':
        with open("test.c", 'w') as file:
            file.write(code)
            return "test.c"

# if code is in Java
    if language == 'Java':
        with open("test.java", 'w') as file:
            file.write(code)
            return "test.java"


# if code is in Python
    if language == 'Python':
        with open("test.py", 'w') as file:
            file.write(code)
            return "test.py"


# dummy code stired in string variable x
x = "import socket \nimport os\nimport subprocess\nimport sys"


def judge(code, problem_code, runid, language):

    create_file(code, language)








# calling judge function
judge(x, "IAM", "123", "Python");
