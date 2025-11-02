import json
import sys
import requests
from utils import prepare_request
from utils import ak, sk

method = 'POST'
DOMAIN = "api-knowledgebase.mlp.cn-beijing.volces.com"
path = '/api/knowledge/doc/add'

request_params = {
    "collection_name": "MyNewCollection",
    "project": "",
    "add_type": "url",
    "doc_id": "QA_dataset",
    "doc_name": "招聘数据集",
    "doc_type": "xlsx",
    "url":"http://118.145.187.17:38287/api/v1/download-shared-object/aHR0cDovLzEyNy4wLjAuMTo5MDAwL2NhaWppYW4vUUEuZmFxLnhsc3g_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1HMFFVS1ZNWVFOVlU1NjM3RzUzVCUyRjIwMjQxMTE4JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI0MTExOFQwMjU1MDVaJlgtQW16LUV4cGlyZXM9NDMxOTkmWC1BbXotU2VjdXJpdHktVG9rZW49ZXlKaGJHY2lPaUpJVXpVeE1pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SmhZMk5sYzNOTFpYa2lPaUpITUZGVlMxWk5XVkZPVmxVMU5qTTNSelV6VkNJc0ltVjRjQ0k2TVRjek1UazBNRFUwT0N3aWNHRnlaVzUwSWpvaWJXbHVhVzloWkcxcGJpSjkuOFI3X1Zzd0t2Uzl6QXVYeERlbmtzbFBGUlhNTWhab0lqZ2ZqR1QtaldodnE3OHM0LTNQdFN5ajFqb0ZQX2UzaTFUU0ZsSU1GSWpob285WU5VNmtWLUEmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JnZlcnNpb25JZD1udWxsJlgtQW16LVNpZ25hdHVyZT00MDU4MWJlYjZkMTA0ZWQwN2Q0NTQ4ZjllYjQ2MjZjZjQ4MWU5YTFiZjQyMGUxMzJiNDNlZGYxMGRiY2M3YTZi",   "meta": [
        {"field_name": "category", "field_type": "string", "field_value": "招聘行业"},
            ]
}
info_req = prepare_request(method=method, path=path, ak=ak, sk=sk, data=request_params)
res = requests.request(method=info_req.method,
                       url="https://{}{}".format(DOMAIN, info_req.path),
                       headers=info_req.headers,
                       data=info_req.body)
print(res.text)



#另一种方式
"""
def create_request_params(collection_name, doc_id, doc_name, doc_url, category):
    return {
        "collection_name": collection_name,
        "project": "",
        "add_type": "url",
        "doc_id": doc_id,
        "doc_name": doc_name,
        "doc_type": "pdf",
        "url": doc_url,
        "meta": [{"field_name": "category", "field_type": "string", "field_value": category}]}

# 示例调用
request_params = create_request_params(collection_name="unstructure_Data",
                                       doc_id="pdf_003",
                                       doc_name="pdf_version2",
                                       doc_url="http://example.com/doc2.pdf",
                                       category="电力行业")
"""