class CSSSelectorAnalysis:
    """
    Beautifulsoup4のelementからCSSセレクターを取得する
    """

    def get_attr_value(self, elem):
        '''
        CSSセレクターの１セレクタ名を取得する
        '''
        id = elem.attrs.get('id')
        if not str:
            return '#'+id
        # TODO 要素名だけの場合、クラス名も付けたほうが良さそう「 div.contentsWrapper.clearfix.inner」
        additional_class = ""
        if elem.attrs.get('class') is not None:
            additional_class = '.'+'.'.join(elem.attrs.get('class'))
        return elem.name+additional_class

    def analysis_css_selector(self, elem, names):
        '''
        CSSセレクタ名をコレクトする
        '''
        if elem.parent is None:
            names.append(self.get_attr_value(elem))
            return
        names.append(self.get_attr_value(elem))
        self.analysis_css_selector(elem.parent, names)

    def get_css_selector(self, elem):
        '''
        要素からCSSセレクターを取得する
        '''
        names = []
        self.analysis_css_selector(elem, names)
        names.reverse()
        names = ' > '.join(names[1:])
        return names


from bs4 import BeautifulSoup
import requests
res = requests.get("https://developer.mozilla.org/ja/docs/Web/CSS/CSS_Selectors")

soup = BeautifulSoup(res.text, 'html.parser')
elem = soup.select_one("#content > article > h1")
print(elem)

csa = CSSSelectorAnalysis()
selector = csa.get_css_selector(elem)
print(selector)
elem = soup.select_one(selector)
print(elem)