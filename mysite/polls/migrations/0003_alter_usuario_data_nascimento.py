# Generated by Django 4.2.12 on 2024-10-06 02:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("polls", "0002_remove_usuario_veiculo_veiculo_cpf_motorista"),
    ]

    operations = [
        migrations.AlterField(
            model_name="usuario",
            name="data_nascimento",
            field=models.CharField(max_length=100),
        ),
    ]
