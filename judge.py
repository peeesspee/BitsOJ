def judge(code, problem_code, runid, language):



# if code is in C++

    if language == 'C++':
        with open("test.cpp", "w") as file:
            file.write(code)

# if code is in C

    if language == 'C':
        with open("test.c", 'w') as file:
            file.write(code)

# if code is in Java

    if language == 'Java':
        with open("test.java", 'w') as file:
            file.write(code)

# if code is in Python

    if language == 'Python':
        with open("test.py", 'w') as file:
            file.write(code)


# dummy code stired in string variable x
x= "import socket \nimport os\nimport subprocess\nimport sys"



# calling judge function

judge(x, "IAM", "123", "Python");
