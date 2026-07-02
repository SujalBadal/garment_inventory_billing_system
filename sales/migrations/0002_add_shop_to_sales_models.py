from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_add_shop_to_inventory_models'),
        ('sales', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='shop',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.shop'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_number',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterUniqueTogether(
            name='invoice',
            unique_together={('shop', 'invoice_number')},
        ),
    ]
