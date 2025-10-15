from elasticsearch import Elasticsearch

es = Elasticsearch(
    "https://localhost:9200",
    basic_auth=("elastic", "154615"),
    verify_certs=False  # если сертификат самоподписанный
)


if es.ping():
    print("Успешное подключение к Elasticsearch!")
else:
    print("Ошибка подключения.")
