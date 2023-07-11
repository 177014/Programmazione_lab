#Esame di laboratorio di programmazione di Zhou Wenxiang 11/07/2023
import csv

class ExamException(Exception):
    pass

class CSVFile:

    def __init__(self, name):
        self.name = name

    def get_data(self):
        pass
    

class CSVTimeSeriesFile(CSVFile):

    def get_data(self):
        try:
            with open(self.name, 'r') as csvfile:
                my_file = csv.reader(csvfile)
                next(my_file)                                                                       #Salta la riga dell'intestazione
                time_series = []
                for row in my_file:
                    date, passengers = row
                    try:
                        if int(passengers) <= 0:
                            continue                                                                #Salta le righe con valori di passeggeri non positivi
                        time_series.append([str(date), int(passengers)])                            #Aggiungo sulla lista time_series date come stringa e passengers come inteto
                        
                    except ValueError:
                        continue                                                                    #Salta le righe con valori dei passeggeri non numerici

                years_months = []                                                                   #Lista usata per contrallare le date
                for i in range(len(time_series)-1):
                    elements = time_series[i][0].split('-')
                    if elements[0] != 'date':                                                       #Salta la riga dell'intestazione
                        years_months.append(elements)                                               #Memorizza l'anno e il mese

                for i in range(0,len(years_months) - 1):
                    if int(years_months[i][1]) > 12:
                        raise ExamException("Non posso esserci più di 12 mesi")                     #Alza un'eccezione se un mese è maggiore di 12

                    if years_months[i+1][0] < years_months[i][0]:
                        raise ExamException("Gli anni del file csv non sono in ordine")             #Alza un'eccezione se gli anni non sono in ordine crescente

                    for j in range(1,len(years_months) - 1 - i):
                        if time_series[i][0] == time_series[i+j][0]:
                            raise ExamException("Ci sono date duplicate")                           #Alza un'eccezione se ci sono date duplicate

        except FileNotFoundError:
            raise ExamException("File non trovato")                                                 #Alza un'eccezione se il file non viene trovato

        return time_series

def compute_avg_monthly_difference(time_series, first_year, last_year):

    if not time_series:
        raise ExamException("time_series vuota")                                                    

    try:
        first_year = int(first_year)
        last_year = int(last_year)
        
    except ValueError:
        raise ExamException("Gli anni inseriti non sono numerici interi")                           

    if first_year > last_year:
        raise ExamException("Intervallo di anni non valido")                                        #Alza un'eccezione se il primo anno è maggiore dell'ultimo

    month_diff = []
    for i in range(12):
        month_diff.append([])                                                                       #Inizializza una lista per ogni mese per memorizzare le differenze tra i mesi

    for i in range(len(time_series)):
        date = time_series[i][0]
        year, month = [int(line) for line in date.split('-')]

        if first_year <= year < last_year:
            next_year_same_month = None
            for j in range(i+1, len(time_series)):
                next_date = time_series[j][0]
                next_year, next_month = [int(line) for line in next_date.split('-')]
                if next_year == year + 1 and next_month == month:                                   #Controlla se il mese esiste anche per l'anno successivo
                    next_year_same_month = time_series[j]
                    break                                                                           #Esce dal ciclo for se viene trovato un mese corrispondente

            if next_year_same_month is not None:
                diff = (next_year_same_month[1] - time_series[i][1])
                month_diff[month - 1].append(diff)                                                  #Lista contenente la differenza tra i passeggeri

    result = []
    for i in month_diff:
        if i:
            avg = sum(i) / len(i)                                                                   #Calcola la media delle differenze per ogni mese
        else:
            avg = 0                                                                                 
        result.append(avg)                                                                          #Memorizza la media delle differenze per ogni mese

    return result

# time_series_file = CSVTimeSeriesFile(name='C:\\Users\\gigachad\\OneDrive\\Programmazione\\Esame_11-07-2023\\data.csv')
# time_series = time_series_file.get_data()
# result = compute_avg_monthly_difference(time_series, "1949", "1951")
# print(result)
