import json

data = None
with open('books.json') as file:
	data = json.load(file)

new_data = []
for id,book in enumerate(data):
	new_data.append(
		{
		'id': id,
		'author': book['author'],
		'language': book['language'],
		'title': book['title'],
		}
	)

print(new_data)
with open('books_list.json', 'w') as file:
	json.dump(new_data, file, indent = 4) 
