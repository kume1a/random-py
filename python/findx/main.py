import random
import itertools
import requests
import json
import csv


def not_contains_tokens(problems, problem):
    for p in problems:
        if p['tokens'] == problem['tokens']:
            return False

    return True


def generate_problems(operators, start, end):
    res = []

    args = list(map(lambda e: range(start, end), range(len(operators) + 1)))

    index = 0
    for tokens in itertools.product(*args):
        index += 1

        tex = ''

        shuffled_tokens = list(tokens).copy()
        random.shuffle(shuffled_tokens)

        for i, token in enumerate(shuffled_tokens):
            tex += str(token)
            if i != len(tokens) - 1:
                tex += operators[i]

        sorted_tokens = list(tokens).copy()
        sorted_tokens.sort()
        problem = {
            'tex': tex,
            'tokens': sorted_tokens
        }

        if not_contains_tokens(res, problem):
            res.append(problem)

    return res


def get_answer(tex):
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'application/json',
        # 'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL3d3dy5zeW1ib2xhYi5jb20iLCJ1ZGlkIjpudWxsLCJzdWJzY3JpYmVkIjpmYWxzZSwiZXhwIjoxNzA0NDQ1NzUzfQ.Fea4q7GnRp_qNexd3_FyBOBFuDKSCnp2pL_s7G-fot8',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }

    data = {
        'origin': 'input',
        'language': 'en',
        'query': tex,
        'referer': 'https://www.symbolab.com/solver/step-by-step'
    }

    res1 = requests.post('https://www.symbolab.com/pub_api/bridge/solution', headers=headers, data=data)

    return json.loads(res1.text)['solution']['solution']['default']


def main():
    # read csv answerFunctions.csv
    with open('answerFunctions.csv', 'r') as file:
        reader = csv.reader(file)
        answer_functions = list(reader)

        for math_sub_field_id in [4,5,6,7]:
            for answer_function in answer_functions[1:]:
                func = answer_function[2]
                weight = answer_function[3]
                condition = answer_function[4]

                conditionFormatted = '\'' + condition + '\'' if condition else 'NULL'

                print(f"""
                    INSERT INTO "answerFunctions" (func, weight, condition, "mathSubFieldId") VALUES ('{func}', {weight}, {conditionFormatted}, {math_sub_field_id});
                    """)


if __name__ == '__main__':
    main()
