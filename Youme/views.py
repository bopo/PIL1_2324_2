import logging

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
# from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect, render
from django.utils import timezone

from .filters import *
from .recommandations import obtenir_recommandations


########################################################## ACCUEIL #################################################################
def accueil(request):
    return render(request, 'registration/accueil.html')


######################################################## AUTHENTIFICATION ##########################################################
def inscription(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.nom = form.cleaned_data['nom']
            user.email = form.cleaned_data['email']
            user.password = form.cleaned_data['password']
            user = form.save()
            login(request, user)
            if Utilisateur.objects.filter(email=user.email).exists():
                messages.error(request, 'Cet email est déjà utilisé')
            else:
                messages.success(request, 'Votre compte a été créé avec succès!')
            return redirect('profile_intro')
    else:
        form = InscriptionForm()
    return render(request, 'registration/inscription.html', {'form': form})


logger = logging.getLogger(__name__)


def connexion(request):
    if request.method == 'POST':
        form = ConnexionForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                user.last_login = timezone.now()
                user.save()
                return redirect('suggestion_profiles')
            else:
                logger.error(f"Échec de l'authentification pour l'email: {email}")
                messages.error(request, "Votre compte n'existe pas ou les informations sont incorrectes")
        else:
            logger.error("Formulaire invalide.")
            messages.error(request, "Formulaire invalide. Veuillez vérifier les informations saisies.")
    else:
        form = ConnexionForm()
    return render(request, 'registration/connexion.html', {'form': form})


def deconnexion(request):
    logout(request)
    messages.success(request, 'Vous avez été déconnecté')
    return redirect('accueil')


########################################### FORMULAIRES PROFILS & PREFERENCES ###############################################
def user_profile_intro(request):
    if request.method == 'POST':
        return redirect('personality_test')
    return render(request, 'formulaire/profile_intro.html')


def personality_test(request):
    if request.method == 'POST':
        form = PersonalityTestForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.utilisateur = request.user
            profile.save()
            return redirect('preferences_intro')
    else:
        form = PersonalityTestForm()
    return render(request, 'formulaire/personality_test.html', {'form': form})


def preferences_intro(request):
    if request.method == 'POST':
        return redirect('preferences_form')
    return render(request, 'formulaire/preferences_intro.html')


def preferences_form(request):
    if request.method == 'POST':
        form = PreferencesForm(request.POST, request.FILES)
        if form.is_valid():
            preferences = form.save(commit=False)
            preferences.user = request.user
            preferences.save()
            return redirect('connexion')
    else:
        form = PreferencesForm()
    return render(request, 'formulaire/preferences_form.html', {'form': form})


#####################################################################################################

@login_required
def profile(request):
    profile = Profile.objects.get(utilisateur=request.user)
    preferences = Préférences.objects.get(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    context = {
        'form': form,
        'user_profile': profile,
        'preferences': preferences,
    }

    return render(request, 'profile/profile.html', context)


def profile_detail(request, pk):
    info_profil = Profile.objects.get(pk=pk)
    info_preferences = Préférences.objects.get(pk=pk)
    context = {
        "profil": info_profil,
        "preferences": info_preferences,
    }
    return render(request, "profile/profile_detail.html", context)


####################################################### SUGGESTIONS & RECHERCHES DE PROFILS #########################################

@login_required
def suggestion_profiles(request):
    # Récupérer l'utilisateur connecté
    if not request.user.is_active:
        return redirect('connexion')

    current_user = request.user
    user_nom = current_user.nom
    user_id = current_user.id
    print(user_id)

    # Appeler la fonction pour obtenir les recommandations
    matchs = obtenir_recommandations(user_nom)

    # Initialiser une liste pour stocker les informations des profils recommandés
    recommended_profiles = []

    for match in matchs:
        utilisateurs = Utilisateur.objects.filter(nom=match)
        for utilisateur in utilisateurs:
            try:
                profil = Profile.objects.get(utilisateur=utilisateur)
                recommended_profiles.append({
                    'id': utilisateur.id,
                    'nom': utilisateur.nom,
                    'image': profil.photo,
                    'sex': profil.sex,
                    'hobbies': profil.hobbies,
                    'age': profil.age,
                    'location': profil.location,
                    'orientation': profil.orientation,
                    'body_type': profil.body_type,
                })
            except Profile.DoesNotExist:
                print(f"Profile for user {utilisateur.nom} does not exist")
            except Préférences.DoesNotExist:
                print(f"Preferences for user {utilisateur.nom} do not exist")
    ################ FILTRES ##################
    user_profile = Profile.objects.get(utilisateur=current_user)
    user_age = user_profile.age
    age_range_min = user_age - 2
    age_range_max = user_age + 10
    if user_profile.sex == 'm' and user_profile.orientation == 'Hétérosexuel':
        recommended_profiles = [profile for profile in recommended_profiles if
                                profile['sex'] == 'f' and profile['age'] is not None and age_range_min <= profile['age'] <= age_range_max]
    elif user_profile.sex == 'f' and user_profile.orientation == 'Hétérosexuel':
        recommended_profiles = [profile for profile in recommended_profiles if
                                profile['sex'] == 'm' and profile['age'] is not None and age_range_min <= profile['age'] <= age_range_max]
    elif user_profile.orientation == 'Homosexuel':
        recommended_profiles = [profile for profile in recommended_profiles if
                                profile['sex'] == user_profile.sex and profile['age'] is not None and age_range_min <= profile['age'] <= age_range_max]
    elif user_profile.orientation == 'Bisexuel':
        recommended_profiles = [profile for profile in recommended_profiles if profile['age'] is not None and age_range_min <= profile['age'] <= age_range_max]

    ################ FILTRES ##################
    localisation = request.GET.get('Localisation')
    age_min = request.GET.get('age_min')
    age_max = request.GET.get('age_max')
    hobbies_filter = request.GET.get('hobbies')

    if age_min:
        recommended_profiles = [profile for profile in recommended_profiles if profile['age'] is not None and profile['age'] >= int(age_min)]
    if age_max:
        recommended_profiles = [profile for profile in recommended_profiles if profile['age'] is not None and profile['age'] <= int(age_max)]
    if localisation:
        recommended_profiles = [profile for profile in recommended_profiles if profile['location'] == localisation]
    if hobbies_filter:
        hobbies_filter_set = set(hobbies_filter.split(', '))
        recommended_profiles = [profile for profile in recommended_profiles if hobbies_filter_set & set(profile['hobbies'].split(', '))]

    # Passer les recommandations au template
    context = {
        'form': SuggestionFilterForm(),
        'matchs': matchs,
        'recommended_profiles': recommended_profiles,
    }
    return render(request, 'profile/suggestion_profiles.html', context)


@login_required
def recherche_profiles(request):
    if not request.user.is_active:
        return redirect('connexion')
    utilisateurs = Profile.objects.all()
    profile = Profile.objects.get(utilisateur=request.user)

    utilisateurs_filter = UserFilter(request.GET, queryset=utilisateurs)

    context = {'form': utilisateurs_filter.form,
               'profiles': utilisateurs_filter.qs,
               'user': profile
               }
    return render(request, 'profile/recherche.html', context)


########################################## MESSAGERIE #######################################
@login_required
def discussion_list(request):
    discussions = Discussion.objects.filter(user1=request.user) | Discussion.objects.filter(user2=request.user)
    return render(request, 'chat/discussion_list.html', {'discussions': discussions})


@login_required
def discussion_detail(request, discussion_id):
    discussion = get_object_or_404(Discussion, id=discussion_id)
    messages = Message.objects.filter(discussion=discussion)
    return render(request, 'chat/discussion_detail.html', {'discussion': discussion, 'messages': messages})


@login_required
def start_chat(request, user_id):
    user1 = request.user
    user2 = get_object_or_404(Utilisateur, id=user_id)

    if user1 == user2:
        return redirect('recherche_profiles')  # Empêcher un utilisateur de discuter avec lui-même

    discussion = Discussion.objects.filter(
        (Q(user1=user1) & Q(user2=user2)) | (Q(user1=user2) & Q(user2=user1))
    ).first()

    if not discussion:
        discussion = Discussion.objects.create(user1=user1, user2=user2)

    return redirect('discussion_detail', discussion_id=discussion.id)
