from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='gamesession',
            name='can_undo',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='gamesession',
            name='previous_board',
            field=models.JSONField(default=list),
        ),
        migrations.AddField(
            model_name='gamesession',
            name='previous_score',
            field=models.IntegerField(default=0),
        ),
    ]
