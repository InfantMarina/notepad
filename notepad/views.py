from django.shortcuts import render, reverse, redirect
from django.http import HttpResponse, HttpResponseRedirect
from notepad.models import Sign, Storage
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from rest_framework.views import APIView
from notepad import storageserilaizer
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from django.utils.decorators import method_decorator
from rest_framework.decorators import action

def login_view(request):
    print('hello')
    if request.method == 'GET':
        print(request.user.is_authenticated)
        if not request.user.is_authenticated:
            return render(request, 'notepad/login.html')
        return redirect('notepad:index')
    else:
        print('post')
        user_exist = User.objects.filter(username = request.POST['username'])
        if user_exist:
            print('user_exist')
            user = authenticate(request, username = request.POST['username'], password = request.POST['password'])
            if user:
                print('user')
                login(request, user=user)
                return redirect('notepad:index')
            else:
                print('else')
                data = {'message':'Incorrect Username or Password'}
                return render(request, 'notepad/login.html',{'data':data})  
        # else:
            # return render(request, 'notepad/data_store/index.html') 

def logout_view(request):
    logout(request)
    return redirect('notepad:login')

class Index(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, action=None, user_id=None):
        data = {}
        create = Storage.objects.all()
        create_serializer = storageserilaizer.Storage_Serializers(create, many=True)
        data['store_obj'] = create_serializer.data
        if action and action.lower() == 'create':
            return render(request, 'notepad/data_store/notes.html')  
        elif action and action.lower() == 'edit':
            edit = Storage.objects.get(id=user_id)
            edit_serializer = storageserilaizer.Storage_Serializers(edit)
            data['store_obj'] = edit_serializer.data
            return render(request, 'notepad/data_store/notes.html',{'data':data})
        elif action and action.lower() == 'delete':
            try:
                user_data = Storage.objects.get(id=int(user_id))
                # data['message'] = f'{user_data.title} notes deleted!'
                user_data.delete()
                # data['status'] = 'success'
            except Exception as e:
                data['status'] = 'failure'
                data['message'] = f'data not deleted {str(e)}'
            return redirect('notepad:index')
        if request.accepted_renderer.format == 'html':
            return render(request, 'notepad/data_store/index.html',{'data':data})
        return Response(data)

    def post(self, request, action=None, user_id=None):
        try:
            data = {}
            if action and action.lower() == 'edit':
                print(action, user_id)
                store_obj = Storage.objects.get(id=user_id)
                print(store_obj)
                edit_serializer = storageserilaizer.Storage_Serializers(store_obj)
                data['store_obj'] = edit_serializer.data
            elif action and action.lower() == 'create':
                store_obj = Storage()
            store_obj.title = request.data['title']
            print(store_obj.title)
            store_obj.body = request.data['body']
            store_obj.save()
            data['status'] = 'success'
            data['message'] = 'Notes are stored or updated'            
        except Exception as e:
            data['status'] = 'failure'
            data['message'] = f'Error occured. {str(e)}'
        if request.accepted_renderer.format == 'html':
            return redirect('notepad:index')
        return Response(data)
        # return render(request, 'notepad/data_store/notes.html', {'data':data})


# class StorageMViewset(viewsets.ModelViewSet):

#     queryset = Storage.objects.all()
#     serializer_class = storageserilaizer.Storage_Serializers

#     @action(detail=True)
#     def custom_action(self, request, *args, **kwargs):
#         pk = kwargs['pk']
#         print(request.method)
#         print(pk)
#         return HttpResponse("Custom Action Called")
