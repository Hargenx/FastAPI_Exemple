import requests

print(
    'POST: {}\n\n'.format(
    requests.post(
    'http://127.0.0.1:8000',
    json={'id':5, 'name':'glue', 'price':18.0, 'description':'A glued thing', 'count':22, 'category':'comsumables'},
    ).json()
    )
    )
print('GET ALL: {}\n\n'.format(requests.get('http://127.0.0.1:8000').json()))

print('GET ONE: {}\n\n'.format(requests.get('http://127.0.0.1:8000/items/1').json()))

print('PUT: {}\n'.format(requests.put('http://127.0.0.1:8000/items/5?count=20').json()))
print('GET ALL: {}\n\n'.format(requests.get('http://127.0.0.1:8000').json()))


print('DELETE: {}\n'.format(requests.delete('http://127.0.0.1:8000/items/5').json()))
print('GET ALL: {}\n\n'.format(requests.get('http://127.0.0.1:8000').json()))

print('PESQUISA NOMEADADE: {}\n\n'.format(requests.get('http://127.0.0.1:8000/items?name=Nails').json()))