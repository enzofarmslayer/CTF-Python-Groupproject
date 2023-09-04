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

print(split_it("'lMiED)teD5E,_hLAe;Nm,0@Dli&Eg ,#4aI?rN@T§&e7#4E #<(S0A?<)NT8<0'"))

