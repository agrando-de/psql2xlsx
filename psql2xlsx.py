import psycopg2
from openpyxl import Workbook


hostname = 'localhost'
username = 'postgres'
password = ''
database = ''
filename = ''


def run_query(conn):
    cur = conn.cursor()
    cur.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'public'")
    return [tup[0] for tup in cur.fetchall()]


def write_table_data(conn, table_name, wb):
    cur = conn.cursor()

    # Get column names
    cur.execute("SELECT COLUMN_NAME FROM information_schema.columns WHERE table_schema = 'public' AND table_name = '{}'".format(table_name))
    column_names = [column_info[0] for column_info in cur.fetchall()]

    # Get data
    cur.execute('SELECT * FROM "{}"'.format(table_name))
    table_data = cur.fetchall()

    sheet = wb.create_sheet(title=table_name)
    sheet.append(column_names)
    for data_row in table_data:
        sheet.append(data_row)


def main():
    conn = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
    public_table_names = run_query(conn)

    wb = Workbook()
    # Remove the 1st sheet (automatically created)
    wb.remove(wb.active)
    for table_name in public_table_names:
        write_table_data(conn, table_name, wb)
    conn.close()
    wb.save(filename=filename)


if __name__ == '__main__':
    main()
