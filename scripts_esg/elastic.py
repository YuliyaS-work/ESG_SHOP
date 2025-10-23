from elasticsearch import Elasticsearch

# Подключение к локальному серверу
es = Elasticsearch("https://localhost:9200",  basic_auth=("elastic", "f3hRbYAUlIGJs*SDMrgn"), verify_certs=False)

# Проверка подключения
if es.ping():
    print("Успешное подключение к Elasticsearch!")
else:
    print("Ошибка подключения.")
