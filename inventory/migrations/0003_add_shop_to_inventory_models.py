from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_category_subcategory_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='shop',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.shop'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterUniqueTogether(
            name='category',
            unique_together={('shop', 'name')},
        ),
        migrations.AddField(
            model_name='subcategory',
            name='shop',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.shop'),
        ),
        migrations.AlterUniqueTogether(
            name='subcategory',
            unique_together={('shop', 'category', 'name')},
        ),
        migrations.AddField(
            model_name='product',
            name='shop',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.shop'),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_id',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterUniqueTogether(
            name='product',
            unique_together={('shop', 'product_id')},
        ),
    ]
