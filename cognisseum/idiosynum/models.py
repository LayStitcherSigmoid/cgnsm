from django.db import models
from administrarium.models import Pragmon
from politeum.models import Book, Person
from pharmakeium.models import Molecule
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Throughline(Pragmon):
    name = models.CharField(max_length=100)
    related_to = models.ManyToManyField('self', through='ThroughlineRelation', symmetrical=False, blank=True)


class ThroughlineRelation(Pragmon):
    source_throughline = models.ForeignKey(Throughline, on_delete=models.RESTRICT, related_name="source_throughline")
    target_throughline = models.ForeignKey(Throughline, on_delete=models.RESTRICT, related_name="target_throughline")
    description = models.TextField()


class PostCategory(Pragmon):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)


class Tag(Pragmon):
    name = models.CharField(max_length=100)
    related_tags = models.ManyToManyField('self', blank=True, symmetrical=False)


class Post(Pragmon):
    title = models.CharField(max_length=100)
    category = models.ForeignKey(PostCategory, on_delete=models.RESTRICT)
    tags = models.ManyToManyField(Tag, blank=True, symmetrical=False)
    throughlines = models.ManyToManyField(Throughline, blank=True)
    asymmetrically_related_posts = models.ManyToManyField(
        'self',
        through='DirectedPostRelation',
        symmetrical=False,
        related_name='points_to'
    )
    symmetrically_related_posts = models.ManyToManyField(
        'self',
        through='SymmetricPostRelation',
        symmetrical=False,
        related_name='joined_with'
    )
    body = models.TextField()


class DirectedPostRelation(Pragmon):
    source_post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='source_posts')
    target_post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='target_posts')
    description = models.CharField(max_length=255, blank=True, null=True)  # Optional field to describe the relation
    relation_type = models.CharField(max_length=50, blank=True, null=True)  # Could be used to classify the relationship

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['source_post', 'target_post'], name='unique_post_relation')
        ]


class SymmetricPostRelation(Pragmon):
    post_1 = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='symmetry_post_1')
    post_2 = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='symmetry_post_2')
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['post_1', 'post_2'], name='unique_symmetric_relation'),
            models.UniqueConstraint(fields=['post_2', 'post_1'], name='unique_reverse_symmetric_relation')
        ]


class PostRelationToPerson(Pragmon):
    relative_post = models.ForeignKey(Post, on_delete=models.RESTRICT)


class PostRelationToBook(Pragmon):
    relative_post = models.ForeignKey(Post, on_delete=models.RESTRICT)
    relative_artifact = models.ForeignKey(Book, on_delete=models.RESTRICT)


class PageSpecificNote(Pragmon):
    book_relation = models.ForeignKey(PostRelationToBook, on_delete=models.RESTRICT)
    page_number = models.IntegerField()


class PostRelationToMolecule(Pragmon):
    relative_post = models.ForeignKey(Post, on_delete=models.RESTRICT)
    relative_molecule = models.ForeignKey(Molecule, on_delete=models.RESTRICT)


class TaskStatus(models.TextChoices):
    NOT_STARTED = 'NOT_STARTED', _('Not Started')
    STARTED = 'STARTED', _('Started')
    SUSPENDED = 'SUSPENDED', _('Suspended')
    IN_PROGRESS = 'IN_PROGRESS', _('In Progress')
    BLOCKED = 'BLOCKED', _('Blocked')
    ABANDONED = 'ABANDONED', _('Abandoned')
    COMPLETED = 'COMPLETED', _('Completed')


class SoftHardEnum(models.TextChoices):
    HARD = 'HARD', _('Hard Co-Entity')
    SOFT = 'SOFT', _('Soft Co-Entity')


class Project(Pragmon):
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=12, choices=TaskStatus.choices, default=TaskStatus.NOT_STARTED)
    co_related_projects = models.ManyToManyField(
        'self',
        through='ProjectCoRelation',
        symmetrical=False,
        blank=True,
        related_name='co_related_projects_set'
    )
    parent_projects = models.ManyToManyField(
        'self',
        through='ProjectParentRelation',
        symmetrical=False,
        blank=True,
        related_name='child_projects_set'
    )


class ProjectCoRelation(Pragmon):
    source_project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='source_co_relations')
    target_project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='target_co_relations')
    relation_type = models.CharField(max_length=10, choices=SoftHardEnum.choices, default=SoftHardEnum.SOFT)

    class Meta:
        unique_together = ('source_project', 'target_project')
        constraints = [
            models.UniqueConstraint(fields=['source_project', 'target_project'], name='unique_project_co_relation')
        ]


class ProjectParentRelation(Pragmon):
    parent_project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='parent_relations')
    child_project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='child_relations')

    class Meta:
        unique_together = ('parent_project', 'child_project')
        constraints = [
            models.UniqueConstraint(fields=['parent_project', 'child_project'], name='unique_project_parent_relation')
        ]


class Goal(Pragmon):
    name = models.CharField(max_length=100)
    projects = models.ManyToManyField(Project, through='GoalProjectRelation', blank=True)
    status = models.CharField(max_length=12, choices=TaskStatus.choices, default=TaskStatus.NOT_STARTED)
    co_related_goals = models.ManyToManyField(
        'self',
        through='GoalCoRelation',
        symmetrical=False,
        blank=True,
        related_name='co_related_goals_set'
    )
    parent_goals = models.ManyToManyField(
        'self',
        through='GoalParentRelation',
        symmetrical=False,
        blank=True,
        related_name='child_goals_set'
    )


class GoalProjectRelation(Pragmon):
    relative_project = models.ForeignKey(Project, on_delete=models.CASCADE)
    relative_goal = models.ForeignKey(Goal, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('relative_project', 'relative_goal')


class GoalCoRelation(Pragmon):
    source_goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name='source_co_relations')
    target_goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name='target_co_relations')
    relation_type = models.CharField(max_length=10, choices=SoftHardEnum.choices, default=SoftHardEnum.SOFT)

    class Meta:
        unique_together = ('source_goal', 'target_goal')
        constraints = [
            models.UniqueConstraint(fields=['source_goal', 'target_goal'], name='unique_goal_co_relation')
        ]


class GoalParentRelation(Pragmon):
    parent_goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name='parent_relations')
    child_goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name='child_relations')

    class Meta:
        unique_together = ('parent_goal', 'child_goal')
        constraints = [
            models.UniqueConstraint(fields=['parent_goal', 'child_goal'], name='unique_goal_parent_relation')
        ]


class Task(Pragmon):
    name = models.CharField(max_length=100)
    description = models.TextField()
    is_complete = models.BooleanField(default=False)
    goals = models.ManyToManyField(Goal, through='TaskGoalRelation', blank=True)
    projects = models.ManyToManyField(Project, through='TaskProjectRelation', blank=True)
    status = models.CharField(max_length=12, choices=TaskStatus.choices, default=TaskStatus.NOT_STARTED)
    co_related_tasks = models.ManyToManyField(
        'self',
        through='TaskCoRelation',
        symmetrical=False,
        blank=True,
        related_name='co_related_tasks_set'
    )
    parent_tasks = models.ManyToManyField(
        'self',
        through='TaskParentRelation',
        symmetrical=False,
        blank=True,
        related_name='child_tasks_set'
    )


class TaskCoRelation(Pragmon):
    source_task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='source_co_relations')
    target_task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='target_co_relations')
    relation_type = models.CharField(max_length=10, choices=SoftHardEnum.choices, default=SoftHardEnum.SOFT)

    class Meta:
        unique_together = ('source_task', 'target_task')
        constraints = [
            models.UniqueConstraint(fields=['source_task', 'target_task'], name='unique_task_co_relation')
        ]


class TaskParentRelation(Pragmon):
    parent_task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='parent_relations')
    child_task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='child_relations')

    class Meta:
        unique_together = ('parent_task', 'child_task')
        constraints = [
            models.UniqueConstraint(fields=['parent_task', 'child_task'], name='unique_task_parent_relation')
        ]


class TaskGoalRelation(Pragmon):
    relative_task = models.ForeignKey(Task, on_delete=models.CASCADE)
    relative_goal = models.ForeignKey(Goal, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('relative_task', 'relative_goal')


class TaskProjectRelation(Pragmon):
    relative_task = models.ForeignKey(Task, on_delete=models.CASCADE)
    relative_project = models.ForeignKey(Project, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('relative_task', 'relative_project')


class ReadingTask(Pragmon):
    relative_task = models.ForeignKey(Task, on_delete=models.RESTRICT)
    relative_book = models.ForeignKey(Book, on_delete=models.RESTRICT)

    class Meta:
        unique_together = ('relative_task', 'relative_book')


class BookGoal(Pragmon):
    relative_goal = models.ForeignKey(Goal, on_delete=models.RESTRICT)
    relative_book = models.ForeignKey(Book, on_delete=models.RESTRICT)

    class Meta:
        unique_together = ('relative_goal', 'relative_book')


class PageSpecificNote(Pragmon):
    book_relation = models.ForeignKey(BookGoal, on_delete=models.RESTRICT)
    page_number = models.IntegerField()


class ReadingLog(Pragmon):
    relative_book = models.ForeignKey(Book, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    progress_percentage = models.PositiveIntegerField()
    current_page = models.PositiveIntegerField()
    
    def __str__(self):
        return f"{self.user.username} reading {self.book.title} starting on {self.start_date}"