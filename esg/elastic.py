from elasticsearch import Elasticsearch

es = Elasticsearch(
    "https://localhost:9200",
    # basic_auth=("elastic", "sopjxz3Qvo1KfpjnB0Yi"),
    basic_auth=("elastic", "f3hRbYAUlIGJs*SDMrgn"),
    verify_certs=False  # если сертификат самоподписанный
)


if es.ping():
    print("Успешное подключение к Elasticsearch!")
else:
    print("Ошибка подключения.")
