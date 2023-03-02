from django.db import models


class Department(models.Model):
    """Department table"""
    title = models.CharField(verbose_name="标题", max_length=32)
    def __str__(self):
        return self.title

class UserInfo(models.Model):
    """User table"""
    name = models.CharField(verbose_name="员工名字", max_length=16)
    password = models.CharField(verbose_name="密码", max_length=32)
    app = models.IntegerField(verbose_name="年龄")
    account = models.DecimalField(verbose_name="账户余额", max_digits=12, decimal_places=2, default=0)
    create_time = models.DateField(verbose_name="入职时间")
    # 生成数据 会自动加上"_id"
    # to = 关联的数据表
    # to_field = 关联的数据属性
    # 如果部门表被删除， 数据也被删除 - CASCADE
    # depart = models.ForeignKey(to="Department",to_field="id",on_delete=models.CASCADE)
    # 如果部门表被删除， 数据置空
    depart = models.ForeignKey(to="Department", to_field="id", on_delete=models.SET_NULL, null=True, blank=True)

    # 在Django里面做的约束
    gender_choice = (
        (1, "男"),
        (2, "女")
    )
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choice)
