from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.views import View
from django.shortcuts import render, redirect
from core.forms import MoodForm
from core.models import Mood
from string import punctuation
from datetime import datetime


@login_required
def home(request):
    return render(request, 'home.html')

# user authentication process
class Signup(View):

    def get(self, request):
        form = UserCreationForm(request.GET)
        return render(request, 'signup.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
        else:
            form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})


# input from user
class Index(View):

    def get(self, request):
        form = MoodForm(request.GET)
        return render(request, 'index.html', {'form': form})

    def post(self,request):
        form = MoodForm(request.POST)
        print('Printing the form data...\n', form.data)

        if form.is_valid():
            print("Form is valid")
            try:
                obj = form.save(commit=False)

                mood_dict = form.data
                print('Printing the value of mood_dict = form.data...\n', mood_dict)

                expression = mood_dict['message']
                print('Printing the message...\n', expression)

                positive_keywords = ["great", "happy", "amazing", "fantastic", "like", "love",
                                     "good", "awesome", "cool", "best", "exciting"]
                negative_keywords = ["disgusting", "boring", "sad", "depressing", "hate", "shit",
                                     "bad", "terrible", "horrible", "annoying", "worst"]

                expression = ''.join(c for c in expression if c not in punctuation)
                words = expression.strip().lower().split()
                print('Printing the words in the text as a list...\n', words)

                positive_mood_counter = 0
                negative_mood_counter = 0
                mood = 'Good'

                for word in words:
                    if word in positive_keywords:
                        positive_mood_counter += 1
                    elif word in negative_keywords:
                        negative_mood_counter += 1
                    else:
                        continue

                if positive_mood_counter >= negative_mood_counter:
                    mood = 'Good'
                    print('The mood is "{}"'.format(mood))
                elif negative_mood_counter > positive_mood_counter:
                    mood = 'Bad'
                    print('The mood is "{}"'.format(mood))

                # time = datetime.now()

                obj.user = request.user
                obj.result = mood
                # obj.time = time
                obj.save()
                print("The mood was saved in the database")

                return redirect('/show')
            except:
                    print("The mood did not save in the database")
                    pass
        else:
            form = MoodForm()
        return render(request, 'index.html', {'form': form})


# show all the data on html
class Show(View):

    def get(self, request):

        print('The current user is "{}"'.format(request.user))
        moods = Mood.objects.filter(user=request.user)
        print(moods)
        print('Printing the moods of the user')
        for mood in moods:
            print(mood.user, mood.message, mood.result, mood.time)

        return render(request, "show.html", {'moods': moods})


# To delete particular record
class Delete(View):

    def get(self,request, id):
        mood = Mood.objects.get(id=id)
        print('The mood for the message "{}" has been deleted.'.format(mood.message))
        mood.delete()
        return redirect("/show")
