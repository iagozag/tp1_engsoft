# Generated by Django 4.2.12 on 2024-10-06 02:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("polls", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="usuario",
            name="veiculo",
        ),
        migrations.AddField(
            model_name="veiculo",
            name="cpf_motorista",
            field=models.ForeignKey(
                default="0.00000000",
                on_delete=django.db.models.deletion.CASCADE,
                to="polls.usuario",
            ),
        ),
    ]