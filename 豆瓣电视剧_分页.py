import requests
import json


class DouBanDSJSpider(object):

    def __init__(self):
        # 准备数据
        # 请求url
        self.url = 'https://m.douban.com/rexxar/api/v2/subject_collection/filter_tv_{}_hot/items?start={}&count=18&loc_id=108288'
        # 请求头
        # Referer 是随着电视剧的分类而变化的
        # 国产剧：chinese   港剧：hongkong  动漫：animation
        self.headers = {
            'Referer': '',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Mobile Safari/537.36',
        }

    def get_data_from_url(self, url, ref_cg):
        self.headers['Referer'] = ref_cg
        response = requests.get(url, headers=self.headers)
        return response.content

    def get_dsj_list(self, json_str):
        dic = json.loads(json_str.decode())

        start = dic['start']
        count = dic['count']
        total = dic['total']

        next_start = start + count
        return dic['subject_collection_items'], next_start, total

    def save_dsj_list(self, dsj_list):
        with open("dsj_list.txt", 'a', encoding='utf8') as f:
            for dsj in dsj_list:
                json.dump(dsj, f, ensure_ascii=False)
                f.write("\n")

    def main(self, next_start, cg, category, url_category):
        # 发起请求，获取响应参数
        url = self.url.format(cg, next_start)
        ref_cg = category[url_category.index(cg)]

        json_str = self.get_data_from_url(url, ref_cg)
        # 解析数据
        dsj_list, next_start, total = self.get_dsj_list(json_str)
        # print(dsj_list)

        # 存储电视剧列表到文件里
        self.save_dsj_list(dsj_list)

        return next_start, total

    def run(self):

        # 准备要获取的电视剧类别
        category = ['https://m.douban.com/tv/chinese', 'https://m.douban.com/tv/tvshow', 'https://m.douban.com/tv/animation']
        url_category = ['domestic', 'variety', 'animation']
        for cg in url_category:
            next_start = 0
            while next_start is not None:
                next_start, total = self.main(next_start, cg, category, url_category)
                print(next_start, total)
                if next_start >= total:
                    with open("dsj_list.txt", 'a') as f:
                        f.write('\n')
                    next_start = None


if __name__ == '__main__':
    dsjs = DouBanDSJSpider()
    dsjs.run()

