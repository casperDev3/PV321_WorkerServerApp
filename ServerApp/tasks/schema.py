import graphene
from graphene import relay
from graphene_django.types import DjangoObjectType
from graphene.relay import Node
from .models import Task
from graphene_django.filter import DjangoFilterConnectionField
from django_filters import FilterSet, OrderingFilter


class TaskFilter(FilterSet):
    class Meta:
        model = Task
        fields = {
            'title': ['exact', 'icontains', 'istartswith', 'iendswith'],
            'description': ['exact', 'icontains', 'istartswith'],
            'completed': ['exact'],
            'due_date': ['exact', 'gt', 'lt'],
        }
        order_by = OrderingFilter(
            fields=(
                ('title', 'title'),
                ('due_date', 'due_date'),
            )
        )


class TaskType(DjangoObjectType):
    class Meta:
        model = Task
        interfaces = (relay.Node,)  # Використовуємо Relay Node
        fields = ('id', 'title', 'description', 'completed', 'due_date')


class CreateTask(relay.ClientIDMutation):
    class Input:
        title = graphene.String(required=True)
        description = graphene.String()
        completed = graphene.Boolean()
        due_date = graphene.Date()

    task = graphene.Field(TaskType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        # Дозволяємо Django автоматично призначити ID
        task = Task(
            title=input.get('title'),
            description=input.get('description'),
            completed=input.get('completed', False),
            due_date=input.get('due_date')
        )
        task.save()
        return CreateTask(task=task)


class UpdateTask(relay.ClientIDMutation):
    class Input:
        # Тут передається глобальний ID, а не простий числовий
        id = graphene.ID(required=True)
        title = graphene.String()
        description = graphene.String()
        completed = graphene.Boolean()
        due_date = graphene.Date()

    task = graphene.Field(TaskType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        task = Node.get_node_from_global_id(info, input.get('id'), only_type=TaskType)
        if not task:
            raise Exception("Task not found (можливо, ви передали не той формат ID)")

        # Оновлюємо лише ті поля, що присутні у вхідних даних
        if input.get('title') is not None:
            task.title = input['title']
        if input.get('description') is not None:
            task.description = input['description']
        if input.get('completed') is not None:
            task.completed = input['completed']
        if input.get('due_date') is not None:
            task.due_date = input['due_date']

        task.save()
        return UpdateTask(task=task)


class DeleteTask(relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)
        print("testID", id)

    success = graphene.Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        task = Node.get_node_from_global_id(info, input.get('id'), only_type=TaskType)
        if not task:
            raise Exception("Task not found (можливо, ви передали не той формат ID)")

        task.delete()
        return DeleteTask(success=True)


class Query(graphene.ObjectType):
    node = relay.Node.Field()  # Relay потребує поля node
    all_tasks = DjangoFilterConnectionField(TaskType, filterset_class=TaskFilter,
                                            order_by=graphene.List(of_type=graphene.String))

    def resolve_all_tasks(root, info, **kwargs):
        query = Task.objects.filter(**kwargs)
        return query


class Mutation(graphene.ObjectType):
    create_task = CreateTask.Field()
    update_task = UpdateTask.Field()
    delete_task = DeleteTask.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
