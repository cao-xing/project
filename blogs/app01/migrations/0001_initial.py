# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-16 09:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='文章标题')),
                ('desc', models.CharField(max_length=255, verbose_name='文章描述')),
                ('read_count', models.IntegerField(default=0)),
                ('comment_count', models.IntegerField(default=0)),
                ('up_count', models.IntegerField(default=0)),
                ('down_count', models.IntegerField(default=0)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('article_type_id', models.IntegerField(choices=[(1, '编程语言'), (2, '软件设计'), (3, '前端'), (4, '操作系统'), (5, '数据库')], default=None)),
            ],
            options={
                'verbose_name_plural': '文章表',
            },
        ),
        migrations.CreateModel(
            name='Article2Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.Article', verbose_name='文章')),
            ],
        ),
        migrations.CreateModel(
            name='ArticleDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='文章内容')),
                ('article', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app01.Article', verbose_name='所属文章')),
            ],
            options={
                'verbose_name_plural': '文章详细表',
            },
        ),
        migrations.CreateModel(
            name='ArticleUp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app01.Article', verbose_name='所属文章')),
            ],
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, verbose_name='个人博客标题')),
                ('site', models.CharField(max_length=32, verbose_name='个人博客后缀')),
                ('theme', models.CharField(max_length=32, verbose_name='博客主题')),
            ],
            options={
                'verbose_name_plural': '站点表',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='分类标题')),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.Blog', verbose_name='所属博客')),
            ],
            options={
                'verbose_name_plural': '分类表',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=255, verbose_name='评论内容')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='评论时间')),
                ('up_count', models.IntegerField(default=0)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.Article', verbose_name='评论文章')),
                ('pid', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app01.Comment', verbose_name='父级评论')),
            ],
            options={
                'verbose_name_plural': '评论表',
            },
        ),
        migrations.CreateModel(
            name='CommentUp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app01.Comment', verbose_name='所属评论')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='标签名称')),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.Blog', verbose_name='所属博客')),
            ],
            options={
                'verbose_name_plural': '标签表',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32, verbose_name='用户名')),
                ('password', models.CharField(max_length=32, verbose_name='密码')),
                ('nickname', models.CharField(max_length=32, verbose_name='别名')),
                ('telephone', models.CharField(blank=True, max_length=11, null=True, unique=True, verbose_name='手机号码')),
                ('avatar', models.FileField(default='/avatar/default.png', upload_to='avatar', verbose_name='头像')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name_plural': '用户表',
            },
        ),
        migrations.CreateModel(
            name='UserFans',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('follower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follows', to='app01.User', verbose_name='粉丝')),
                ('myself', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='focus', to='app01.User', verbose_name='博主')),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='fans',
            field=models.ManyToManyField(blank=True, null=True, related_name='f', through='app01.UserFans', to='app01.User', verbose_name='粉丝们'),
        ),
        migrations.AddField(
            model_name='commentup',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app01.User', verbose_name='所属用户'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.User', verbose_name='评论者'),
        ),
        migrations.AddField(
            model_name='blog',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app01.User', verbose_name='对应用户'),
        ),
        migrations.AddField(
            model_name='articleup',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app01.User', verbose_name='所属用户'),
        ),
        migrations.AddField(
            model_name='article2tag',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.Tag', verbose_name='标签'),
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app01.Category', verbose_name='文章类型'),
        ),
        migrations.AddField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(through='app01.Article2Tag', to='app01.Tag'),
        ),
        migrations.AddField(
            model_name='article',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app01.User', verbose_name='所属用户'),
        ),
        migrations.AlterUniqueTogether(
            name='userfans',
            unique_together=set([('myself', 'follower')]),
        ),
        migrations.AlterUniqueTogether(
            name='article2tag',
            unique_together=set([('article', 'tag')]),
        ),
    ]