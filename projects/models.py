from django.db import models


class Skill(models.Model):
    name = models.CharField("Название навыка", max_length=124, unique=True)

    class Meta:
        verbose_name = "Навык"
        verbose_name_plural = "Навыки"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Project(models.Model):
    class ProjectStatuses(models.TextChoices):
        OPEN = "open", "Открыт"
        CLOSED = "closed", "Закрыт"

    name = models.CharField("Название", max_length=200)
    description = models.TextField("Описание", blank=True)
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="owned_projects",
        verbose_name="Автор",
    )
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    github_url = models.URLField("GitHub", blank=True)
    status = models.CharField(
        "Статус", max_length=6, choices=ProjectStatuses, default=ProjectStatuses.OPEN,
    )
    participants = models.ManyToManyField(
        "users.User",
        related_name="participated_projects",
        verbose_name="Участники",
        blank=True,
    )
    skills = models.ManyToManyField(
        Skill, related_name="projects", verbose_name="Необходимые навыки", blank=True,
    )

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"
        ordering = ["-created_at", "-id"]

    def __str__(self):
        return self.name
