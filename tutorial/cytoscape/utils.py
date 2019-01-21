from textwrap import dedent

import dash_core_components as dcc
import dash_html_components as html
from tutorial import styles



def CreateDisplay(scope):
    def Display(example_string):
        return html.Div([
            dcc.SyntaxHighlighter(
                dedent(example_string).strip(),
                language='python',
                customStyle={'marginBottom': 10, 'borderLeft': 'thin #C8D4E3 solid'}
            ),
            html.Div(
                children=eval(dedent(example_string), scope),
                style={
                    'border': 'thin lightgrey solid',
                    'margin-top': '-10px',
                    'padding': '15px'
                }
            )
        ])
    return Display


def merge(*args):
    merged = {}
    for arg in args:
        for key in arg:
            merged[key] = arg[key]
    return merged


def section_title(title):
    return html.H4(title, style={"marginTop": "20px"})


def html_table(
    df,
    base_column_style={},
    table_style={},
    column_style={},
    cell_style={},
    cell_style_by_column={},
    header_style={},
    header_style_by_column={},
    row_style={},
    row_style_by_index={},
    odd_row_style={},
    conditional_cell_style=(lambda cell, column: {})
):
    header = []
    for column in df.columns:
        header.append(
            html.Th(
                column,
                style=merge(
                    row_style,
                    base_column_style,
                    cell_style,
                    column_style.get(column, {}),
                    header_style,
                    header_style_by_column.get(column, {}),
                ),
            )
        )

    rows = []
    for i in range(len(df)):
        row = []
        for column in df.columns:
            row.append(
                html.Td(
                    df.iloc[i][column],
                    style=merge(
                        row_style,
                        row_style_by_index.get(i, {}),
                        odd_row_style if i % 2 == 1 else {},
                        cell_style,
                        cell_style_by_column.get(column, {}),
                        conditional_cell_style(df.iloc[i][column], column)
                    ),
                )
            )
        rows.append(html.Tr(row))

    return html.Table(
        [html.Thead(header), html.Tbody(rows)],
        style=merge(table_style, {"marginTop": "20px", "marginBottom": "20px"}),
    )


def PythonSnippet(code):
    if code and code[0] == '\n':
        code = code[1:]

    return dcc.SyntaxHighlighter(
        dedent(code),
        language='python',
        customStyle=styles.code_container
    )