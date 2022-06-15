import graphene
# format django object to grapql object
from graphene_django import DjangoListField, DjangoObjectType
from .models import Books, Category, Answer, Question, Quizzes

# SOLVED: https://exerror.com/importerror-cannot-import-name-force_text-from-django-utils-encoding/


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id", "name")


class QuizzesType(DjangoObjectType):
    class Meta:
        model = Quizzes
        fields = ("id", "title", "category", "quiz")


class QuestionType(DjangoObjectType):
    class Meta:
        model = Question
        fields = ("title", "quiz")


class AnswerType(DjangoObjectType):
    class Meta:
        model = Answer
        fields = ("question", "answer_text")


class BooksType(DjangoObjectType):
    class Meta:
        model = Books
        fields = ("id", "title", "excerpt")


class Query(graphene.ObjectType):
    all_books = graphene.List(BooksType)
    user_name = graphene.String()

    # No need to resolve this manually - Except you want to extend the return
    all_quizzes = DjangoListField(QuizzesType)  # OR
    quiz = graphene.Field(QuizzesType, id=graphene.Int())

    all_questions = graphene.List(QuestionType, id=graphene.Int())
    all_answers = graphene.List(AnswerType, id=graphene.Int())

    def resolve_all_books(root, info):
        return Books.objects.all()

    def resolve_user_name(root, info):
        return f"I am logged In currently"

    def resolve_all_quizzes(root, info):
        return Quizzes.objects.all()

    def resolve_quiz(root, info, id):
        return Quizzes.objects.get(id=id)

    def resolve_all_questions(root, info, id):
        return Question.objects.filter(id=id)

    def resolve_all_answers(root, info, id):
        return Answer.objects.filter(question=id)


class CategoryMutation(graphene.Mutation):  # Adding data to database
    class Arguments:
        name = graphene.String(required=True)

    category = graphene.Field(CategoryType)  # return after mutating

    @classmethod
    def mutate(cls, root, info, name):
        category = Category(name=name)
        category.save()
        return CategoryMutation(category=category)


class CategoryUpdateMutation(graphene.Mutation):  # Updating data to database
    class Arguments:
        id = graphene.ID()
        name = graphene.String(required=True)

    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, id, name):
        category = Category.objects.get(id=id)
        category.name = name
        category.save()
        return CategoryMutation(category=category)


class Mutation(graphene.ObjectType):
    add_category = CategoryMutation.Field()
    update_category = CategoryUpdateMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)


# {
#   allBooks{
#     id
#     title
#   }
# }
# ====================

# query{
#   userName
# }
# =====================
# query{
#   allQuizzes{
#     title
#     category {
#       id
#       name
#     }
#   }
#   allQuestions{
#     title
#   }
# }
# ==========================
# query getQuestionAndAnswers($id: Int=1) #Global variable
# {
#    allQuestions(id:$id){
#     title
#   }
#   allAnswers(id:$id){
# 	answerText
#   }
# }
# ========================
# mutation categoryMutation
# {
#   addCategory(name:"Programming"){
#     category{
#       name
#     }
#   }
# }
# ==================================
# mutation categoryUpdateMutation
# {
#   updateCategory(id:1, name:"Cooking"){
#     category{
#       name
#     }
#   }
# }
