import ipyvuetify as v
from components.cards import BaseCard
from components.tables import PlainTable
from components.iframe import ChartFrame
import pandas as pd
import numpy as np
import os
from scipy import stats
import plotly.express as px
import plotly.graph_objects as go


class ColumnSummary(BaseCard):

    def _make_summary_data(self, data_name, col:pd.Series):
        special_char = '_'

        self.summary_data = {
            'variable_name': col.name,
            'dtype_str': str(col.dtype),
            'size': len(col),
            'distinct': len(col.unique()),
            'distinct(%)': f'{len(col.unique()) / len(col) * 100:.2f}',
            'missing': col.isna().sum(),
            'missing(%)': f'{col.isna().mean().round(4) * 100:.2f}',
        }

        # datetime values
        if pd.api.types.is_datetime64_any_dtype(col):
            self.summary_data['minimum'] = col.min()
            self.summary_data['maximum'] = col.max()

        # numeric values
        if pd.api.types.is_numeric_dtype(col):
            self.summary_data['minimum'] = col.min()
            self.summary_data['maximum'] = col.max()
            self.summary_data['special_char'] = sum(col == special_char)
            self.summary_data['zeros'] = sum(col == 0)
            self.summary_data['zeros(%)'] = f'{self.summary_data["zeros"] / len(col) * 100: .2f}'
            self.summary_data['mean'] = f'{col.mean():.1f}'
            self.summary_data['median'] = f'{col.median():.1f}'
            self.summary_data['sum'] = f'{col.sum():.1f}'
            self.summary_data['sd'] = f'{col.std():.2f}'
            self.summary_data['skewness'] = f'{col.skew():.2f}'

            # quantiles
            self.summary_data['min'] = col.quantile(0)
            self.summary_data['5-th per.'] = f'{col.quantile(.05):.2f}'
            self.summary_data['Q1'] = f'{col.quantile(.25):.2f}'
            self.summary_data['median'] = f'{col.quantile(.50):.2f}'
            self.summary_data['Q3'] = f'{col.quantile(.75):.2f}'
            self.summary_data['95-th per.'] = f'{col.quantile(.95):.2f}'
            self.summary_data['max'] = col.quantile(1)

        # frequency
        self.summary_data['freq_values'] = ['Value'] + list(col.value_counts().index)[:6]
        self.summary_data['freq_counts'] = ['Count'] + list(col.value_counts())[:6]
        self.summary_data['freq_percent'] = ['Count(%)'] + list((col.value_counts() / len(col) * 100).map('{:.2f}'.format))[:6]
        
        # chart_src
        self.summary_data['chart_dir'] = self.app_context.env_values['tmp_dir'] + f'/column_summary_charts/{data_name}' 
        self.summary_data['chart_src'] = f"{self.summary_data['chart_dir']}/{col.name}.html"
        self.summary_data['chart_title'] = ""

    def _make_chart_data(self, data_name, col):
        def _get_freedman_bins(data, returnas="width", max_bins=50):
            """
            Use Freedman Diaconis rule to compute optimal histogram bin width.
            ``returnas`` can be one of "width" or "bins", indicating whether
            the bin width or number of bins should be returned respectively.
            http://www.jtrive.com/determining-histogram-bin-width-using-the-freedman-diaconis-rule.html
            Parameters
            ----------
            data: np.ndarray
                One-dimensional array.
            Returns: {"width", "bins"}
                If "width", return the estimated width for each histogram bin.
                If "bins", return the number of bins suggested by rule.
            """
            data = np.asarray(data, dtype=np.float_)
            IQR = stats.iqr(data, rng=(25, 75), scale=1.0, nan_policy="omit")
            N = data.size
            bw = (2 * IQR) / np.power(N, 1/3)

            if returnas=="width":
                result = bw
            else:
                datmin, datmax = data.min(), data.max()
                datrng = datmax - datmin
                if bw == 0:
                    bw = 1
                result = int((datrng / bw) + 1)
                result = max_bins if result > max_bins else result
            return result

        if not os.path.exists(self.summary_data['chart_dir']):
            os.makedirs(self.summary_data['chart_dir'])
        if not os.path.isfile(self.summary_data['chart_src']):
            # histogram for numerical
            if pd.api.types.is_numeric_dtype(col):
                bins = _get_freedman_bins(data=col.dropna().values, returnas="bins")
                fig = go.Figure(data=[go.Histogram(x=col.dropna(), nbinsx=bins)])
                fig.update_layout(template = 'plotly_white', bargap=0.01)
                fig.write_html(self.summary_data['chart_src'])
                # fig.write_html(self.summary_data['chart_src_rel'])
                # fig = go.Figure(data=[go.Histogram(x=col.dropna().values, nbins=bins)])

            # bar chart for object/categorical
            if pd.api.types.is_object_dtype(col):
                val_cnt = col.value_counts(ascending=False)
                len_values = len(val_cnt)
                show_bars_cnt = 5

                main_values = val_cnt
                if len_values > show_bars_cnt:
                    main_values = val_cnt[:show_bars_cnt-1]
                    other_value, other_len = val_cnt[show_bars_cnt-1:].sum(), len(val_cnt[show_bars_cnt-1:])
                    main_values[f'Others ({other_len})'] = other_value

                # bar chart from main_values
                fig = px.bar(main_values,  orientation='h', template='plotly_white')
                fig.update_layout(showlegend=False, bargap=0.01)
                fig.write_html(self.summary_data['chart_src'])
                # fig.write_html(self.summary_data['chart_src_rel'])
                self.summary_data['chart_title'] = "Bar 차트"

            # bar chart for datetime
            if pd.api.types.is_datetime64_any_dtype(col):
                pass
    
    def _make_output_data(self, col):
        def _get_key_value_table_data_list(cols):
            temp =  []
            for col in cols:
                temp.extend((
                    [{'value':key, 'style':''} for key in col],
                    [{'value':self.summary_data[key], 'style':'text-align:right'} for key in col],
                ))
            return list(zip(*temp))

        def _get_value_only_table_data_list(keys):
            temp = [ [{'value':x, 'style':'text-align:right'} for x in self.summary_data[key]] for key in keys]
            return list(zip(*temp))

        # for numerical
        if pd.api.types.is_numeric_dtype(col):
            table_headers = ["기술통계/4", "분위수/2", "최빈값/3"]
            table_data_list = []

            # table 1 - 기술통계
            cols1 = [
                ['size', 'distinct', 'distinct(%)', 'missing', 'missing(%)', 'minimum', 'maximum'],
                ['zeros', 'zeros(%)', 'mean', 'median', 'sum', 'sd', 'skewness']
            ]
            table_data_list.append(_get_key_value_table_data_list(cols1))

            # table 2 - 분위수
            cols2= [
                ['min', '5-th per.', 'Q1', 'median', 'Q3', '95-th per.', 'max'],
            ]
            table_data_list.append(_get_key_value_table_data_list(cols2))

            # table 3 - 최빈값
            keys = ['freq_values', 'freq_counts', 'freq_percent']
            table_data_list.append(_get_value_only_table_data_list(keys))

            # chart title
            self.summary_data['chart_title'] = "히스토그램"

        # for object
        elif pd.api.types.is_object_dtype(col):
            table_headers = ["기술통계/4", "최빈값/3"]
            table_data_list = []

            # table 1 - 기술통계
            cols1 = [
                ['size', 'distinct', 'distinct(%)', 'missing', 'missing(%)'],
            ]
            table_data_list.append(_get_key_value_table_data_list(cols1))

            # table 2 - 최빈값
            keys = ['freq_values', 'freq_counts', 'freq_percent']
            table_data_list.append(_get_value_only_table_data_list(keys)) 

            # chart title
            self.summary_data['chart_title'] = "Bar 차트"

        # for datetime
        elif pd.api.types.is_datetime64_any_dtype(col):
            table_headers = ["기술통계/4", "최빈값/3"]
            table_data_list = []

            # table 1 - 기술통계
            cols1 = [
                ['size', 'distinct', 'distinct(%)', 'missing', 'missing(%)'],
            ]
            table_data_list.append(_get_key_value_table_data_list(cols1))

            # table 2 - 최빈값
            keys = ['freq_values', 'freq_counts', 'freq_percent']
            table_data_list.append(_get_value_only_table_data_list(keys)) 

            # chart title
            self.summary_data['chart_title'] = "Bar 차트"

        chart = ChartFrame(
            title = self.summary_data['chart_title'],
            src = os.path.relpath(self.summary_data['chart_src'], self.app_context.env_values['workspace_dir']),
            size = {'width':'100%'}
        )

        return table_headers, table_data_list, chart

    def __init__(self, app_context, context_key, title:str, col:pd.Series, **kwargs):
        self.app_context = app_context
        self.data_name = app_context.tabular_dataset.current_data_name
        self._make_summary_data(self.data_name, col)
        self._make_chart_data(self.data_name, col) 
        table_headers, table_data_list, chart = self._make_output_data(col)

        super().__init__(
            class_ = context_key,
            header_title = title,
            body_items = [v.Row(
                class_ = "",
                style_ = "margin:0",
                children = [PlainTable(header=header, items=items) for header, items in zip(table_headers, table_data_list)] + [chart]
            )],
            body_size = {"width":"1570px", "height":"auto"},
            align = 'center',
        )

    def update_data(self, col:pd.Series):
        self._make_summary_data(self.data_name, col)
        self._make_chart_data(self.data_name, col) 
        table_headers, table_data_list, chart = self._make_output_data(col)

        self.card_body[0].children[0].children = [
            PlainTable(header=header, items=items) for header, items in zip(table_headers, table_data_list)
            ] + [chart]
 