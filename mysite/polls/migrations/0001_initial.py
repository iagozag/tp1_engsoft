# Generated by Django 4.2.12 on 2024-10-06 02:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Veiculo",
            fields=[
                (
                    "placa",
                    models.CharField(max_length=7, primary_key=True, serialize=False),
                ),
                ("modelo", models.CharField(max_length=50)),
                ("cor", models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name="Usuario",
            fields=[
                ("nome", models.CharField(default="", max_length=100)),
                (
                    "cpf",
                    models.CharField(max_length=11, primary_key=True, serialize=False),
                ),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("data_nascimento", models.DateField()),
                ("telefone", models.CharField(blank=True, max_length=15, null=True)),
                ("avaliacao_media", models.FloatField(default=0)),
                ("senha", models.CharField(max_length=128)),
                (
                    "veiculo",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="polls.veiculo"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Carona",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quantidade", models.IntegerField()),
                ("ponto_encontro", models.CharField(max_length=255)),
                ("destino", models.CharField(max_length=255)),
                ("data_hora", models.DateTimeField()),
                (
                    "cpf_motorista",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="polls.usuario"
                    ),
                ),
                (
                    "veiculo",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="polls.veiculo"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Historico",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("avaliacao_motorista", models.IntegerField(blank=True, null=True)),
                ("avaliacao_usuario", models.IntegerField(blank=True, null=True)),
                (
                    "cpf_motorista",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="historico_motorista",
                        to="polls.usuario",
                    ),
                ),
                (
                    "cpf_usuario",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="historico_usuario",
                        to="polls.usuario",
                    ),
                ),
                (
                    "numero_carona",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="polls.carona"
                    ),
                ),
            ],
            options={
                "unique_together": {("numero_carona", "cpf_usuario")},
            },
        ),
    ]
