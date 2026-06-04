from clients.amazon_client import AmazonClient
from parsers.detail_page_parser import DetailPage
from parsers.search_result_parser import SearchResult
# from storage.db_manager import .

def main():
    # 1. 获取搜索结果页面的HTML
    search_query = "laptop"
    amazon_client = AmazonClient()
    search_result_html = amazon_client.search(search_query)

    # 2. 解析搜索结果页面，提取每个商品的ASIN、标题、价格等信息
    search_result = SearchResult(search_result_html)
    items = search_result._items()  # 获取所有商品列表项

    for item in items:
        print(f"ASIN: {item.ASIN()}, Title: {item.title()}, Price: {item.price()}")

        # 3. 获取每个商品的详情页面HTML
        detail_page_html = amazon_client.get_detail_page(item.detail_page_link())

        # 4. 解析详情页面，提取品牌、五点描述、图片链接等详细信息
        detail_page = DetailPage(detail_page_html)
        print(f"Brand: {detail_page.brand()}, Title: {detail_page.title()}, Sale Price: {detail_page.sale_price()}")