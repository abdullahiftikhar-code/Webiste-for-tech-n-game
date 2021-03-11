from django.shortcuts import render ,HttpResponse,redirect
from home.models import Contact
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from blog.models import Post
# Main endpoints
def index(request):
    return render(request, 'home/home.html')

def about(request):
    return render(request, 'home/about.html')
def contact(request):
    # Pushing the form to database
    if request.method=='POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        if len(name)<3 or len(email)<3 or len(phone)<7 or len(content)<3:
            messages.error(request, "Please fill the form correctly")

        else:
            contact = Contact(name=name,email=email,phone=phone,content=content)
            contact.save()
            messages.success(request,"Message is sent succesfully")

    return render(request, 'home/contact.html')
    
def search(request):
    query = request.GET['query']
    if len(query) > 78:
        allPosts = Post.objects.none()

    else:    
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsContent = Post.objects.filter(content__icontains=query)
        allPosts = allPostsTitle.union(allPostsContent)

    if allPosts.count()==0:
        messages.warning(request,"Please enter a correct Keyword")
    params = {'allPosts':allPosts, 'query':query}
    return render(request,"home/search.html",params)

# AUTH API
def handleSignup(request):
    if request.method=='POST':
        # get the post parameters
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # Check for errorneous inputs
        if not username.isalnum():
            messages.error(request,"Username Should only contain letters or numbers")
            return redirect('/')
        if pass1 != pass2:
            messages.error(request,"Password do not match")
            return redirect('/')

        if User.objects.filter(username=username).exists():
            messages.error(request,f"This Username {username} has been chosen by somebody else")
            return redirect('/')
        if User.objects.filter(email=email).exists():
            messages.error(request,f"Someone has made an account with this email {email}")
            return redirect('/')
        

        

        # Create the user
        myuser = User.objects.create_user(username,email,pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request,"Your iCoder account is Successfully created")
        return redirect('/')

    else:
        return HttpResponse("404 not Found")


def handleLogin(request):
    if request.method == "POST":
        # get the post parameters
        loginusername = request.POST['loginUsername']
        loginpass = request.POST['loginpass']

        user = authenticate(username=loginusername,password=loginpass)

        if user is not None:
            login(request,user)
            messages.success(request,"You have succesfully logged in")
            return redirect('/')

        else:
            messages.error(request,"Invalid credentials")
            return redirect('/')
    else:
        return HttpResponse("404 Error not Found")

    return HttpResponse("Login")
def handleLogout(request):
    logout(request)
    messages.success(request,"You have succesfully logged out")
    return redirect('/')
    return HttpResponse("Logout")

