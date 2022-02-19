import json
from peewee import Model, SqliteDatabase, AutoField, CharField, TimeField, BooleanField, TextField, DateField
from playhouse.shortcuts import model_to_dict

path_to_database = 'db.sqlite'
conn = SqliteDatabase(path_to_database)

class BaseModel(Model):
    class Meta:
        database = conn

class Schedule(BaseModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.create_table()

    schedule_id = AutoField(column_name='scheduleId', primary_key=True)
    name = CharField(column_name='name')
    teacher = CharField(column_name='teacher')
    isUpperWeek = BooleanField(column_name='isUpperWeek', default=False)
    date = DateField(column_name='date', formats='%H:%M, %A')
    link = TextField(column_name='link')
    time = TimeField(column_name='time', formats='%H:%M')
    day = DateField(column_name='day', formats='%A')

    def migrate(json_filepath: str):
        try:
            with open(json_filepath, 'r') as f:
                data = f.read()
                data = json.loads(data)
                for _ in data["_default"]:
                    rec = data['_default'][_]
                    # print(rec)
                    Schedule.create(
                        name=rec['name'],
                        teacher=rec['teacher'],
                        isUpperWeek=rec['isUpperWeek'],
                        date=f'{rec["time"]}, {rec["day"]}',
                        time=rec['time'],
                        day=rec['day'],
                        link=rec['links'][0]
                    )
        except Exception as ex:
            print(ex)

    def as_dict(self):
        return str(model_to_dict(self))

if __name__ == '__main__':
    # print([str(_) for _ in Schedule.select()])
    # print([_.day for _ in Schedule.select()])
    Schedule.migrate('db.json')