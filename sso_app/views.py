# views.py

from django.shortcuts import redirect, render
from django.conf import settings
import msal
from django.contrib.auth.models import Group
from urllib.parse import urlencode
from urllib.parse import quote
from urllib.parse import unquote
from urllib.parse import parse_qs

app = msal.ConfidentialClientApplication(
    settings.AZURE_AD_CLIENT_ID,
    authority=settings.AZURE_AD_AUTHORITY,
    client_credential=settings.AZURE_AD_CLIENT_SECRET)

def login_view(request):
    target_dashboard = request.GET.get("target")
    print(target_dashboard)
    return render(request, 'sso_login.html')

def login(request):
    target_dashboard1 = request.GET.get("target")
    print("Target:",target_dashboard1)

    # Encode the custom parameter within the state
    state_parameter = quote(f'target_dashboard={target_dashboard1}')
    auth_url = app.get_authorization_request_url(settings.AZURE_AD_SCOPE, redirect_uri=settings.REDIRECT_URI,state=state_parameter,
    additional_params={"target_dashboard": target_dashboard1})
    # auth_url += f'&target={target_dashboard1}'
    print(auth_url)
    # print(Group.objects.filter(name='POD Dashboard').exists())
    # print(request.user.groups.filter(name='POD Dashboard').exists())
    return redirect(auth_url)


def callback(request): 
    auth_code = request.GET.get('code')
    print("auth_code:-",auth_code)

    print("\n")
    print(request)
    print("\n")
    print(request.user)

    state_parameter = request.GET.get("state")
    # Decode and parse the state parameter to access your custom parameter
    target_dashboard = unquote(state_parameter).split('=')[1]

    print("Custom:",target_dashboard)

    if 'code' in request.GET:
        result = app.acquire_token_by_authorization_code(
            request.GET['code'], settings.AZURE_AD_SCOPE, redirect_uri=settings.REDIRECT_URI)
        
        # print("Result:",result)
        # token = result['access_token']

        context = {
        'target_dashboard': target_dashboard,
        'redirection_url': get_redirection_url(target_dashboard),  
    }

        if target_dashboard is not None:

            # Get the group object by name
            group = Group.objects.get(name=target_dashboard)

            # Get all users from the group
            users_in_group = group.user_set.all()

            for user in users_in_group:
                print(f"Username: {user.username}, Email: {user.email}")

            # Find out email_id using id_token_claims
            claims = result.get("id_token_claims")
            user_email = claims.get("preferred_username")
            print(user_email)

            user_matches=False
            for user in users_in_group:
                if user.email==user_email:
                    user_matches=True
                    print("User Matches")
            if user_matches:
                encoded_email = urlencode({'email': user_email})    
                return redirect (f"/authenticate/?target={target_dashboard}&email={encoded_email}")
            else:
                return render(request, 'callback.html',context=context)
        else:
            return render(request, 'callback.html',context=context)

   
    else:
        return render(request, 'callback.html',context=context)
    
    #     else:

    # if  request.user.groups.filter(name='POD Dashboard').exists():
    #     print("You exist in the POD Dashboard Group")
    #     if request.user.has_perm('sso_app.can_access_auth_url'):           
    #         return redirect("https://poddashboard.maricoapps.biz/login/streamlit/")

    #         # Use 'token' to make authenticated requests to Azure AD or Microsoft Graph API
    #         # Store user information in session or perform other actions as needed
            
    #         token = result['access_token']

    #         # Get the user's email from the token or any other source
    #         user_email = get_user_email_from_token(token)

    #         # Get or create a user profile
    #         user, created = User.objects.get_or_create(email=user_email)
    #         user_profile, _ = UserProfile.objects.get_or_create(user=user, email=user_email)
    
def authenticate(request):
    target_dashboard = request.GET.get("target")
    print(target_dashboard)

    # Passing user email 
    email_param = request.GET.get("email")
    decoded_email = parse_qs(email_param)['email'][0]
    print(decoded_email)
    
    if target_dashboard == "MIL_Dashboard":
        return redirect("https://ai.maricoapps.biz/dashboard/mil_sc/")
    elif target_dashboard == "POD_Dashboard":    
        return redirect("https://ai.maricoapps.biz/app/pod/?email={email_param}")
    elif target_dashboard == "MBL_Dashboard":
        return redirect("https://ai.maricoapps.biz/dashboard/mbl_sc/")
    elif target_dashboard == "CODE_Tracer":
        return redirect("https://ai.maricoapps.biz/app/codetracer/")
    elif target_dashboard == "JIRA_Tracker":
        return redirect("https://ai.maricoapps.biz/dashboard/jira_tracker/")
    elif target_dashboard == "EDAapp":
        return redirect("https://ai.maricoapps.biz/app/EDAapp/")
    else:
        return render(request, 'callback.html')
    

def get_redirection_url(target_dashboard):
    if target_dashboard == "MIL_Dashboard":
        return "https://ai.maricoapps.biz/dashboard/mil_sc/"
    elif target_dashboard == "POD_Dashboard":
        return "https://ai.maricoapps.biz/app/pod/"
    elif target_dashboard == "MBL_Dashboard":
        return "https://ai.maricoapps.biz/dashboard/mbl_sc/"
    elif target_dashboard == "CODE_Tracer":
        return "https://ai.maricoapps.biz/app/codetracer/"
    elif target_dashboard == "JIRA_Tracker":
        return "https://ai.maricoapps.biz/dashboard/jira_tracker/"
    elif target_dashboard == "EDAapp":
        return "https://ai.maricoapps.biz/app/EDAapp/"
    
    
