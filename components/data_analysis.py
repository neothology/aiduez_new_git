import numpy as np
import bqplot as bq
from bqplot import pyplot as plt
from bqplot import ColorScale
from ipywidgets import AppLayout
from IPython.display import display
import plotly.express as px
import plotly.graph_objects as go

import traitlets
import ipyvuetify as v
import ipywidgets as widgets
#from common.font_utils import get_korean_font_path

color_options=[ "OrRd", "PuBu", "BuPu", "Oranges", "BuGn", "YlOrBr", "YlGn", "Reds", "RdPu", "Greens", "YlGnBu", "Purples", "GnBu", "Greys", "YlOrRd", "PuRd", "Blues", "PuBuGn", "viridis", "plasma", "inferno", "magma",]

class CreateAnalticsChart():
    def __init__(self, app_context):
        self.df = app_context.tabular_dataset.current_data
        self.rowChosen = 100
        self.x_colname = ""
        self.y_colname = ""
        self.color='RdBu'
        self.hue= ""
        # 수치형 컬럼 선택지 조정
        self.columnChoices=[]
        for colname in self.df.columns.to_list():
            if self.df[colname].dtype=="int64" or self.df[colname].dtype=="float64":
                self.columnChoices.append(colname)

    #히트맵 그래프 얻기
    def _get_heatmap_plot(self, color, rowChosen, colnames):
        self.rowChosen =rowChosen
        labels=colnames

        corr = self.df.head(self.rowChosen).filter(labels).corr()

        fig = go.Figure(go.Heatmap(z=corr, x=labels, y=labels,
                                   colorscale=color, reversescale=True, zmid=0))
        
        fig.update_layout(title='Heatmap', yaxis=dict(autorange='reversed'), width=599, height=599) 
        #fig.write_image("fig1forTEST.png")
        return go.FigureWidget(fig)
    
    def _get_box_plot(self, rowChosen, x_colname, y_colname, hue):
        self.rowChosen = rowChosen
        if self.rowChosen < 100:
            return "최소 100개 이상의 샘플을 선택해 주세요."

        if hue == '-':
            hue = None

        return go.FigureWidget(self.df
                .pipe(lambda dff: dff.dropna(subset=[hue]) if hue is not None else dff)
                .head(self.rowChosen)
                .pipe(px.box, x=x_colname, y=y_colname, color=hue, title='Boxplot'))
    
    def _get_scatter_plot(self, y_colname, hue, rowChosen):
        self.hue = hue
        self.y_colname = y_colname
        self.rowChosen = rowChosen

        print(len(self.y_colname))
        if len(self.y_colname) > 10:
            return "최대 10개 컬럼에 대한 산포도 시각화가 가능합니다."

        if self.hue == '-':
            self.hue = None

        df = (self.df
                .pipe(lambda dff: dff.dropna(subset=[self.hue]) if self.hue is not None else dff)
                .pipe(lambda dff: dff.astype({self.hue: 'object'}) if self.hue is not None else dff)
                .head(self.rowChosen))

        fig = go.Figure(px.scatter_matrix(df, dimensions=self.y_colname, color=self.hue, title='Scatter plot'))
        fig.update_layout(width=599, height=599)
        return go.FigureWidget(fig)
    '''
    def _get_wordcloud_plot(self ,rowChosen, color):
        from wordcloud import WordCloud
        from konlpy.tag import Komoran
        from collections import Counter

        self.rowChosen = rowChosen
        self.color = color

        komoran = Komoran()
        words_list = []
        for sentence in self.df.loc[:self.rowChosen, self.x_objects.value]:
            try:
                for word, tag in komoran.pos(sentence):
                    if tag in ["NNG", "NNP", "VA"]:
                        words_list.append(word)
            except:
                continue
        if len(words_list) != 0:
            most_words = Counter(words_list).most_common(40)
            wc = WordCloud(font_path=str(get_korean_font_path()), background_color=self.color)
            cloud = wc.generate_from_frequencies(dict(most_words)).to_array()
            fig = px.imshow(cloud)
            fig.update_xaxes(visible=False)
            fig.update_yaxes(visible=False)
            return go.FigureWidget(fig)
        else:
            return None
    '''    
    def _get_density_plot(self, x_colname, hue, color):
        self.x_colname= x_colname
        self.hue = hue
        self.color = color
        try:
            self.color = None if self.hue is None or self.hue == '-' else hue
            data = self.df.filter([self.x_colname]) if self.color is None else self.df.filter([self.x_colname, self.color])
            fig = px.histogram(data, x=self.x_colname, color=self.color, hover_data=data.columns)
            fig.update_layout(title_text='분포차트 (Density Plot)')
            return go.FigureWidget(fig)
        except:
            return 'Hue 그룹별 데이터가 특정 값에 편중되어 있습니다. 다른 Hue 값을 선택해 주세요.'
    
'''
class MyComponent(v.VuetifyTemplate):
    def __init__(self):
        self._df= None

    colors = traitlets.List(traitlets.Unicode(), default_value=color_options).tag(sync=True)
    selectedColor = traitlets.Unicode(default_value=None, 
    allow_none=True).tag(sync=True)
    
    chartmaker= CreatePlotlyChart(self._df)
    chart= chartmaker._get_heatmap_plot("Greys")

    def on_change_toggle_with_color_option_selector(widget, event, data):
        chart=chartmaker._get_heatmap_plot(widget.v_model)
        chart.update_layout(paper_bgcolor="LightSteelBlue")

    chart_src = traitlets.Any(default_value=None).tag(sync=True)
    @traitlets.default('template')
    def _template(self):
        return 
        <template>
            <v-select label="Colors" :items="colors" v-model="selectedColor"/>
            <v-img
            max-height="150"
            max-width="250"
            :src=chart_src
            ></v-img>
        </template>
        <script>
        module.exports = {
            methods: {
            },
            computed: {
            },
            data: {
                src: "fig1forTEST.png"
            }
        }
        </script>

    def set_df(self, value):
        self._df= value
'''