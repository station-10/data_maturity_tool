from modules.data_collection import collect_data


print("Welcome to Station10's Data Maturity Calculator")
print("What is the name of the company you would like to assess?")
company_name = input()
print("Please enter the homepage URL for " + company_name)
input_url = input()
print("Thank you")
data = collect_data(input_url)
print("This is what I can tell you about " + company_name+":")

for i in data[0]:
    print(i,": ", data[0][i])

for i in data[1]:
    print(i,": ", data[1][i])


