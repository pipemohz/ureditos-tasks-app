import csv

def email_csv_report_writer(user_id: str, username: str, zone: str, office: str, course: str, csv_log: str):
    """
    Writes a row in csv report with results of query to database.

    `user_id: str`
        User id string.
    `username: str`
        Username string.
    `zone: str`
        Zone string.
    `office: str`
        Office string.
    `course: str`
        Course name string.
    `csv_log: str`
        Path to the csv report to append records.
    """
    with open(csv_log, mode='a', newline='') as csv_file:
        
        fields = ['Id', 'Nombre asesor(a)', 'Zona',
                  'Oficina', 'Nombre curso', 'Estado']
        csv_writer = csv.DictWriter(csv_file, fieldnames=fields)

        csv_writer.writerow(
            {'Id': f"CC:{user_id}", 'Nombre asesor(a)': username, 'Zona': zone, 'Oficina': office, 'Nombre curso': course, 'Estado': 'Inscrito'})