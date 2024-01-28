from site_generator.providers.provider import Provider

CHART_JS_VERSION = "4.4.1"
CHART_JS__ADAPTER_DATE_FNS_VERSION = "3.0.0"


class JS(Provider):
    def get(self) -> list[str]:
        return [self._get_chart_js(), self._get_chart_js_adapter_date_fns()]

    def _get_chart_js(self):
        file_name = "chart_{CHART_JS_VERSION}.js"
        remote_file_url = f"https://cdn.jsdelivr.net/npm/chart.js@{CHART_JS_VERSION}/dist/chart.umd.js"
        return self._download(file_name, remote_file_url).decode("utf-8")

    def _get_chart_js_adapter_date_fns(self):
        file_name = f"chartjs-adapter-date-fns_{CHART_JS__ADAPTER_DATE_FNS_VERSION}.js"
        remote_file_url = f"https://cdn.jsdelivr.net/npm/chartjs-adapter-date-fns@{CHART_JS__ADAPTER_DATE_FNS_VERSION}/dist/chartjs-adapter-date-fns.bundle.min.js"
        return self._download(file_name, remote_file_url).decode("utf-8")
