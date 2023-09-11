def logic(li):
    list_items = li[0]
    dictionary = li[1]
    if not list_items:
        print('if')
        return 0
    elif isinstance(list_items[0], list):
        print('elif')
        sum_of_element = logic((list_items[0], dictionary))
        sum_of_rest_list = logic((list_items[1:0], dictionary))
        return sum_of_element + sum_of_rest_list
    else:
        print('else')
        op = 'addition'
        element = list_items[0]
        if dictionary.get(element) == 'true':
            element = 0
        elif dictionary.get(element) == 'false':
            element = 1
        elif element == 'NOT':
            element = 1
        elif element == 'AND':
            element = 0
        elif element == 'true':
            element = 0
        elif element == 'false':
            element = 1
        elif element == 'OR':
            return 'OR'
            
        sum_of_rest_list = logic((list_items[1:], dictionary))
        if sum_of_rest_list == 'OR':
            op = 'mult'
            sum_of_rest_list = logic((list_items[2:], dictionary))

        if (op == 'addition'):
            return element + sum_of_rest_list
        else:
            op == 'mult'
            return element * sum_of_rest_list


test_list = (["NOT", ["NOT", ["NOT", ["cat_asleep", "AND", ["NOT", "cat_asleep"]]]]],
               {"cat_asleep": "false"})
print(logic(test_list))
# print(logic(test_list))

# def interpret(input):
#     li = input[0]
#     dictionary = input[1]
#     test = dictionary.get(li[0])
#     return test
# print(interpret(test_list))

# def sum_of_any_level_list(seq):
#     if not seq:
#         return 0
#     elif isinstance(seq[0], list):
#         sum_of_first_element = sum_of_any_level_list(seq[0])
#         sum_of_rest_of_list = sum_of_any_level_list(seq[1:])
#         return sum_of_first_element + sum_of_rest_of_list
#     else:
#         sum_of_first_element = seq[0]
#         sum_of_rest_of_list = sum_of_any_level_list(seq[1:])
#         return sum_of_first_element + sum_of_rest_of_list
    
# sum_of_any_level_list(test_list)