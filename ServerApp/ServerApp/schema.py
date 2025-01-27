import graphene
from django.db.models.sql import Query
from graphene_django.types import DjangoObjectType
# from graphene_django.filter import DjangoFilterConnectionField
from graphene import relay
from ServerApp.tasks.models import Task

class TaskType(DjangoObjectType):
    class Meta:
        model = Task
        interfaces = (graphene.relay.Node, )
        # filter_fields = {
        #     'title': ['exact', 'icontains', 'istartswith'],
        #     'description': ['exact', 'icontains'],
        #     'status': ['exact'],
        #     'created_at': ['exact', 'icontains'],
        #     'updated_at': ['exact', 'icontains']
        # }

class CreateTask(relay.ClientIDMutation):
   task = graphene.Field(TaskType)
   class Arguments:
       title = graphene.String()
       description = graphene.String()
       completed = graphene.Boolean()
       due_date = graphene.Date()
   def mutate(self, info, title, due_date, description = None, completed = False):
       task = Task(title=title, description=description, completed=completed, due_date=due_date)
       task.save()
       return CreateTask()


class Mutation(graphene.ObjectType):
    create_task = CreateTask.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)