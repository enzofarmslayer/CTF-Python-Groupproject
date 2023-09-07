def logic(list_items, dictionary):
    # list_items = li[0]
    # dictionary = li[1]
    if isinstance(list_items, str):
        element = list_items
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
        return element
    elif not list_items:
        print('if')
        return 0
    elif isinstance(list_items[0], list):
        print('elif')
        sum_of_element = logic(list_items[0], dictionary)
        sum_of_rest_list = logic(list_items[1:0], dictionary)
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
            return 'AND'
        elif element == 'true':
            element = 0
        elif element == 'false':
            element = 1
        elif element == 'OR':
            return 'OR'
            
        sum_of_rest_list = logic(list_items[1:], dictionary)
        if sum_of_rest_list == 'OR':
            op = 'mult'
            sum_of_rest_list = logic(list_items[2:], dictionary)
        elif sum_of_rest_list == 'AND':
            op = 'sub'
            sum_of_rest_list = logic(list_items[2:], dictionary)

        if (op == 'addition'):
            return element + sum_of_rest_list
        elif op == 'mult':
            return element * sum_of_rest_list
        else:
            if element + sum_of_rest_list != 0:
                return 1
            return element + sum_of_rest_list
        
def interpret(list_items, dictionary):
    result = logic(list_items, dictionary)
    print(result)
    if result % 2 == 1:
        return "false"
    else:
        return "true"
    
print(interpret(['false', 'AND', 'false'], {}))
