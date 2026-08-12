from .base_exporter import BaseExporter
from ..model.сoin_model import CoinModel
from .exporter_factory import ExporterFactory


@ExporterFactory.register_exporters("html")
class HtmlExporter(BaseExporter):
    def export(self, data: list[CoinModel], filepath):
        with open(filepath, "w", encoding="utf-8") as f:
            table_rows = '\n'.join([f'<tr><td>{coins.name}</td><td>{coins.time}</td><td>{coins.price}</td><td>{coins.source}</td></tr>'
                                    for coins in data])
            html_content = f"""<!DOCTYPE html>\n
            <html>\n
                <head>\n
                    <meta charset="utf-8">\n
                    </head>\n
                        <body>\n
                            <table>\n
                                <thead>\n
                                    <tr>\n
                                        <th>Name</th>\n
                                        <th>Time</th>\n
                                        <th>Price</th>\n
                                        <th>Source</th>\n
                                    </tr>\n
                                </thead>\n
                                <tbody>
                                    {table_rows}\n
                                </tbody>\n
                            </table>\n
                        </body>\n
            </html>"""
            f.write(html_content)