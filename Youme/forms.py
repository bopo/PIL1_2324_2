from django import forms

from .models import *


class InscriptionForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Utilisateur
        fields = ['nom', 'email', 'password']

    def save(self, commit=True):
        user = super(InscriptionForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])  # Hacher le mot de passe
        if commit:
            user.save()
        return user


class ConnexionForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)


hobbies_list = [
    "Lecture", "Cinéma", "Voyages", "Cuisine", "Sport", "Randonnée",
    "Musique", "Photographie", "Dessin", "Écriture", "Jardinage",
    "Pêche", "Chasse", "Collection", "Jeux vidéo", "Bricolage",
    "Danse", "Théâtre", "Astronomie", "Yoga"
]


class PersonalityTestForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['age', 'height', 'sex', 'orientation', 'body_type', 'diet', 'drink', 'drugs', 'education', 'location', 'offspring', 'smokes', 'religion', 'origin', 'langue',
                  'hobbies', 'bio']

    age = forms.IntegerField(label='Entrez votre âge ', min_value=18, max_value=100)
    sex = forms.ChoiceField(label='Votre sexe ', choices=[('m', 'Homme'), ('f', 'Femme')])
    bio = forms.CharField(label="", widget=forms.Textarea(attrs={'max_length': 1000}))
    hobbies = forms.MultipleChoiceField(
        label='Hobbies',
        choices=[(hobby, hobby) for hobby in hobbies_list],
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    def clean_hobbies(self):
        data = self.cleaned_data['hobbies']
        if len(data) != 3:
            raise forms.ValidationError("Veuillez sélectionner trois hobbies.")
        return data


class PreferencesForm(forms.ModelForm):
    class Meta:
        model = Préférences
        fields = ['location', 'religion', 'origin', 'physique', 'education', 'lifestyle', 'hobbies']

    location = forms.ChoiceField(label='Où souhaitez vous rencontrer votre partenaire ?',
                                 choices=[('Abidjan', 'Abidjan'), ('Dakar', 'Dakar'), ('Lomé', 'Lomé'), ('Bamako', 'Bamako'), ('Ouagadougou', 'Ouagadougou'), ('Accra', 'Accra'),
                                          ('Cotonou', 'Cotonou')])
    religion = forms.ChoiceField(label="Quelle religion préferez-vous ?", choices=[('Chrétien', 'Chrétien'), ('Musulman', 'Musulman'), ('Aucune', 'Aucune'), ('Autre', 'Autre')])
    origin = forms.ChoiceField(label='Avez-vous un pays préféré parmi ceux-ci ?',
                               choices=[('Côte d\'Ivoire', 'Côte d\'Ivoire'), ('Sénégal', 'Sénégal'), ('Togo', 'Togo'), ('Mali', 'Mali'), ('Burkina Faso', 'Burkina Faso'),
                                        ('Ghana', 'Ghana'), ('Bénin', 'Bénin')])
    physique = forms.ChoiceField(label='Quel est la physique idéal pour vous ?',
                                 choices=[('Athlétique', 'Athlétique'), ('Moyen', 'Moyen'), ('En surpoids', 'En surpoids'), ('Minces', 'Minces')])
    education = forms.ChoiceField(label="Quel est le niveau d'étude normal pour vous ?",
                                  choices=[('École secondaire', 'École secondaire'), ('Licence', 'Licence'), ('Master', 'Master'), ('Doctorat', 'Doctorat')])
    lifestyle = forms.ChoiceField(label='Vous préférez être actif ou sédimentaire ?', choices=[('Actif', 'Actif'), ('Sédentaire', 'Sédentaire')])
    hobbies = forms.MultipleChoiceField(
        label='Hobbies souhaités',
        choices=[(hobby, hobby) for hobby in hobbies_list],
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    def clean_hobbies(self):
        data = self.cleaned_data['hobbies']
        if len(data) != 3:
            raise forms.ValidationError("Veuillez sélectionner trois hobbies.")
        return data


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo', 'age', 'height', 'sex', 'orientation', 'body_type', 'diet', 'drink', 'drugs', 'education', 'location', 'offspring', 'smokes', 'religion', 'origin',
                  'langue', 'hobbies', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'hobbies': forms.CheckboxSelectMultiple,
        }


############################################### FILTRES ###############################################
class SuggestionFilterForm(forms.Form):
    Localisation = forms.CharField(required=False)
    age_min = forms.IntegerField(required=False)
    age_max = forms.IntegerField(required=False)
    hobbies = forms.CharField(required=False, help_text="Séparez les centres d'intérêts par des virgules")


class SearchFilterForm(forms.Form):
    Localisation = forms.CharField(required=False)
    sex = forms.ChoiceField(choices=[('m', 'Homme'), ('f', 'Femme')])
    age_min = forms.IntegerField(required=False)
    age_max = forms.IntegerField(required=False)
    silhouette = forms.ChoiceField(choices=[('Athlétique', 'Athlétique'), ('Moyen', 'Moyen'), ('En surpoids', 'En surpoids'), ('Minces', 'Minces')])
    hobbies = forms.CharField(required=False, help_text="Séparez les centres d'intérêts par des virgules")
