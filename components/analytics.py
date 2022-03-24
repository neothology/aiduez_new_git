import ipyvuetify as v

class TabularaAnalyticsBasicinfo(v.Container):
    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key
        super().__init__(
            style_ = "min-width:100%; min-height:100%; display:flex; flex-direction:column;",
            children = [self.context_key]
        )

class TabularAnalyticsScatter(v.Container):
    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key
        super().__init__(
            style_ = "min-width:100%; min-height:100%; display:flex; flex-direction:column;",
            children = [self.context_key]
        )

class TabularAnalyticsHeatmap(v.Container):
    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key
        super().__init__(
            style_ = "min-width:100%; min-height:100%; display:flex; flex-direction:column;",
            children = [self.context_key]
        )

class TabularAnalyticsBoxplot(v.Container):
    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key
        super().__init__(
            style_ = "min-width:100%; min-height:100%; display:flex; flex-direction:column;",
            children = [self.context_key]
        )

class TabularAnalyticsDensity(v.Container):
    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key
        super().__init__(
            style_ = "min-width:100%; min-height:100%; display:flex; flex-direction:column;",
            children = [self.context_key]
        )

class TabularAnalyticsWordCloud(v.Container):
    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key
        super().__init__(
            style_ = "min-width:100%; min-height:100%; display:flex; flex-direction:column;",
            children = [self.context_key]
        )

class TabularAnalyticsDimensionReduction(v.Container):
    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key
        super().__init__(
            style_ = "min-width:100%; min-height:100%; display:flex; flex-direction:column;",
            children = [self.context_key]
        )

class TabularAnalyticsClustering(v.Container):
    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key
        super().__init__(
            style_ = "min-width:100%; min-height:100%; display:flex; flex-direction:column;",
            children = [self.context_key]
        )

class TabularAnalyticsDataSample(v.Container):
    def __init__(self, app_context, context_key, **kwargs):
        self.app_context = app_context
        self.context_key = context_key
        super().__init__(
            style_ = "min-width:100%; min-height:100%; display:flex; flex-direction:column;",
            children = [self.context_key]
        )