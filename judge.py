def create_file(code, language, file_name):

# if code is in C++
    if language == 'C++':
        with open(file_name , "w") as file:
            file.write(code)
            return file_name

# if code is in C
    if language == 'C':
        with open(file_name, 'w') as file:
            file.write(code)
            return file_name

# if code is in Java
    if language == 'Java':
        with open(file_name, 'w') as file:
            file.write(code)
            return file_name

# if code is in Python
    if language == 'Python':
        with open(file_name, 'w') as file:
            file.write(code)
            return file_name


# dummy code stired in string variable x
x = "import socket \nimport os\nimport subprocess\nimport sys"


def judge(code, problem_code, run_id, client_id, language):

    if language == 'C++':
        file_name = client_id + " " + run_id + " "  + " " + problem_code + '.cpp'

    if language == 'C':
        file_name = client_id + " " + run_id + " "  + " " + problem_code + '.c'

    if language == 'Java':
        file_name = client_id + " " + run_id + " "  + " " + problem_code + '.java'

    if language == 'Python':
        file_name = client_id + " " + run_id + " "  + " " + problem_code + '.py'

    create_file(code, language, file_name)








# calling judge function
judge(x, "KCAT", "prak", "123", "C++");
