from django.views.generic import ListView, UpdateView, CreateView, DeleteView, DetailView
from .models import Post, Author
from .filters import PostFilter
from .forms import PostForm, UserForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth.models import User

class PostsList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-dateCreation'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'posts.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'posts'
    paginate_by = 4  # поставим постраничный вывод в один элемент

    # def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
    #     context = super().get_context_data(**kwargs)
    #     context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр в контекст
    #     return context

    def post(self, request, *args, **kwargs):
        # берём значения для нового товара из POST-запроса отправленного на сервер
        author = request.POST['author']
        categoryType = request.POST['categoryType']
        #dateCreation = request.POST['dateCreation']
        title = request.POST['title']
        text = request.POST['text']



        post = Post(author=author, categoryType=categoryType, title=title, text=text)
        post.save()
        return super().get(request, *args, **kwargs)  # отправляем пользователя обратно на GET-запрос.

class PostDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post
    # Используем другой шаблон — product.html
    template_name = 'post.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'post'

class PostFil(PostsList):
    template_name = 'postfilter.html'
    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        return context

# дженерик для создания объекта. Надо указать только имя шаблона и класс формы, который мы написали в прошлом юните. Остальное он сделает за вас
class PostCreateView(CreateView):
    template_name = 'newapp/post_create.html'
    form_class = PostForm
    success_url = '/news/add/'


# дженерик для редактирования объекта
class PostUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'newapp/post_create.html'
    form_class = PostForm
    success_url = '/news/'


    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте, который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)



class PostDeleteView(DeleteView):
    template_name = 'newapp/post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'newapp/protected_profile.html'
    queryset = Author.objects.all()


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'newapp/protected_profile.html'
    form_class = UserForm
    success_url = '/news/profile/'

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте, который мы собираемся редактировать
    def get_object(self, **kwargs):
        return self.request.user

    # def get_object(self, **kwargs):
    #     context = super().get_context_data(**kwargs)  # получаем весь контекст из класса-родителя
    #     # добавили новую контекстную переменную is_not_premium, чтобы ответить на вопрос, есть ли пользователь в группе,
    #     # мы заходим в переменную запроса self.request, из этой переменной мы можем вытащить текущего пользователя,
    #     # в поле groups хранятся все группы, в которых он состоит, далее применяем фильтр к этим группам и ищем ту самую
    #     # имя которой premium, после чего проверяем, есть ли какие-то значения в отфильтрованном списке, метод exists()
    #     # вернет True, если группа premium в списке групп пользователя найдена, иначе — False,# в нашем случае
    #     # нужно получить наоборот — True, если пользователь не находится в этой группе, поэтому добавляем
    #     # отрицание not, и возвращаем контекст
    #     # Важно filter(name = 'authors') чтоб группы совпадали 'authors' тут = премиум в джанге
    #     context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
    #     return context

