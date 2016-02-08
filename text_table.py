#!/usr/bin/env python2
# -*- coding: utf-8 -*-

def parse_text_table(text):
    # First: split into rows.
    current_row = []
    table_rows = []
    for line in text.lstrip('\n').rstrip().split('\n') + ['\n']:
        # Don't strip left portion of the line
        # as this could screw up the indentation.
        line = line.rstrip()
        if line:
            # Not a blank line, add to current row.
            current_row.append(line)
            continue
        # Blank line, start a new row if needed.
        if current_row:
            table_rows.append(current_row)
            current_row = []
    # Then, split each row into cells.
    table = []
    for row in table_rows:
        row_cells = []
        cell_start_column = 0
        max_line_width = max(len(line) for line in row)
        previous_column_was_blank = None
        for col in range(max_line_width + 1):
            # Is the column blank?
            column_is_blank = True
            for line in row:
                if col < len(line) and not line[col].isspace():
                    column_is_blank = False
                    break
            # Split into cells on blank columns.
            if (
                previous_column_was_blank is not None and
                column_is_blank != previous_column_was_blank
            ):
                if column_is_blank:
                    cell = '\n'.join(line[cell_start_column:col]
                                     for line in row)
                    row_cells.append(cell)
                else:
                    cell_start_column = col
            previous_column_was_blank = column_is_blank
        table.append(row_cells)
    return table


if '__main__' == __name__:

    table_text = u'''

       □□□□□□□  _   □□□■□□□  a
          ■            □
      

    □■■■■□□  b   □■□■□□■  c     □□□□□□□ _
       □            ■              ■

    '''

    print table_text

    table = parse_text_table(table_text)

    for r, row in enumerate(table):
        for c, col in enumerate(row):
            print '(%u,%u):\n\n%s\n' % (r, c, row[c])

