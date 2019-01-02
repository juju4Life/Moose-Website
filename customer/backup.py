from customer.models import Customer


data = Customer.objects.all()
file = open('credit.txt', 'w')

for each in data:
	name = each.name
	credit = each.credit
	medals = each.medal
	print(name, credit)
	file.write(f'{name}: Store Credit({credit}, Medals{medal})\n')
