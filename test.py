from search import Search
occupation = "Plumber"
test = Search(occupation)

tup =test.avg_salary()
occupation=tup[1]
print (occupation)
average= tup[0]
print(average)
result = test.over_med()

print result