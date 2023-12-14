# Generated by Django 4.2.6 on 2023-12-14 07:56

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('date_of_birth', models.DateField(null=True)),
                ('last_update', models.DateTimeField(auto_now=True)),
                ('add_date', models.DateTimeField(auto_now_add=True)),
                ('user_type', models.CharField(max_length=100)),
                ('accept_policy', models.BooleanField(default=False)),
                ('photo', models.ImageField(blank=True, default='user_photos/default_user_photo.jpg', upload_to='user_photos')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('text', models.TextField()),
                ('update_date', models.DateField(auto_now=True)),
                ('add_date', models.DateTimeField(auto_now_add=True)),
                ('assignment_type', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=100)),
                ('tags', models.CharField(max_length=255)),
                ('language', models.CharField(max_length=100)),
                ('share', models.IntegerField(default=0)),
                ('likes', models.IntegerField(default=0)),
                ('image_url', models.CharField(max_length=255)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assignments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AssignmentClient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('text', models.TextField()),
                ('update_date', models.DateField(auto_now=True)),
                ('add_date', models.DateTimeField(auto_now_add=True)),
                ('assignment_type', models.CharField(max_length=100)),
                ('status', models.CharField(default='to do', max_length=100)),
                ('tags', models.CharField(max_length=255)),
                ('language', models.CharField(max_length=100)),
                ('share', models.IntegerField(default=0)),
                ('likes', models.IntegerField(default=0)),
                ('image_url', models.CharField(max_length=255)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assignments_clients', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BlockChoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reply', models.CharField(max_length=100)),
                ('checked', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('add_date', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='notes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Massage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('massage', models.TextField()),
                ('post_date', models.DateTimeField(auto_now_add=True)),
                ('is_read', models.BooleanField(default=False)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sent_massages', to=settings.AUTH_USER_MODEL)),
                ('recipient', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='received_massages', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assignments', models.ManyToManyField(blank=True, to='api.assignment')),
                ('clients', models.ManyToManyField(blank=True, related_name='clients', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('add_date', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('diagnosis', models.CharField(blank=True, max_length=255)),
                ('about', models.TextField(blank=True)),
                ('assignments', models.ManyToManyField(blank=True, to='api.assignmentclient')),
                ('notes', models.ManyToManyField(blank=True, to='api.note')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Block',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=250)),
                ('reply', models.TextField(blank=True)),
                ('type', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('start_range', models.IntegerField(default=1)),
                ('end_range', models.IntegerField(default=10)),
                ('left_pole', models.CharField(max_length=50)),
                ('right_pole', models.CharField(max_length=50)),
                ('choice_replies', models.ManyToManyField(blank=True, to='api.blockchoice')),
            ],
        ),
        migrations.AddField(
            model_name='assignmentclient',
            name='blocks',
            field=models.ManyToManyField(blank=True, related_name='assignment_client', to='api.block'),
        ),
        migrations.AddField(
            model_name='assignmentclient',
            name='comments',
            field=models.ManyToManyField(blank=True, to='api.comment'),
        ),
        migrations.AddField(
            model_name='assignmentclient',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='assignment',
            name='blocks',
            field=models.ManyToManyField(blank=True, related_name='assignment', to='api.block'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='comments',
            field=models.ManyToManyField(blank=True, to='api.comment'),
        ),
    ]
