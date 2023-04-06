from django.db import models

class table1(models.Model):
    company_name = models.CharField(max_length=255)
    job_name = models.CharField(max_length=255)
    company_size = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    salary = models.CharField(max_length=255)
    attribute_text = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    job_welfare = models.CharField(max_length=255)

    class Meta:
        db_table = 'table1'  # 数据表名称