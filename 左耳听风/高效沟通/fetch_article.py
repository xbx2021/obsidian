import urllib.request
import urllib.parse
import json

url = "https://time.geekbang.org/serv/v1/article"

headers = {
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json",
    "Cookie": "_ga=GA1.2.644228871.1770960692; LF_ID=e3adbea-bc1e4ce-05d766d-33c163e; mantis5539=4875ed2f3572442993073522164d4d74@5539; _ga_MTX5SQH9CV=GS2.2.s1771055914$o5$g1$t1771056086$j60$l0$h0; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2219ddd9b332a42a-08ecc7f1ad889f-26061851-1821369-19ddd9b332b67d%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_landing_page%22%3A%22https%3A%2F%2Flive.geekbang.org%2Froom%2F2513%22%7D%2C%22%24device_id%22%3A%2219ddd9b332a42a-08ecc7f1ad889f-26061851-1821369-19ddd9b332b67d%22%7D; _tea_utm_cache_20000743={%22utm_source%22:%22geektime_search%22%2C%22utm_medium%22:%22geektime_search%22%2C%22utm_campaign%22:%22geektime_search%22%2C%22utm_term%22:%22geektime_search%22%2C%22utm_content%22:%22geektime_search%22}; gksskpitn=6c6d4d7d-864a-40b3-b095-b54e5dcb9d93; HMACCOUNT=1BC4FF6002AD57C7; _gid=GA1.2.724136422.1779078235; Hm_lvt_022f847c4e3acd44d4a2481d9187f1e6=1777529941,1778636182; Hm_lvt_59c4ff31a9ee6263811b23eb921a5083=1777529941,1778636182; gk_process_ev={%22count%22:1%2C%22utime%22:1779327157460%2C%22referrer%22:%22https://time.geekbang.org/column/article/13067%22%2C%22target%22:%22page_geektime_login%22}; GCID=08b75b5-6dd716c-c85c534-e7b9a2a; _ga_JW698SFNND=GS2.2.s1779327161$o4$g0$t1779327161$j60$l0$h0; GRID=08b75b5-6dd716c-c85c534-e7b9a2a; GCESS=Bg0BAQIEvGAOaggBAwQEAI0nAAYEFWgp6QUEAAAAAAcEE6IjawwBAQEIOr1DAAAAAAAJAQELAgYAAwS8YA5qCgQAAAAA; tfstk=g4-rF9q3j0nrDllMQdjE7BLkXmSRfMlsLH1CKpvhF_foybCeTdObAwxSekleTB7BNpj5-W5Di_OWPpwJkC9gV3gRAkSRvMcs1ciseLIdx8X5F72Rm9XUrD13rijRdPv_bKm6eLemdZ1jxcgeyBHVt6AhrZXcBsqlKBXlixWhd743qBvm3sBLxkfuqtqcp9EhxMAHnxWdi6jhrBvm39CctXrvwBF1IaD5KGjlTDSAz1vlglvXDTAgyL14cotVYa5gYsr3xnWJKbZvUluCsFC55sdmcuSen9RNQQPmgMv22h7DqjEe_I8G0tLxTy5w-LT9-ZkoqKSPaN-fl84F4eAJYaLzpApcqILO6a0xMt-Wfw5OuSckhK5l7eRSMkfW7KAV5nNbfivMuiSr_WBmeEtpzW4FrtBV1xk4DdRRnYM-t9zLJZbG31MR-yUdrtBV1xk4JyQ8jt5sewf..; acw_tc=276ae9b017793297258872653e0eb61fcdfffd1e29c57b4793ff5f2ab3727d; _gat=1; __tea_cache_tokens_20000743={%22web_id%22:%227630760694203561229%22%2C%22user_unique_id%22:%224439354%22%2C%22timestamp%22:1779331497836%2C%22_type_%22:%22default%22}; Hm_lpvt_59c4ff31a9ee6263811b23eb921a5083=1779331498; Hm_lpvt_022f847c4e3acd44d4a2481d9187f1e6=1779331498; _ga_03JGDGP9Y3=GS2.2.s1779330749$o31$g1$t1779331498$j60$l0$h0; SERVERID=1fa1f330efedec1559b3abbcb6e30f50|1779331499|1779327130",
    "Origin": "https://time.geekbang.org",
    "Referer": "https://time.geekbang.org/column/article/13067",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36",
    "X-GEEK-REQ-ID": "7fd588b3be8e4c1a9ae18337f2458989@1@web"
}

data = json.dumps({
    "id": "13067",
    "include_neighbors": True,
    "is_freelyread": True
}).encode('utf-8')

try:
    req = urllib.request.Request(url, data=data, headers=headers, method='POST')
    with urllib.request.urlopen(req) as response:
        status_code = response.getcode()
        print(f"Status Code: {status_code}")
        response_headers = dict(response.info())
        print(f"Response Headers: {response_headers}")
        response_text = response.read().decode('utf-8')
        print(f"Response Text: {response_text}")
        if response_text:
            try:
                json_data = json.loads(response_text)
                print(f"Response JSON: {json.dumps(json_data, indent=2, ensure_ascii=False)}")
            except json.JSONDecodeError:
                print("Response is not valid JSON")
except Exception as e:
    print(f"Error: {e}")
