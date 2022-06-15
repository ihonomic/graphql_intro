from django.urls import path
from graphene_django.views import GraphQLView
from books.schema import schema  # Assuming it's not global in settings.py

urlpatterns = [
    #   Only one endpoint to access GraphQL
    path('graphql', GraphQLView.as_view(graphiql=True, schema=schema)),
]
