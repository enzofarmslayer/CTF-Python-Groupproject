def split_it(string):
  part1 = ''
  part2 = ''
  for i in string:
    if i.islower() == True or i in ['_', '.']:
      part1 += i
    elif i.isupper() == True or i in ['|', ' ']:
      part2 += i
    else:
      continue
  return part1, part2
first_message,second_message=split_it("hTEeSj_CO")

def split_first(string):
  if not string:
    return []
    
  recurse_result = split_first(string[1:])

  if string[0].islower() == True or string[0] in ['_', '.']:
    return recurse_result + [string[0]]
  else:
    return recurse_result
  
def split_second(string):
  if not string:
    return []
    
  recurse_result = split_second(string[1:])

  if string[0].isupper() == True or string[0] in [' ']:
    return recurse_result + [string[0]]
  else:
    return recurse_result
  
def turn_to_string(string):
  conc_string = ''
  rev_string = string[::-1]
    
  final_string = conc_string.join(rev_string)

  return final_string
  
def split_rec(string):
  first_part = split_first(string)
  second_part = split_second(string)

  final_string_1 = turn_to_string(first_part)
  final_string_2 = turn_to_string(second_part)

  return final_string_1, final_string_2

print(split_rec("'lMiED)teD5E,_hLAe;Nm,0@Dli&Eg ,#4aI?rN@T§&e7#4E #<(S0A?<)NT8<0'"))

