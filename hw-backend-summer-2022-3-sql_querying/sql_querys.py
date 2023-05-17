# INFO
# Вывести топ 5 самых коротких по длительности перелетов.  Duration - разница между scheduled_arrival и scheduled_departure.
# В ответе должно быть 2 колонки [flight_no, duration]
TASK_1_QUERY = """
select flight_no, age(scheduled_arrival, scheduled_departure) as duration
from flights
order by duration
limit 5
"""
#  flight_no | duration
# -----------+----------
#  PG0235    | 00:25:00
#  PG0234    | 00:25:00
#  PG0233    | 00:25:00
#  PG0235    | 00:25:00
#  PG0234    | 00:25:00


# INFO
# Вывести топ 3 рейса по числу упоминаний в таблице flights
# количество упоминаний которых меньше 50
# В ответе должно быть 2 колонки [flight_no, count]
TASK_2_QUERY = """
select flight_no, count(flight_no) as count
from flights
group by flight_no
having count(flight_no) < 50
order by count desc
limit 3
"""
#  flight_no | count
# -----------+-------
#  PG0260    |    27
#  PG0371    |    27
#  PG0310    |    27

# INFO
# Вывести число перелетов внутри одной таймзоны
# Нужно вывести 1 значение в колонке count
TASK_3_QUERY = """
select count(1)
from flights as f
join airports_data as ad1 on f.arrival_airport = ad1.airport_code
join airports_data as ad2 on f.departure_airport = ad2.airport_code
where ad1.timezone = ad2.timezone
"""
#  count
# --------
#  16824
